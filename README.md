```
docker build -t mock-im .
docker run --name mock_im_api -p 5050:5050 -p 9001:9001 --env-file .env -v "./${FEED_FILE_PATH}":/app/${FEED_FILE_PATH} -v "./replies/replies.txt":/app/replies/replies.txt mock-im:latest
docker exec mock_im_api python -m http.server 9001 --directory /app/replies
```
