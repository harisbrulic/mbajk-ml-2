FROM python:3.11-slim

WORKDIR /app

COPY src/serve/app.py ./src/serve/
COPY models ./models
COPY requirements.txt ./

RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 5000

CMD ["python", "src/serve/app.py"]
