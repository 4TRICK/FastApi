def dict_fields_to_str_converter(d) -> dict:
    result = {}
    for key, value in d.items():
        if isinstance(value, dict):
            result[key] = dict_fields_to_str_converter(value)
        elif (
            isinstance(value, bool)
            or isinstance(value, int)
            or isinstance(value, float)
        ):
            result[key] = value
        else:
            result[key] = str(value)
    return result


def list_fields_to_str_converter(l) -> list:
    return [
        dict_fields_to_str_converter(item) if isinstance(item, dict) else item
        for item in l
    ]
