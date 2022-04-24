FROM oraclelinux:8

RUN dnf -y install oracle-instantclient-release-el8 oraclelinux-developer-release-el8 && \
    dnf -y module enable python38 && \
    dnf -y install oracle-instantclient-basic \
                   python38 python3-pip python38-pip python3-setuptools python36-cx_Oracle && \
    rm -rf /var/cache/dnf

WORKDIR /usr/src

RUN yum install -y nginx

RUN python3.8 -m pip install dash pandas cx_Oracle Flask Flask-SQLAlchemy python-dotenv gunicorn pycountry

COPY . .

# RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx /etc/init.d/
# RUN rm /etc/nginx/nginx.conf
COPY ./nginx.conf /etc/nginx/nginx.conf

# RUN systemctl start nginx

RUN chmod -R 775 /usr/src 
RUN chmod 775 /etc/init.d/nginx

RUN /etc/init.d/nginx start

# SHELL ["/bin/bash", "-c"] 

# CMD ["python3.8", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]

# "-b", "0.0.0.0:8080",
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:8080", "app:server"]