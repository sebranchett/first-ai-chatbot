from fastapi import FastAPI
from chatbot import email_chain
from models.email_query import EmailQueryInput, EmailQueryOutput
from utils.async_utils import async_retry

app = FastAPI(
    title="Ask Erik Anything Chatbot",
    description="Endpoints for chatbot based on Erik's weekly emails",
)


@async_retry(max_retries=10, delay=1)
async def invoke_agent_with_retry(query: str):
    """Retry the query if it fails to run.

    This can help when there are intermittent connection issues
    to external APIs.
    """
    return await email_chain.ainvoke({"input": query})


@app.get("/")
async def get_status():
    return {"status": "running"}


@app.post("/email-query")
async def query_email_agent(query: EmailQueryInput) -> EmailQueryOutput:
    query_response = await invoke_agent_with_retry(query.text)
    query_response["intermediate_steps"] = [
        str(s) for s in query_response["intermediate_steps"]
    ]

    return query_response
