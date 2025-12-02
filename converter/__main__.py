"""Run the API."""

import uvicorn

from converter.router import app

API_HOST = "0.0.0.0"
API_PORT = 8000

if __name__ == "__main__":
    "Runs the main API."
    uvicorn.run(app, host=API_HOST, port=API_PORT)
