from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.auth_router import auth_router
from src.routes.transaction_router import transaction_router

app = FastAPI()

origins = ["http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(transaction_router)
