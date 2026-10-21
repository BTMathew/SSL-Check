"""Check a website's TLS certificate expiration using Python's standard library."""

import argparse
import socket
import ssl
from datetime import datetime, timezone
from urllib.parse import urlsplit


def parse_website(value):
    """Accept a hostname or an HTTPS URL, optionally including a port."""
    value = value.strip()
    if not value:
        raise ValueError("Enter a website hostname or HTTPS URL.")
    parsed = urlsplit(value if "://" in value else "//" + value)
    if parsed.scheme and parsed.scheme.lower() != "https":
        raise ValueError("Use an HTTPS URL or a hostname, such as example.com.")
    if not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Enter a valid hostname or HTTPS URL without credentials.")
    hostname = parsed.hostname.encode("idna").decode("ascii")
    port = parsed.port if parsed.port is not None else 443
    if not 1 <= port <= 65535:
        raise ValueError("The port must be between 1 and 65535.")
    return hostname, port


def check_expiration(hostname, port=443, timeout=10):
    """Return the verified server certificate's expiration in UTC."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port), timeout=timeout) as connection:
        with context.wrap_socket(connection, server_hostname=hostname) as secured:
            certificate = secured.getpeercert()
    return datetime.fromtimestamp(
        ssl.cert_time_to_seconds(certificate["notAfter"]), tz=timezone.utc
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("website", nargs="?", help="Hostname or HTTPS URL")
    args = parser.parse_args()
    try:
        value = args.website if args.website is not None else input("Website: ")
        hostname, port = parse_website(value)
        expires = check_expiration(hostname, port)
        days_left = (expires - datetime.now(timezone.utc)).total_seconds() / 86400
        print(f"Website: {hostname}:{port}")
        print(f"Certificate expires: {expires:%Y-%m-%d %H:%M:%S} UTC")
        print(f"Time remaining: {days_left:.1f} days")
        return 0
    except ssl.SSLCertVerificationError as error:
        print(f"Certificate verification failed: {error.verify_message}")
        print("The certificate may be expired, untrusted, or for a different hostname.")
    except (ValueError, UnicodeError) as error:
        print(f"Invalid website: {error}")
    except (OSError, ssl.SSLError) as error:
        print(f"Unable to check certificate: {error}")
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
