# locust


### Deploy on Kubernetes

Add helm repo and update
```bash
helm repo add deliveryhero https://charts.deliveryhero.io/

helm repo update
```

Install locust:
```bash
helm install locust deliveryhero/locust \
  --set service.type=NodePort
```

Update NodePort
```bash
kubectl patch svc locust \
  --patch='{"spec": {"ports": [{"name": "master-p3", "nodePort": 30089, "port": 8089}]}}'
```

http://k8s.shubhamtatvamasi.com:30089
