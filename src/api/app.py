from fastapi import FastAPI


app = FastAPI()


@app.get("/api/healthchecker")
async def root():
    return {"message": "Hello from FastAPI in Docker!"}
