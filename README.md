```
docker build -t mock-im .
docker run --name mock-im-api -p 5050:5050 --env-file .env -v "./${FEED_FILE_PATH}":/app/${FEED_FILE_PATH} mock-im:latest
```
