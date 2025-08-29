FROM python:3.11-slim

WORKDIR /app

COPY . .

CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]