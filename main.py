import uvicorn
from fastapi import FastAPI
from api.routes import adbo_router

app = FastAPI(
    title="AdbO Backend Solution",
    description="This is the backend API for the entire AdbO Solution",
    version="0.0.0",
    redoc_url=None
)

app.include_router(adbo_router)


# just for debugging purpose
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

