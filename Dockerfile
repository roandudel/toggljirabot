FROM python:3.9-slim

COPY requiremets.txt /usr/scr/app/requiremets.txt
RUN pip install --no-cache-dir -r /usr/scr/app/requiremets.txt

COPY ./togglejirabot /usr/scr/app/togglejirabot

ENV PYTHONPATH "${PYTHONPATH}:/usr/scr/app"

WORKDIR /usr/scr/app/togglejirabot

CMD ["python", "main.py"]