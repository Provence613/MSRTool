FROM python:3.6

LABEL MAINTAINER="Sonia Liu <fangxiaoliu@smail.nju.edu.cn>"

WORKDIR /var/www

ADD ./requirements.txt /var/www/requirements.txt
# Install native libraries, required for numpy

RUN pip3 install --upgrade setuptools

RUN python3 -m pip install --upgrade pip
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install gunicorn

RUN pip3 install -r requirements.txt
ADD . /var/www

EXPOSE 5000
CMD ["gunicorn","-w","4","--bind","0.0.0.0:5000","wsgi"]





