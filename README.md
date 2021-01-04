# locust


### Deploy on Kubernetes

Add helm repo and update
```bash
helm repo add deliveryhero https://charts.deliveryhero.io/

helm repo update
```

create config map:
```yaml
kubectl apply -f - << EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-loadtest-locustfile
data:
  main.py: |
    from locust import HttpUser, task, between

    class WebsiteUser(HttpUser):
        wait_time = between(1, 2)

        @task(1)
        def get_index(self):
            self.client.get("/")
EOF
```

Install locust:
```bash
helm install locust deliveryhero/locust \
  --set loadtest.locust_locustfile_configmap=my-loadtest-locustfile \
  --set service.type=NodePort \
  --set worker.hpa.enabled=true \
  --set worker.resources.limits.cpu=500m
```

Uninstall locust
```bash
helm un locust
```

Update NodePort
```bash
kubectl patch svc locust \
  --patch='{"spec": {"ports": [{"name": "master-p3", "nodePort": 30089, "port": 8089}]}}'
```

http://k8s.shubhamtatvamasi.com:30089
