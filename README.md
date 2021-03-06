# locust


### Deploy on Kubernetes

Add helm repo and update
```bash
helm repo add deliveryhero https://charts.deliveryhero.io/

helm repo update
```

create config map:
```python
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
  --set worker.hpa.enabled=true \
  --set worker.hpa.targetCPUUtilizationPercentage=100 \
  --set worker.resources.limits.memory=256Mi \
  --set worker.resources.limits.cpu=200m \
  --set worker.resources.requests.memory=128Mi \
  --set worker.resources.requests.cpu=100m \
  --set service.type=NodePort
```
> Remove NodePort if you have LoadBalancer

Ingress for locust
```bash
kubectl apply -f - << EOF
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: locust
spec:
  tls:
    - hosts:
      - locust.k8s.shubhamtatvamasi.com
      secretName: letsencrypt
  rules:
    - host: locust.k8s.shubhamtatvamasi.com
      http:
        paths:
        - path: /
          backend:
            serviceName: locust
            servicePort: 8089
EOF
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
