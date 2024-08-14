import time
import requests

CHATBOT_URL = "http://localhost:8000/email-query"

questions = [
   "Does Erik have children?",
   "What does Erik like to wear?",
   "Does Erik drink wine?",
   "What are important topics for Erik?",
   "Who are Erik's colleagues?",
]

request_bodies = [{"text": q} for q in questions]

start_time = time.perf_counter()
outputs = [requests.post(CHATBOT_URL, json=data) for data in request_bodies]
end_time = time.perf_counter()

for i, output in enumerate(outputs):
    print(f"Question: {questions[i]}")
    print(f"Response: {output.json()}")
    print()

print(f"Run time: {end_time - start_time} seconds")
