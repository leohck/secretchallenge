FROM python:3.8-slim-buster
WORKDIR /desafiobrasilprev
COPY ./game/* ./game/
COPY ./main.py .
COPY ./api.py .
COPY ./requirements.txt .


RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "api.py"]
