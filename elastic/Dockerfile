FROM docker.elastic.co/elasticsearch/elasticsearch:8.15.0

COPY create_index.sh /tmp/create_index.sh
COPY es_index.json /tmp/es_index.json

CMD ["/bin/sh", "-c", "sh /tmp/create_index.sh & exec /usr/local/bin/docker-entrypoint.sh"]