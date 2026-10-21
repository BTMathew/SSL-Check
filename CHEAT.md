# `ssl_check.py` cheat sheet

Project-specific reference for the current 64-line script. Update the line references when the code changes. Blank separator lines are omitted.

## Imports (lines 1-7)

| Lines | Code | What it does here |
| --- | --- | --- |
| 1 | Module docstring | Describes the tool and supplies the CLI help description. |
| 3 | `argparse` | Parses the optional website argument and provides help. |
| 4 | `socket` | Opens the TCP connection. |
| 5 | `ssl` | Configures verified TLS and parses certificate dates. |
| 6 | `datetime`, `timezone` | Represents current and expiration times in UTC. |
| 7 | `urlsplit` | Extracts hostname and port from input. |

## Website parser - `parse_website` (lines 10-24)

| Lines | Code | What it does here |
| --- | --- | --- |
| 10-11 | Function and docstring | Accepts a hostname or HTTPS URL with an optional port. |
| 12-14 | Strip and empty check | Trims whitespace and rejects blank input. |
| 15 | `urlsplit` | Prefixes bare hostnames with `//` so they parse as network locations. |
| 16-17 | Scheme validation | Rejects explicit schemes other than HTTPS. |
| 18-19 | Host and credential validation | Requires a hostname and rejects usernames/passwords in URLs. |
| 20 | IDNA conversion | Converts international domain names to ASCII. |
| 21 | Port selection | Uses the supplied port or defaults to 443; malformed ports raise ValueError. |
| 22-23 | Port validation | Requires a port between 1 and 65535. |
| 24 | Tuple return | Returns `(hostname, port)`. |

Paths, queries, and fragments are ignored. Parsing does not prove a hostname exists.

## TLS connection - `check_expiration` (lines 27-35)

| Lines | Code | What it does here |
| --- | --- | --- |
| 27-28 | Function and defaults | Uses port 443 and a 10-second socket timeout by default. |
| 29 | `create_default_context()` | Enables normal certificate trust and hostname verification. |
| 30 | `create_connection(...)` | Resolves and connects to the host, with automatic socket cleanup. |
| 31 | `wrap_socket(...)` | Performs TLS; `server_hostname` supplies SNI and the expected hostname. |
| 32 | `getpeercert()` | Reads the verified server certificate as a dictionary. |
| 33-35 | Expiration conversion | Converts `notAfter` to Unix seconds and returns a UTC-aware datetime. |

Expired or invalid certificates fail verification before a date is returned. DNS may take longer than the socket timeout.

## Main workflow (lines 38-60)

| Lines | Code | What it does here |
| --- | --- | --- |
| 38-41 | Argument parser | Defines optional positional `website`; `nargs="?"` allows interactive use. |
| 42-43 | Input selection | Uses the argument or prompts with `Website:`. |
| 44-45 | Parse and check | Validates input and retrieves expiration. |
| 46 | Days calculation | Divides remaining seconds by 86,400. |
| 47-49 | Output | Prints host/port, UTC expiration, and days to one decimal place. |
| 50 | Success | Returns exit code 0. |
| 51-53 | Verification failure | Prints the verification message and possible causes. |
| 54-55 | Invalid input | Handles ValueError and UnicodeError. |
| 56-57 | Connection failure | Handles socket, DNS, timeout, and TLS errors. |
| 58-59 | Cancellation | Handles EOF and Ctrl+C. |
| 60 | Failure | Returns exit code 1 after handled errors. |

Argument parsing occurs before the try block. Help exits with 0; invalid CLI syntax exits with 2.

## Entry point (lines 63-64)

| Lines | Code | What it does here |
| --- | --- | --- |
| 63 | Main guard | Runs the CLI only when executed directly. |
| 64 | `SystemExit(main())` | Exposes main's return value as the process exit code. |

## Files and commands

```text
SSL Check/
|-- ssl_check.py     # Program
|-- README.md        # Setup and usage
|-- CHEAT.md         # Code reference
|-- PROMPT.md        # Recreation guide
`-- .gitignore      # Tracking rules
```

```powershell
python ssl_check.py
python ssl_check.py example.com
python ssl_check.py --help
```

No credentials, input files, or generated output files are needed.
