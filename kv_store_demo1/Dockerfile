# Use a lightweight Python image
FROM python:3.8-alpine

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirement.txt

EXPOSE 8080

CMD ["python", "main.py"]
