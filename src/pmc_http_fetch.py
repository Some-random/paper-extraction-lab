"""Small Python-3.10 HTTPS bridge; retains TLS verification and strict byte caps.

Stdout is one JSON header line followed by raw response bytes. The parent
sequential batch worker reads the stream and owns storage/progress accounting.
No model imports, paid APIs, SSH, or background worker fan-out.
"""
import json
import sys
import urllib.request


def main():
    url, maximum = sys.argv[1], int(sys.argv[2])
    header_sent = False
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'paper-extraction-lab/0.2 (sequential PMC research batch)'})
        with urllib.request.urlopen(request, timeout=35) as response:
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
                chunk = response.read(min(262144, maximum - total))
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
        print(json.dumps({'ok': False, 'error': error, 'retryable': True}), flush=True)


if __name__ == '__main__':
    main()
