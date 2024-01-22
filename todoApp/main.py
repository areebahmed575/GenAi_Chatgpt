from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from database import engine

app = FastAPI()

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

class Todos(BaseModel):
    name: str
    description: str


class TodoUpdate(BaseModel):
    name: str
    description: str


# Define a dependency function get_db() that yields a database session (db). 
# This function ensures that the database session is properly closed after it's used. 
# This dependency will be used by other routes to get a database session.
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todos/")
def create_todo(todo: Todos, db: Session = Depends(get_db)):
    db_todo = Todo(name=todo.name, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in updated_todo.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted"}