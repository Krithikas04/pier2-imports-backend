INVALID_PHONE = "10001"

ERROR_MAPPER = {
    INVALID_PHONE: {
        "en": "Invalid phone number"
    },
}



def field_error_format(error: dict[str, str]) -> dict[str, str]:
    try:
        field_name = error["loc"][1]
    except IndexError:
        field_name = "N/A"
    error_type = error["type"]
    if error_type == "missing":
        return {
            "en": f"{field_name} is required",
            "bn": f"{field_name} is required",
            "field": field_name,
        }
    if error_type == "value_error":
        code = error["msg"].split(",")[1].strip()
        message = ERROR_MAPPER.get(code, {})
        message["field"] = message.get("field", field_name)
        message["en"] = message.get("en", error.get("msg", "N/A"))
        return message
    return {
        "en": error.get("msg", "N/A"),
        "field": field_name,
    }




