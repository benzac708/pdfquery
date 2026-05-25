FROM python:3.12-slim

WORKDIR /app

COPY setup.py .
COPY ccep/ ccep/

RUN pip install --no-cache-dir -e .

COPY app.py .
COPY .env.example .env

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
