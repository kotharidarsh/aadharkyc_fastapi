from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST


async def http_exception_handler(_request: Request, exc: HTTPException,) -> JSONResponse:
    """

    :param _request:
    :param exc:
    :return:
    """
    payload = {"message": exc.detail}
    return JSONResponse(content=payload, status_code=exc.status_code)


async def request_validation_exception_handler(_request: Request, exc: RequestValidationError,) -> JSONResponse:
    """

    :param _request:
    :param exc:
    :return:
    """
    payload = {"message": "Validation Error", "detail": exc.errors()}
    return JSONResponse(content=payload, status_code=HTTP_400_BAD_REQUEST)


def register_handlers(app: FastAPI):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    return app
