"""Parse CLI argument and convert to .epub."""

import uvicorn

from converter.router import app

API_HOST = "0.0.0.0"
API_PORT = 8000

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)
