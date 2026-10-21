# AI prompt guide: building `ssl_check.py`

Use these prompts in order with a coding AI to recreate SSL Check. Only Python's standard library is needed. No credentials are required.

## 1. Create the project skeleton

```text
Create a Python 3.9+ project named SSL Check containing ssl_check.py, README.md, CHEAT.md, PROMPT.md, and .gitignore. Keep the program in one script using argparse, socket, ssl, datetime with timezone, and urllib.parse.urlsplit. Do not hard-code local absolute paths or add third-party dependencies.
```

## 2. Parse website input

```text
Implement parse_website(value). Strip whitespace and reject blank input. Accept bare hostnames, hostname:port, or HTTPS URLs. Prefix bare values with // for urlsplit. Reject explicit non-HTTPS schemes, missing hostnames, and embedded credentials. Convert the hostname to ASCII using IDNA. Default to port 443 and require ports from 1 through 65535. Return (hostname, port). Ignore paths, queries, and fragments. Do not follow redirects.
```

## 3. Retrieve the expiration

```text
Implement check_expiration(hostname, port=443, timeout=10). Use ssl.create_default_context() with normal certificate and hostname verification. Open socket.create_connection((hostname, port), timeout=timeout), then context.wrap_socket(connection, server_hostname=hostname). Use nested context managers for cleanup. Read getpeercert()["notAfter"], convert with ssl.cert_time_to_seconds, and return datetime.fromtimestamp(..., tz=timezone.utc). Propagate verification/connection errors. Do not bypass verification to inspect invalid certificates.
```

## 4. Add the command-line workflow

```text
Implement main() with argparse and an optional positional website argument. If absent, ask input("Website: "). Parse the website, retrieve expiration, and calculate (expires - datetime.now(timezone.utc)).total_seconds() / 86400. Print Website: hostname:port, Certificate expires: YYYY-MM-DD HH:MM:SS UTC, and Time remaining: N.N days. Return 0 on success. Keep normal --help support. Do not write result files or add batch processing/monitoring.
```

## 5. Handle failures

```text
Catch ssl.SSLCertVerificationError first and display verify_message plus possible expired/untrusted/hostname causes. Catch ValueError and UnicodeError as invalid input. Catch OSError and ssl.SSLError as connection failures. Catch EOFError and KeyboardInterrupt as cancellation. Return 1 for handled failures. Preserve argparse's standard help and syntax-error exits. Use if __name__ == "__main__": raise SystemExit(main()).
```

## 6. Verify behavior

```text
Check compilation and --help. Use offline mocks to verify bare-hostname/HTTPS/custom-port parsing, invalid inputs, certificate notAfter conversion to an aware UTC datetime, successful CLI output, and handled failure exit codes. Distinguish offline checks from live network tests. Do not claim a live connection was tested unless it was.
```

## 7. Document the project

```text
Write README.md covering behavior, requirements, input forms, interactive/direct commands, illustrative output, exit codes, troubleshooting, and the file tree. Explain that invalid/expired certificates produce verification errors, redirects are not followed, socket operations time out after 10 seconds, and DNS may take longer.

Write CHEAT.md with tables explaining imports, each function, and the entry point using accurate final-script line references. Write PROMPT.md with staged prompts and a condensed prompt.

Create .gitignore following a source/documentation allowlist: ignore new files by default, permit directory traversal, allow *.py, *.md, and .gitignore, and explicitly exclude Python caches and virtual environments. Keep all work local until publishing is requested.
```

## Single all-in-one prompt

```text
Build a Python 3.9+ standard-library SSL certificate expiration checker named ssl_check.py in SSL Check. Accept an optional website argument or prompt interactively. Use urlsplit to accept hostnames, HTTPS URLs, and custom ports; reject blank input, credentials, non-HTTPS schemes, and invalid ports. Normalize international hostnames using IDNA and default to 443.

Use socket.create_connection with a 10-second timeout and ssl.create_default_context with wrap_socket(server_hostname=hostname), preserving trust and hostname verification. Read getpeercert()["notAfter"] and convert it to a UTC-aware datetime with ssl.cert_time_to_seconds. Close connections with context managers. Print hostname/port, UTC expiration, and fractional days remaining to one decimal place. Return 0 on success and 1 for handled input, certificate, connection, or cancellation errors; retain argparse help and syntax-error behavior. Use a guarded SystemExit(main()) entry point.

Add README.md for setup/usage/troubleshooting, CHEAT.md with accurate code references, PROMPT.md with recreation instructions, and .gitignore allowing source/documentation while excluding caches/environments. Verify behavior with offline mocks and report any live tests separately. Keep everything local until asked to publish.
```
