import json
import argparse
from pathlib import Path

def main(path):
    lp_json = Path(path)
    with open(lp_json) as fd:
        lp_data = json.load(fd)
    ae_entries = []
    ae_data = {
        "version": 1,
        "header": { "slots": None, "params": None },
        "db": { "version": 2, "entries": ae_entries },
    }
    for account in lp_data.get("accounts", []):
        entry = {
            "type": "totp",
            "uuid": account.get("accountID"),
            "name": account.get("issuerName"),
            "issuer": account.get("originalIssuerName"),
            "note": account.get("userName", ""),
            "favorite": account.get("isFavorite", False),
            "icon": None,
            "info": {
                "secret": account.get("secret"),
                "algo": account.get("algorithm"),
                "digits": account.get("digits"),
                "period": account.get("timeStep"),
            },
        }
        ae_entries.append(entry)
    ae_json = lp_json.parent / f"aegis_{lp_json.name}"
    with open(ae_json, "w") as fd:
        json.dump(ae_data, fd)
    print(f"Converted. Export file: {ae_json}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("LastPass Authenticator to Aegis JSON Converter")
    parser.add_argument("filename", help="LastPass Authenticator JSON File")
    args = parser.parse_args()
    main(args.filename)
