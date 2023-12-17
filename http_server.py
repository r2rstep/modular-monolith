import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.application:app", host="localhost", port=8100, reload=True)
