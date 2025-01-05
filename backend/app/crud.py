from sqlalchemy.orm import Session
from app import models, schemas

def create_problem(db: Session, problem: schemas.ProblemCreate, user_id: int):
    db_problem = models.Problem(**problem.dict(), user_id=user_id)
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem