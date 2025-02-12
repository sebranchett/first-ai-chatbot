from fastapi import FastAPI
from chatbot import email_agent_executor
from models.email_query import EmailQueryInput, EmailQueryOutput
from utils.async_utils import async_retry

app = FastAPI(
    title="AllAboutErik Chatbot",
    description="Endpoints for chatbot based on Erik's weekly emails",
)


@async_retry(max_retries=5, delay=1)
async def invoke_with_retry(query: str):
    """Retry the query if it fails to run.

    This can help when there are intermittent connection issues
    to external APIs.
    """
    return await email_agent_executor.ainvoke({"input": query})


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/email-query")
async def query_email(query: EmailQueryInput) -> EmailQueryOutput:
    query_response = await invoke_with_retry(query.text)
    query_response["intermediate_steps"] = [
        str(s) for s in query_response["intermediate_steps"]
    ]

    return query_response
