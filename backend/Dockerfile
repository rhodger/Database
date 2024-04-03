FROM python:latest

EXPOSE 3068

WORKDIR code

RUN python3 -m pip install flask flask_cors thefuzz

COPY . .

CMD ["python3", "./backend.py"]
