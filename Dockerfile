# syntax=docker/dockerfile:1

FROM nikolaik/python-nodejs:python3.9-nodejs16
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN sudo apt install ./google-chrome-stable_current_amd64.deb
RUN apt-get update && apt-get install -y ffmpeg chromium-driver poppler-utils libfile-mimeinfo-perl libimage-exiftool-perl ghostscript libsecret-1-0 zlib1g-dev libjpeg-dev imagemagick libmagic1 webp
WORKDIR /up

COPY up/requirements.txt .

RUN pip install -r requirements.txt
COPY /up .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN ["chmod", "+x", "/up/run_job_scraper.sh"]
CMD /up/run_job_scraper.sh