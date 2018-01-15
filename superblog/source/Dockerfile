FROM ubuntu:17.10

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install curl zip

# install chromedriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
    ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

# Install Google Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -y update && \
    apt-get -y install google-chrome-stable

RUN bash -c "debconf-set-selections <<< 'mysql-server mysql-server/root_password password eSeeM1ooyo'"
RUN bash -c "debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password eSeeM1ooyo'"

RUN apt-get -y install mysql-server python python-pip python-dev \
                       libmysqlclient-dev libgconf-2-4 xvfb python-selenium

RUN pip2 install 'Django<2' mysqlclient gunicorn requests

ADD mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf

ADD dump.sql /tmp/
RUN service mysql start && \
    mysql -uroot -peSeeM1ooyo < /tmp/dump.sql && \
    rm /tmp/dump.sql

# xss user
RUN groupadd -g 1000 xss-man && useradd -g xss-man -u 1000 xss-man

ADD flag1 /asdjkasecretflagfile1
ADD flag2 /asdjkasecretflagfile2
COPY app /app

ENV DOCKER 1
RUN service mysql start && \
    cd /app && \
    python2 manage.py migrate && \
    python2 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_user(username='admin', password='eevii0et8em7wei9Tahw', email='')" && \
    python2 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_user(username='foo', password='bar', email='')"

RUN mkdir /bot
ADD scripts/chrome.py scripts/bot.py scripts/login.py /bot/
RUN chown -R xss-man:xss-man /bot/ && \
    chmod 500 /bot/*

RUN apt-get -y install nginx
COPY nginx/default /etc/nginx/sites-available/default

CMD service mysql start && service nginx start && \
    cd /app && \
    (gunicorn -w 32 blog.wsgi --bind 0.0.0.0:1342 & \
    su xss-man -c 'python2 /bot/bot.py' & \
    /bin/bash -i)
