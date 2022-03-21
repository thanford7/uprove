# syntax=docker/dockerfile:1

FROM nikolaik/python-nodejs:python3.9-nodejs16
RUN apt-get update && apt-get install -y ffmpeg
WORKDIR /up

COPY up/requirements.txt .
COPY up/package.json .

RUN npm install npm@latest
RUN pip install -r requirements.txt
COPY /up .

ENV NODE_ENV=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV AWS_STORAGE_BUCKET_NAME=uprove-upload
ENV DJANGO_ALLOWED_HOSTS=.uprove.co
ENV PORT=8080
ENV DEFAULT_FROM_EMAIL=no_reply@uprove.co

ENV DB=local
ENV DEBUG="True"
ENV USE_LOCAL="True"

ARG DB_USER
ARG DB_PASSWORD
ARG SENDGRID_API_KEY
ENV DB_USER=$DB_USER
ENV DB_PASSWORD=$DB_PASSWORD
ENV SENDGRID_API_KEY=$SENDGRID_API_KEY

RUN npm run prod
RUN python manage.py collectstatic --noinput --clear
CMD ["gunicorn", "--worker-tmp-dir", "/dev/shm", "up.wsgi"]
EXPOSE $PORT