# syntax=docker/dockerfile:1

FROM seleniarm/standalone-chromium:latest

FROM nikolaik/python-nodejs:python3.9-nodejs16
RUN apt-get update && apt-get install -y sudo ffmpeg poppler-utils libfile-mimeinfo-perl libimage-exiftool-perl ghostscript libsecret-1-0 zlib1g-dev libjpeg-dev imagemagick libmagic1 webp
#RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN apt-get install -y fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 libgtk-3-0 libnspr4 libnss3 libxcomposite1 libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils libu2f-udev libvulkan1
#RUN apt-get install -f -y ./google-chrome-stable_current_amd64.deb
WORKDIR /up

COPY up/requirements.txt .
RUN pip install -r requirements.txt

RUN curl -s https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list && apt-get update && apt-get install -y google-chrome-stable
RUN google-chrome --version | grep -oE "[0-9]{1,10}.[0-9]{1,10}.[0-9]{1,10}" > /tmp/chromebrowser-main-version.txt
RUN wget --no-verbose -O /tmp/latest_chromedriver_version.txt https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$(cat /tmp/chromebrowser-main-version.txt)
RUN wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$(cat /tmp/latest_chromedriver_version.txt)/chromedriver_linux64.zip && rm -rf /opt/selenium/chromedriver && unzip /tmp/chromedriver_linux64.zip -d /opt/selenium && rm /tmp/chromedriver_linux64.zip && mv /opt/selenium/chromedriver /opt/selenium/chromedriver-$(cat /tmp/latest_chromedriver_version.txt) && chmod 755 /opt/selenium/chromedriver-$(cat /tmp/latest_chromedriver_version.txt) && ln -fs /opt/selenium/chromedriver-$(cat /tmp/latest_chromedriver_version.txt) /usr/bin/chromedriver

COPY /up .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN ["chmod", "+x", "/up/run_job_scraper.sh"]
CMD /up/run_job_scraper.sh