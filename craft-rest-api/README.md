# Execution Instructions

### Prerequisites

* `python >= 3.3.0`
* pip install py-healthcheck
* pip install flask

### Build Docker Image
```bash
docker image build -t country-name-to-country-code:v0.0.1 .
```

### Deploy app on local k8s cluster
```bash
kubectl apply -f getCountryCode.yaml
```

### Call following APIs
```bash
# converts country name to country code
curl http://localhost:5001/convert/Australia

# returns health of the service
curl http://localhost:5001/health

# check returns status of the api https://www.travel-advisory.info/api
curl http://localhost:5001/diag
```