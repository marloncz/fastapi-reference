import uvicorn

from fastapi_reference.service.api import app

uvicorn.run(app, host="0.0.0.0", port=8000)
