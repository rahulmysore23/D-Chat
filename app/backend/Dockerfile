FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# I know, I shouldn't be doing this. IYKYK
COPY . .

EXPOSE 5000

CMD ["python", "main.py"]
