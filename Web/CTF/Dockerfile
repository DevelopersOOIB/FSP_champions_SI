FROM php:8.0-apache

COPY . /var/www/html/
RUN mkdir -p /var/www/html/uploads \
    && chmod 777 /var/www/html/uploads
RUN sed -i 's/80/5000/' /etc/apache2/ports.conf /etc/apache2/sites-enabled/000-default.conf
EXPOSE 5000
