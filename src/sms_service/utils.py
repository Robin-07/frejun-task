def validate_input(data, response):
    malformed_request = False
    params = ["from", "to", "text"]

    for param in params:
        if data.get(param) is None:
            response["error"] = f"{param} is missing"
            malformed_request = True
            break

    if not malformed_request:
        _from = data.get(params[0])
        _to = data.get(params[1])
        _text = data.get(params[2])
        
        if not _from.isnumeric() or len(_from) < 6 or len(_from) > 16:
            response["error"] = "from is invalid"
        elif not _to.isnumeric() or len(_to) < 6 or len(_to) > 16:
            response["error"] = "to is invalid"
        elif len(_text) < 1 or len(_text) > 120:
            response["error"] = "text is invalid"