import logging
import os
from langchain.schema import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableMap
from .utils import ChatOpenAI
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, crud
from app.database import get_db
from app.auth import get_current_user

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def create_simple_qa_chain(llm):
    """
    Create a simple QA chain using LangChain components.
    """
    template = """
    Give problem solution and answer to the following problem:
    Problem: {problem}
    Your answers should be in the language of the question.
    Give very detailed step-by-step solution. Answer should be numerical.
    """
    prompt = ChatPromptTemplate.from_template(template)

    chain = RunnableMap({
        "problem": RunnablePassthrough()  # Pass the question unchanged
    }) | prompt | llm | StrOutputParser()

    return chain

# Initialize the LLM
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No OPENAI_API_KEY found in environment variables")
llm = ChatOpenAI(temperature=0.0, course_api_key=api_key)
qa_chain = create_simple_qa_chain(llm)

router = APIRouter(
    prefix="/problems",
    tags=["problems"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Problem)
def submit_problem(problem: schemas.ProblemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_problem(db=db, problem=problem, user_id=current_user.id)

@router.get("/", response_model=list[schemas.Problem])
def get_problems(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Problem).filter(models.Problem.user_id == current_user.id).all()

@router.post("/solve", response_model=schemas.Solution)
def solve_problem(problem: schemas.ProblemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    try:
        solution_text = qa_chain.invoke(problem.problem_text)
        return {"solution": solution_text}
    except Exception as e:
        logging.error(f"Error processing problem: {e}")
        raise HTTPException(status_code=500, detail="Failed to get solution")