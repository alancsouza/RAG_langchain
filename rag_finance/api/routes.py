import asyncio
import logging
from fastapi import FastAPI, status
from pydantic import BaseModel

from rag_finance.core.graph import question

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Finance API", version="1.0.0")


class MessageRequest(BaseModel):
    question: str


class MessageResponse(BaseModel):
    task_id: str
    status: str


@app.post("/message", response_model=MessageResponse, status_code=status.HTTP_202_ACCEPTED)
async def process_message(request: MessageRequest) -> MessageResponse:
    """
    Process a question and return a response.
    
    Args:
        request: MessageRequest containing the question
        
    Returns:
        MessageResponse containing the task ID and status
    """
    logger.info(f"Received request - Question: {request.question}")
    
    task = asyncio.create_task(question(request.question))
    
    task_id = str(id(task))
    logger.info(f"Created background task with ID: {task_id}")
    
    return MessageResponse(
        task_id=task_id,
        status="processing"
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
