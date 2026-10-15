import json
from pathlib import Path

from error import ConfigError


def load_config(path="config.json"):
    config_path = Path(path)

    if not config_path.exists():
        raise ConfigError(f"Config file not found: {path}")

    try:
        with config_path.open("r", encoding="utf-8") as file:
            config = json.load(file)
    except json.JSONDecodeError as Exception:
        raise ConfigError(f"Invalid JSON in {path}: {Exception}") from Exception

    validate_config(config)
    return config


def validate_config(config):
    if not isinstance(config, dict):
        raise ConfigError("Config root must be a JSON object")

    apis = config.get("apis")
    alerts = config.get("alerts")

    if not isinstance(apis, dict):
        raise ConfigError("Config must contain an 'apis' object")

    if not isinstance(alerts, list):
        raise ConfigError("Config must contain an 'alerts' array")

    for api_name, api in apis.items():
        if not isinstance(api, dict):
            raise ConfigError(f"API '{api_name}' must be an object")

        for field in ("url", "method", "response_balance_field"):
            if field not in api:
                raise ConfigError(
                    f"API '{api_name}' missing required field '{field}'"
                )

    for idx, alert in enumerate(alerts):
        if not isinstance(alert, dict):
            raise ConfigError(f"Alert at index {idx} must be an object")

        for field in (
            "id",
            "api_ref",
            "params",
            "threshold",
            "schedule_cron",
            "channels",
        ):
            if field not in alert:
                raise ConfigError(
                    f"Alert at index {idx} missing required field '{field}'"
                )

        if alert["api_ref"] not in apis:
            raise ConfigError(
                f"Alert '{alert['id']}' references unknown api_ref "
                f"'{alert['api_ref']}'"
            )