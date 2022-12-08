def success_response(message: str = "", data: dict = None, status: int = 200) -> (dict, int):
    return {
               "message": message,
               "data": data,
           }, status


def error_response(message: str, error: str, status: int = 400) -> (dict, int):
    return {
               "message": message,
               "error": error,
           }, status
