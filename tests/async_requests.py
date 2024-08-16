import asyncio
import time
import httpx

CHATBOT_URL = "http://localhost:8000/email-query"


async def make_async_post(url, data):
    timeout = httpx.Timeout(timeout=120)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, timeout=timeout)
        return response


async def make_bulk_requests(url, data):
    tasks = [make_async_post(url, payload) for payload in data]
    responses = await asyncio.gather(*tasks)
    outputs = [r.json()["output"] for r in responses]
    return outputs


questions = [
   "Does Erik have children?",
   "What does Erik like to wear?",
   "Does Erik drink wine?",
   "What are important topics for Erik?",
   "Who are Erik's colleagues?",
]

request_bodies = [{"text": q} for q in questions]

start_time = time.perf_counter()
outputs = asyncio.run(make_bulk_requests(CHATBOT_URL, request_bodies))
end_time = time.perf_counter()

for i, output in enumerate(outputs):
    print(f"Question: {questions[i]}")
    print(f"Response: {output}")
    print()

print(f"Run time: {end_time - start_time} seconds")
