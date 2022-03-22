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

RUN npm run prod
CMD ["gunicorn", "--worker-tmp-dir", "/dev/shm", "up.wsgi"]