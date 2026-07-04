from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette import status


class ErrorResponse(BaseModel):
    code: str
    message: str
    correlation_id: str | None = None


class EHISException(Exception):
    def __init__(self, code: str, message: str, http_status: int = status.HTTP_400_BAD_REQUEST):
        self.code = code
        self.message = message
        self.http_status = http_status
        super().__init__(message)


def install_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(EHISException)
    async def ehis_exception_handler(request: Request, exc: EHISException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.http_status,
            content=ErrorResponse(code=exc.code, message=exc.message, correlation_id=getattr(request.state, "correlation_id", None)).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        request.app.state.logger.exception("Unhandled exception", extra={"correlation_id": getattr(request.state, "correlation_id", None)})
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(code="internal_error", message="An unexpected error occurred.", correlation_id=getattr(request.state, "correlation_id", None)).model_dump(),
        )
