import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import adbo_router
from api.utils.definition_data import tags_metadata
from config.config import CONFIGS

app = FastAPI(
    title='AdbO Backend Solution',
    description='This is the backend API for the entire AdbO system',
    version='0.0.1',
    redoc_url=None,
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIGS.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(adbo_router)

# just for debugging purpose
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8100)
