import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class GeneralResponse(BaseModel):
    """General response model for the API."""

    message: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins / list of urls to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", status_code=200, response_model=GeneralResponse)
async def health():
    """Health check endpoint.

    Returns:
        The status of the service.
    """
    return GeneralResponse(message="Service is up and running.")
