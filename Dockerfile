FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /testpad-homework-backend

RUN pip install django django-cors-headers djangorestframework requests beautifulsoup4

# copy from the current directory of the Dockerfile to /backend in the image
COPY . .

RUN python manage.py makemigrations

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]