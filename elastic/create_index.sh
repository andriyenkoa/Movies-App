ES_PORT=${ES_PORT:-9200}
echo "Waiting for Elasticsearch to be ready on port $ES_PORT..."
until curl -s http://localhost:$ES_PORT; do
  sleep 2
done

echo "Creating Elasticsearch index..."
curl -u -X PUT "http://localhost:$ES_PORT/movies" -H 'Content-Type: application/json' -d @/tmp/es_index.json
