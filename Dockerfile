# syntax=docker/dockerfile:1

FROM nikolaik/python-nodejs:python3.9-nodejs16
RUN apt-get update && apt-get install -y ffmpeg poppler-utils libfile-mimeinfo-perl libimage-exiftool-perl ghostscript libsecret-1-0 zlib1g-dev libjpeg-dev imagemagick libmagic1 webp
WORKDIR /up

COPY up/requirements.txt .

RUN pip install -r requirements.txt
COPY /up .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD /up/run_job_scraper.sh