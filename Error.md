```
>>> os.chdir("firmware")
>>> import main
network config: ('192.168.1.144', '255.255.255.0', '192.168.1.1', '192.168.1.1')
<< b'CONNECT {"name": null, "verbose": false, "ssl_required": false, "lang": "micropython", "version": "0.0.1", "pedantic": false}\r\n'
>> b'INFO {"server_id":"NCW232ZXKC6R3NJCGHWLQ3OGSWTFH35V2KQYM4HM3O3XKYOE3IHEIAAH","server_name":"us-south-nats-demo","version":"2.10.12","proto":1,"git_commit":"121169ea","go":"go1.21.8","host":"0.0.0.0","port":4222,"headers":true,"tls_available":true,"max_payload":1048576,"jetstream":true,"client_id":242410,"client_ip":"81.241.240.251","nonce":"PUWSNCJrmCPPskI","xkey":"XAPH3ZQWDK5GXPRVF6CAR2VF2FYE3HQA6324W24PSCMG4AOC7V2TJO56"}'
nats server connected
<< b'SUB area3001.ira.default.devices.0001.output  1\r\n'
heartbeat
<< b'PUB area3001.ira.default.devices.0001 176\r\n'
<< b'SUB area3001.ira.default.output  2\r\n'
<< b'{"hardware": {"version": "2024.1", "kind": "area3001_badge"}, "id": "0001", "group": "default", "network": {"mac": "C82B968B1744", "ip": "192.168.1.144"}, "name": "Badge Daan"}\r\n'
listening to ira messages
sent heartbeat
waiting
>> b"'Unknown Protocol Operation'"
Task exception wasn't retrieved
future: <Task> coro= <generator object 'wait' at 3ffd8200>
Traceback (most recent call last):
  File "asyncio/core.py", line 1, in run_until_complete
  File "nats.py", line 188, in wait
NATSError: b"'Unknown Protocol Operation'"
<< b'PUB area3001.ira.default.devices.0001 176\r\n'
<< b'{"hardware": {"version": "2024.1", "kind": "area3001_badge"}, "id": "0001", "group": "default", "network": {"mac": "C82B968B1744", "ip": "192.168.1.144"}, "name": "Badge Daan"}\r\n'
sent heartbeat
<< b'PUB area3001.ira.default.devices.0001 176\r\n'
Task exception wasn't retrieved
future: <Task> coro= <generator object '_heartbeat_loop' at 3ffd6050>
Traceback (most recent call last):
  File "asyncio/core.py", line 1, in run_until_complete
  File "ira.py", line 43, in _heartbeat_loop
  File "nats.py", line 143, in publish
  File "nats.py", line 218, in _send
  File "asyncio/stream.py", line 1, in write
OSError: [Errno 104] ECONNRESET
```