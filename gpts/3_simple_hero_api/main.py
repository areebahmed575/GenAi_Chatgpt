from typing import Optional

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True) #query ko fast krnay k liyai
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


database_url = "postgresql://areebstudent567:g4bOtYWUfE9s@ep-fancy-glitter-82049478.us-east-2.aws.neon.tech/sqlmodel?sslmode=require"

connect_args = {"check_same_thread": False}
engine = create_engine(database_url) #,echo=true means k jo query chal rahe h woh console mai dhekaye
# engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup") #jab kbhe server chaley tou is function ko chala du
def on_startup():
    create_db_and_tables()


@app.post("/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@app.get("/heroes/")
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes