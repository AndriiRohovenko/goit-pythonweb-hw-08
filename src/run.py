import uvicorn


def dev():
    uvicorn.run("src.main:app", host="127.0.0.1", port=8001, reload=True)


def prod():
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000)
