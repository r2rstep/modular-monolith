import uvicorn


if __name__ == "__main__":
    uvicorn.run("api.application:app", host="0.0.0.0", port=8100, reload=True)