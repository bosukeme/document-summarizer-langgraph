FROM python:3.13-slim

WORKDIR /app

RUN apt update && apt install -y --no-install-recommends --no-install-suggests \
build-essential python3-dev \
&& rm -rf /var/lib/apt/lists/* \
&& pip install --no-cache-dir --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir  -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
