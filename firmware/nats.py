import asyncio
import utime

from nats_utils import _urlparse, _build_connect_config, INFO, _build_inbox, MSG, PING, OK, ERR, _get_command, PONG, \
    NATSCommandException, NATSError


class Message(object):
    def __init__(self, sid, subject, size, data, reply=None):
        self.sid = sid
        self.subject = subject
        self.size = size
        self.data = data
        self.reply = reply


class Subscription(object):
    def __init__(self, sid, subject, queue, callback, connetion):
        self.sid = sid
        self.subject = subject
        self.queue = queue
        self.connetion = connetion
        self.callback = callback
        self.received = 0
        self.delivered = 0
        self.bytes = 0
        self.max = 0

    async def handle_msg(self, msg):
        return await self.callback(msg)


DEFAULT_URI = 'nats://192.168.1.3:4222'



class Connection(object):
    """
    A Connection represents a bare connection to a nats-server.
    """

    def __init__(
            self,
            url=DEFAULT_URI,
            name=None,
            ssl_required=False,
            verbose=False,
            pedantic=False,
            socket_keepalive=False,
            raw=False,
            debug=False
    ):
        self._reader = None
        self._writer = None

        self._connect_timeout = None
        self._socket_keepalive = socket_keepalive
        self._socket = None
        self._socket_file = None
        self._subscriptions = {}
        self._next_sid = 1
        self._raw = raw
        self._debug = debug
        self._options = {
            'url': _urlparse(url),
            'name': name,
            'ssl_required': ssl_required,
            'verbose': verbose,
            'pedantic': pedantic
        }

    async def connect(self):
        """
        Connect will attempt to connect to the NATS server. The url can
        contain username/password semantics.
        """
        self._reader, self._writer = await asyncio.open_connection(
            host=self._options['url']['host'],
            port=self._options['url']['port']
        )

        await self._send('CONNECT %s' % _build_connect_config(self._options))
        await self._recv(INFO)

    async def subscribe(self, subject, callback, queue=''):
        """
        Subscribe will express interest in the given subject. The subject can
        have wildcards (partial:*, full:>). Messages will be delivered to the
        associated callback.

        Args:
            subject (string): a string with the subject
            callback (function): callback to be called
        """
        s = Subscription(
            sid=self._next_sid,
            subject=subject,
            queue=queue,
            callback=callback,
            connetion=self
        )

        self._subscriptions[s.sid] = s
        await self._send('SUB %s %s %d' % (s.subject, s.queue, s.sid))
        self._next_sid += 1

        return s

    async def unsubscribe(self, subscription, max=None):
        """
        Unsubscribe will remove interest in the given subject. If max is
        provided an automatic Unsubscribe that is processed by the server
        when max messages have been received

        Args:
            subscription (pynats.Subscription): a Subscription object
            max (int=None): number of messages
        """
        if max is None:
            await self._send('UNSUB %d' % subscription.sid)
            self._subscriptions.pop(subscription.sid)
        else:
            subscription.max = max
            await self._send('UNSUB %d %s' % (subscription.sid, max))

    async def publish(self, subject, msg, reply=None):
        """
        Publish publishes the data argument to the given subject.

        Args:
            subject (string): a string with the subject
            msg (string): payload string
            reply (string): subject used in the reply
        """
        if msg is None:
            msg = ''

        if reply is None:
            command = 'PUB %s %d' % (subject, len(msg))
        else:
            command = 'PUB %s %s %d' % (subject, reply, len(msg))

        await self._send(command)
        await self._send(msg)

    async def request(self, subject, callback, msg=None):
        """
        publish a message with an implicit inbox listener as the reply.
        Message is optional.

        Args:
            subject (string): a string with the subject
            callback (function): callback to be called
            msg (string=None): payload string
        """
        inbox = _build_inbox()
        if self._debug:
            print('Inbox ID : {}'.format(inbox))

        s = self.subscribe(inbox, callback)
        await self.unsubscribe(s, 1)
        await self.publish(subject, msg, inbox)

        return s

    async def wait(self, duration=None, count=0):
        """
        Publish publishes the data argument to the given subject.

        Args:
            duration (float): will wait for the given number of seconds
            count (count): stop of wait after n messages from any subject
        """
        start = utime.time()
        total = 0
        print("waiting")
        while True:
            type, result = await self._recv(MSG, PING, OK)
            if type is MSG:
                total += 1
                if await self._handle_msg(result) is False:
                    break

                if count and total >= count:
                    break

            elif type is ERR:
                raise NATSError(result)

            elif type is PING:
                await self._handle_ping()

            if duration and utime.time() - start > duration:
                break

    async def reconnect(self):
        """
        Close the connection to the NATS server and open a new one
        """
        await self.close()
        await self.connect()

    async def close(self):
        """
        Close will close the connection to the server.
        """
        await self._reader.close()
        await self._writer.close()

    async def _send(self, command):
        msg = command + '\r\n'
        if not self._raw:
            msg = msg.encode('utf-8')

        if self._debug:
            print('<< {}'.format(msg))

        self._writer.write(msg)
        await self._writer.drain()

    async def _readline(self):
        lines = []

        while True:
            line = await self._reader.readline()
            if not self._raw:
                line = line.decode('utf-8')

            lines.append(line)

            if line.endswith("\r\n"):
                break

        return "".join(lines).strip()

    async def _recv(self, *args):
        line = await self._readline()
        command = _get_command(line)
        if not self._raw:
            line = line.encode('utf-8')
        # INFO regex has issue with parsing long Text in MicroPython.
        # Todo Update the below Condition Once it is fixed in Micropython
        # https://github.com/micropython/micropython/issues/2451
        if command is not INFO:
            result = command.match(line.strip())
        else:
            result = line
        if command in (OK, PING, PONG):
            result = result.group(0)
        elif command is ERR:
            result = result.group(2)
        elif command is MSG:
            result = {'subject': result.group(2), 'sid': result.group(4), 'reply': result.group(6),
                      'size': result.group(9)}

        if result is None:
            raise NATSCommandException(command, line)

        if self._debug:
            print('>> {}'.format(result))

        return command, result

    async def _handle_msg(self, result):
        data = result
        sid = int(data['sid'])

        msg = Message(
            sid=sid,
            subject=data['subject'],
            size=int(data['size']),
            data=self._readline(),
            reply=data['reply'].strip() if data['reply'] is not None else None
        )

        s = self._subscriptions.get(sid)
        s.received += 1

        # Check for auto-unsubscribe
        if s.max > 0 and s.received == s.max:
            self._subscriptions.pop(s.sid)

        return await s.handle_msg(msg)

    async def ping(self):
        await self._send('PING')
        await self._recv(PONG)

    async def _handle_ping(self):
        await self._send('PONG')
