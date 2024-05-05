import ure
import uos
import ubinascii
import ujson
import utime

NATS_SERVER_URL = ure.compile(b'^nats://(([^:^@.+]+):([^:^@.+]+)@)?([^:^@]+):([0-9]+)$')
MSG = ure.compile(b'MSG( )+([^ ]+)( )+([^ ]+)( )+(([^ ]+)( )+)?([0-9]+)$')
OK = ure.compile(b'^\+OK$')
ERR = ure.compile(b'^-ERR( )+(.+)?$')  # match 1: space 2: 'Err Msg'
PING = ure.compile(b'^PING$')
PONG = ure.compile(b'^PONG$')
INFO = ure.compile(b'^INFO( )+(.+)(.+)$')  # match 1: space 2: Info Msg
commands = {'+OK': OK, '-ERR': ERR, 'PING': PING, 'PONG': PONG, 'INFO': INFO, 'MSG': MSG}

def _get_command(line):
    values = line.strip().split(' ', 1)
    tmp_cmd = values[0].strip()
    tmp_command = commands.get(tmp_cmd)
    if tmp_command is None:
        raise NATSCommandException(
            'Command {} not found.Allowed Commands : {}'.format(tmp_cmd, 'INFO,+OK,PING,PONG,MSG,-ERR'))
    return tmp_command


def _urlparse(url):
    parsed_url = NATS_SERVER_URL.match(url)

    if parsed_url is None:
        raise NATSConnectionException(
            'Expected : {} Given : {}'.format('nats://[<username>:<password>@]<host>:<port>', url))

    return {'host': parsed_url.group(4), 'port': int(parsed_url.group(5)), 'username': parsed_url.group(2),
            'password': parsed_url.group(3)}


def _random_choice(seq):
    a = int(utime.time() * 256)  # use fractional seconds
    if not isinstance(a, int):
        a = hash(a)
    a, x = divmod(a, 30268)
    a, y = divmod(a, 30306)
    a, z = divmod(a, 30322)
    x, y, z = int(x) + 1, int(y) + 1, int(z) + 1
    x = (171 * x) % 30269
    y = (172 * y) % 30307
    z = (170 * z) % 30323
    _random = (x / 30269.0 + y / 30307.0 + z / 30323.0) % 1.0
    return seq[int(_random * len(seq))]


def _build_inbox():
    # ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
    # inbox_id = ''.join(self._random_choice(ascii_lowercase) for i in range(13))
    inbox_id = 'AAA666'
    while True:
        inbox_id = ure.match(r'\(?([a-zA-Z0-9]+)', ubinascii.b2a_base64(uos.urandom(16)).strip())
        if inbox_id is not None:
            inbox_id = inbox_id.group(1).upper()[2:8]
            if inbox_id and len(inbox_id) == 6:
                break

    return "_INBOX.%s" % inbox_id


def _build_connect_config(opts):
    config = {
        'verbose': opts['verbose'],
        'pedantic': opts['pedantic'],
        'ssl_required': opts['ssl_required'],
        'name': opts['name'],
        'lang': 'micropython',
        'version': '0.0.1'
    }

    if opts['url']['username'] is not None:
        config['user'] = opts['url']['username']
        config['pass'] = opts['url']['password']

    return ujson.dumps(config)


class NATSConnectionException(Exception):
    pass


class NATSCommandException(Exception):
    pass


class NATSError(Exception):
    pass


# class SocketError(Exception):
#     @staticmethod
#     def wrap(wrapped_function, *args, **kwargs):
#         try:
#             return wrapped_function(*args, **kwargs)
#         except usocket.error as err:
#             raise NATSConnectionException(err)

#
# def rm(d):  # Remove file or tree
#     try:
#         if os.stat(d)[0] & 0x4000:  # Dir
#             for f in os.ilistdir(d):
#                 if f[0] not in ('.', '..'):
#                     rm("/".join((d, f[0])))  # File or Dir
#             os.rmdir(d)
#         else:  # File
#             os.remove(d)
#     except:
#         print("rm of '%s' failed" % d)