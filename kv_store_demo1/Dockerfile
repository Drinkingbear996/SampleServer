FROM python:3.6-alpine
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirement.txt
ENV PYTHONPATH=/app
EXPOSE 8080
CMD ["python", "main.py"]
