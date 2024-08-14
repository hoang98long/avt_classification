FROM python:3.8 as requirements-stage

WORKDIR /app

COPY /home/avt/avt_classification /app/avt_classification

RUN chmod +x /app/avt_classification/main.exe

CMD ["./avt_classification/main.exe"]