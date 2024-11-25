from fastapi import FastAPI
from example.http import router

app = FastAPI()
app.include_router(router, prefix="/api", tags=["Authentication"])
