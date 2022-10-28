import os

import kubernetes
import pykube


def kubernetes_api():
    try:
        config = pykube.KubeConfig.from_service_account()
    except FileNotFoundError:
        config = pykube.KubeConfig.from_file(os.getenv("KUBECONFIG", "~/.kube/config"))
    api = pykube.HTTPClient(config)
    return api


def create_k8s_client():
    try:
        kubernetes.config.load_incluster_config()
    except Exception:
        kubernetes.config.load_kube_config()
    kubernetes.client.configuration.assert_hostname = False
    return kubernetes.client
