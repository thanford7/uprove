# syntax=docker/dockerfile:1

FROM nikolaik/python-nodejs:python3.9-nodejs16
RUN apt-get update && apt-get install -y ffmpeg chromium-driver poppler-utils libfile-mimeinfo-perl libimage-exiftool-perl ghostscript libsecret-1-0 zlib1g-dev libjpeg-dev imagemagick libmagic1 webp
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 libgtk-4-1 libnspr4 libnss3 libxcomposite1 libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils libu2f-udev libvulkan1
RUN apt-get install -f -y ./google-chrome-stable_current_amd64.deb
WORKDIR /up

COPY up/requirements.txt .

RUN pip install -r requirements.txt
COPY /up .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN ["chmod", "+x", "/up/run_job_scraper.sh"]
CMD /up/run_job_scraper.sh