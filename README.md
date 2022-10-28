# OpenShift Console operator for Kubernetes

Experimental Kubernetes operator for deployment [OpenShift console ](https://github.com/openshift/console)





## Schema
| Name |  Description    | Type     | Default | Required |
| ---- | ---- | ---- | ---- | ---- |
| `oidc_id` | The OIDC/OAuth2 Client ID | String | `None` | `yes` |
| `oidc_issuer_url` | The OIDC/OAuth2 issuer URL | String | `None` | `yes` |
| `oidc_secret` | The OIDC/OAuth2 Client Secret | String | `None` | `yes` |
| `image_url` | The Docker image for OpenShift console deployment | String | `quay.io/openshift/origin-console:4.9.0` | `no` |
| `console_base_url` | OpenShift Console base url | | `None` | |
| `grafana_public_url` | Public URL of the cluster's Grafana server | String | `None` | `yes` |
| `prometheus_ur`l | Public URL of the cluster's Prometheus server | String | `http://prometheus-k8s.monitoring:9090` | `yes` |
| alert_manager_url | `Public URL of the cluster's AlertManager server` | String | `http://alertmanager-main.monitoring:9093` | `yes` |
| `cpu_limit` | Cpu limit for OpenShift container | String | `500m` | `no` |
| `memory_limit` | Memory limits of the Openshift console container | String | `256Mi` | `no` |
| `cpu_request` | Cpu request of the OpenShift console container | String | `500m` | `no` |
| `memory_request` | Memory request for Openshift console container | String | `256Mi` | `no` |
| `domain_name` | Domain name for ingress, using only if enable_ingress true | String | `None` | `no` |
| `enable_ingress` | Create ingress for OpneShift console, ingress will be created only if true | Boolean | `false` | `no` |

## Deployment

Checkout repository and change directory to ` openshift-console-operator`

Apply Kubernetes manifests

```shell
kubectl delete -f deployment
```

## Build docker image

```shell
docker build . -t image:tag
```
