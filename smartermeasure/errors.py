class APICallError(Exception):
    pass


class QueryStringError(APICallError):
    pass


class MissingUserIdError(APICallError):
    message = "Missing user_id. Use SmarterMeasure.user(user_id)"


class AuthenticationFailedError(APICallError):
    status_int = 403
    message = "(Forbidden) The server failed to authenticate the request." \
              " Verify that the value of Authorization header is formed" \
              " correctly and includes the signature."


class InternalError(APICallError):
    status_int = 500
    message = "(Internal Server Error) The server encountered an internal error." \
              " Please retry the request."


class InvalidAuthenticationInfoError(APICallError):
    status_int = 400
    message = "(Bad Request) The authentication information was not" \
              " provided in the correct format." \
              " Verify the value of Authorization header."


class InvalidInputError(APICallError):
    status_int = 400
    message = "(Bad Request) One or more of the request inputs is not valid."


class InvalidProtocolError(APICallError):
    status_int = 400
    message = "(Bad Request) The request was not made under a secure connection," \
              " all requests must be made under SSL."


class InvalidUriError(APICallError):
    status_int = 400
    message = "(Bad Request) The requested URI does not represent any resource" \
              " on the server."


class ResourceNotFoundError(APICallError):
    status_int = 404
    message = "(Not Found) The specified resource does not exist."


class UnsupportedHttpVerbError(APICallError):
    status_int = 405
    message = "(Method Not Allowed) The resource doesn't support the specified" \
              " HTTP verb."
