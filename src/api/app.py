from fastapi import FastAPI, Depends, HTTPException, status
from src.db.configurations import get_db_session
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.api.users import router as users_router

from src.api.exceptions import (
    UserNotFoundError,
    DuplicateEmailError,
    user_not_found_handler,
    duplicate_email_handler,
)


app = FastAPI()


@app.get("/api/healthchecker")
async def healthchecker(db: Session = Depends(get_db_session)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
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
