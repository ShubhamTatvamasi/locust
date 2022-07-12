# Docker

Pull the docker image:
```bash
docker pull locustio/locust
```

Start the locust server:
```bash
docker run -p 8089:8089 -v $PWD:/mnt/locust locustio/locust -f /mnt/locust/locustfile.py
```
