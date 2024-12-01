from fastapi import Depends, FastAPI
from sqlmodel import Session, select

from src.database.config import get_session
from src.models.user import User
from src.routes.auth_router import auth_router
from src.routes.transaction_routes import transaction_router

app = FastAPI()


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.get("/all-users")
def get_all_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()


@app.post("/create-sample-user")
def create_sample_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()

    return {"created_user": user.username}


app.include_router(auth_router)
app.include_router(transaction_router)
