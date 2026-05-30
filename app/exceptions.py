from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

async def custom_http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Globally intercepts HTTPExceptions and wraps them in our standard APIResponse envelope.
    """
    # If detail is already a dictionary with a status key, return it directly
    if isinstance(exc.detail, dict) and "status" in exc.detail:
        payload = exc.detail
    else:
        # Map status codes to JSend statuses: 4xx = fail, 5xx = error
        status = "fail" if exc.status_code < 500 else "error"
        payload = {
            "status": status,
            "message": str(exc.detail),
            "data": None,
            "meta": None
        }
    return JSONResponse(status_code=exc.status_code, content=payload)


async def custom_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Globally intercepts validation errors (e.g., bad query parameters)
    and formats them cleanly in the APIResponse envelope.
    """
    errors = exc.errors()
    # Format a concise readable message from validation errors
    error_messages = [f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}" for err in errors]
    message = "Validation failed: " + "; ".join(error_messages)

    payload = {
        "status": "fail",
        "message": message,
        "data": None,
        "meta": {"errors": errors}
    }
    return JSONResponse(status_code=422, content=payload)


async def custom_general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Globally catches all unhandled exceptions (Internal Server Errors)
    and prevents them from leaking raw python tracebacks to clients.
    """
    payload = {
        "status": "error",
        "message": f"Internal Server Error: {str(exc)}",
        "data": None,
        "meta": None
    }
    return JSONResponse(status_code=500, content=payload)


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Registers all custom global exception handlers to the FastAPI application instance.
    """
    app.add_exception_handler(HTTPException, custom_http_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, custom_general_exception_handler)
