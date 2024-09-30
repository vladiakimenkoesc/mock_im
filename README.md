```
docker build -t mock-im .
docker run --network=net --name mock-im-api -p 5050:5050 -e ITEMS_PER_RESPONSE=10 -e FEED_FILE_PATH="/app/messages.json" -v $(pwd)/messages.json:/app/messages.json mock-im
```
