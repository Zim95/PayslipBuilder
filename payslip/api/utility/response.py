def success(message):
    return {
        "type": "SUCCESS",
        "message": message
    }


def error(message):
    return {
        "type": "ERROR",
        "message": message
    }
