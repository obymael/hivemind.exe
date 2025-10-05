from titiler.core.factory import TilerFactory
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

tiler = TilerFactory()
app.include_router(tiler.router, prefix="/ndvi")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
