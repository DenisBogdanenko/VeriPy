FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "-m", "pytest"]
CMD ["-n", "2", "-v"]
