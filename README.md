# SSL Check

`ssl_check.py` checks when a website's TLS (commonly called SSL) certificate expires. Enter a hostname or HTTPS URL to see its expiration date in UTC and days remaining.

## What the script does

1. Reads a website from an argument or interactive prompt.
2. Extracts the hostname and optional port (default 443).
3. Opens a TCP connection and performs a verified TLS handshake.
4. Reads the server certificate's `notAfter` date.
5. Prints the expiration date and fractional days remaining.

## Requirements

- Python 3.9 or later
- Network access to the website's HTTPS port
- A working certificate trust store for Python

Uses only Python's standard library. No package installation, browser, credentials, or configuration files are required.

## Website input

```text
example.com
https://example.com
https://example.com/some/page
example.com:8443
```

Paths, queries, and fragments are ignored. The script connects directly to the supplied hostname without following HTTP redirects. Explicit non-HTTPS schemes and embedded credentials are rejected. International domain names are converted to IDNA form.

## Run the checker

Open a terminal in this folder:

```powershell
python ssl_check.py
```

Enter a website at `Website:` and press Enter. Alternatively:

```powershell
python ssl_check.py example.com
python ssl_check.py https://example.com:8443
python ssl_check.py --help
```

Use `python3` instead of `python` on systems where that is the installed command, or use the full path to your Python executable.

## Output

Illustrative output; these dates are examples rather than live results:

```text
Website: example.com:443
Certificate expires: 2030-12-31 23:59:59 UTC
Time remaining: 42.5 days
```

| Field | Description |
| --- | --- |
| Website | Normalized hostname and connection port |
| Certificate expires | Server certificate expiration date and time in UTC |
| Time remaining | Days until expiration, rounded to one decimal place |

Results appear in the terminal; no output file is created. Exit code 0 means success; 1 means a handled error or cancellation. Invalid command-line syntax uses argparse's exit code 2.

## Common issues

- **Python not found**: install Python 3 with PATH enabled or use an existing executable's full path.
- **Certificate verification failed**: the certificate may be expired, untrusted, or for another hostname. Check the computer's clock and Python trust store too. The tool reports this error instead of retrieving an expiration date for an invalid certificate.
- **Unable to check certificate**: check the hostname, network connection, firewall, and HTTPS port. DNS failures, refusals, timeouts, and TLS failures are reported here.
- **Invalid website**: use a hostname or HTTPS URL without credentials and a port from 1 through 65535.

Socket operations use a 10-second timeout; DNS resolution can take longer. The tool checks the server certificate presented to this connection. It does not audit every chain certificate, check every server behind a domain, or monitor renewals.

## Project files

```text
SSL Check/
|-- ssl_check.py
|-- README.md
|-- CHEAT.md
|-- PROMPT.md
`-- .gitignore
```

[CHEAT.md](CHEAT.md) explains the code. [PROMPT.md](PROMPT.md) provides step-by-step recreation prompts. The Git ignore rules allow source and documentation while excluding local environments and caches.

## Source

Documentation structure follows [Custom Craigslist All US Search Bot](https://github.com/BTMathew/Custom-Craigslist-All-US-Search-Bot). The SSL checker uses Python's built-in socket and TLS APIs.
