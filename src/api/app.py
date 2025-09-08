from fastapi import FastAPI, Depends, HTTPException, status, Request
from src.db.configurations import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.api.users import router as users_router

from src.api.exceptions import (
    UserNotFoundError,
    DuplicateEmailError,
    user_not_found_handler,
    duplicate_email_handler,
)
import time

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db_session)):
    try:
        result = await db.execute(text("SELECT 1"))
        row = result.fetchone()  # no await here
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database connection failed",
            )
        return {"message": "API is healthy and connected to the database"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {e}",
        )


app.add_exception_handler(UserNotFoundError, user_not_found_handler)
app.add_exception_handler(DuplicateEmailError, duplicate_email_handler)


app.include_router(users_router)
