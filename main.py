from loader import load_config
from api_client import APIClient, APIError


def main():
    config = load_config("config.json")
    client = APIClient(timeout=10)

    for alert in config["alerts"]:
        api_config = config["apis"][alert["api_ref"]]

        try:
            balance = client.fetch_balance(api_config, alert["params"])
            print(f"[{alert['id']}] {alert['api_ref']} balance = {balance}")
        except APIError as exc:
            print(f"[{alert['id']}] ERROR: {exc}")


if __name__ == "__main__":
    main()