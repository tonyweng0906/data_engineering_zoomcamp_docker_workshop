docker network create pg-network

docker-compose up

**Build the image:**
    docker build -t taxi_ingest:v001 .

docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips


docker-compose down