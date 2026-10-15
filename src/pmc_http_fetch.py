"""Small Python-3.10 HTTPS bridge; retains TLS verification and strict byte caps.

Stdout is one JSON header line followed by raw response bytes. The parent
sequential batch worker reads the stream and owns storage/progress accounting.
No model imports, paid APIs, SSH, or background worker fan-out.
"""
import json
import sys

import requests


def main():
    url, maximum = sys.argv[1], int(sys.argv[2])
    header_sent = False
    try:
        # requests[socks] understands the environment's socks5h proxy. urllib's
        # ProxyHandler sends HTTP to that SOCKS port and fails before TLS.
        with requests.get(url, stream=True, timeout=(15, 35), headers={
            'User-Agent': 'paper-extraction-lab/0.3 (sequential PMC research batch)',
            'Accept-Encoding': 'identity',
        }) as response:
            response.raise_for_status()
            expected = int(response.headers.get('Content-Length', '0'))
            if expected > maximum:
                print(json.dumps({'ok': False, 'error': 'Object exceeds available byte budget', 'content_length': expected}), flush=True)
                return
            print(json.dumps({'ok': True, 'content_length': expected}), flush=True)
            header_sent = True
            total = 0
            while total < maximum:
                if expected and total >= expected:
                    break
                chunk = response.raw.read(min(262144, maximum - total), decode_content=False)
                if not chunk:
                    break
                total += len(chunk)
                sys.stdout.buffer.write(chunk)
                sys.stdout.buffer.flush()
    except Exception as exc:
        error = type(exc).__name__ + ': ' + str(exc)
        if header_sent:
            # Never mix error messages into a partially received source object.
            print(error, file=sys.stderr, flush=True)
            raise SystemExit(2)
        status = getattr(getattr(exc, 'response', None), 'status_code', None)
        retryable = status is None or status in (408, 425, 429) or status >= 500
        print(json.dumps({'ok': False, 'error': error, 'retryable': retryable,
                          'http_status': status}), flush=True)


if __name__ == '__main__':
    main()
