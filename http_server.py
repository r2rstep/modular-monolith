import uvicorn

if __name__ == "__main__":
    uvicorn.run("api.application:app", host="localhost", port=8100, reload=True)
