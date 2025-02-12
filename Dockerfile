# chatbot_api/Dockerfile

FROM python:3.11-slim

WORKDIR /app
COPY ./src/ /app
COPY ./chroma_data/ /app/chroma_data

COPY ./pyproject.toml /code/pyproject.toml
RUN pip install /code/.

EXPOSE 8000
CMD ["sh", "entrypoint.sh"]