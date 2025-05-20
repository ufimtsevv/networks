FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY ru_ips.txt /etc/nginx/ru_ips.txt
COPY blocked.html /usr/share/nginx/html/blocked.html

RUN chmod 644 /etc/nginx/ru_ips.txt && \
    chmod 644 /usr/share/nginx/html/blocked.html