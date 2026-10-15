from error import ConfigError


def get_by_path(data, path, default=None):
    
    if not path:
        return data

    current = data
    for part in path.split("."):
        if isinstance(current, dict):
            if part not in current:
                return default
            current = current[part]
        elif isinstance(current, list):
            try:
                idx = int(part)
            except ValueError:
                return default
            if idx < 0 or idx >= len(current):
                return default
            current = current[idx]
        else:
            return default

    return current


def format_template(value, params):
    
    if isinstance(value, str):
        try:
            return value.format(**params)
        except KeyError as exc:
            raise ConfigError(
                f"Missing parameter {exc} in template: {value!r}"
            ) from exc

    if isinstance(value, dict):
        return {k: format_template(v, params) for k, v in value.items()}

    if isinstance(value, list):
        return [format_template(v, params) for v in value]

    return value