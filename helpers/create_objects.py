import kopf
import pykube

from .k8s_client import kubernetes_api, create_k8s_client

api = kubernetes_api()

k8s_client = create_k8s_client().CustomObjectsApi()
core_api = create_k8s_client().CoreV1Api()


def create_cm(template):
    kopf.adopt(template)
    cm = pykube.ConfigMap(api, template)
    cm.create()
    return cm


def create_secret(template):
    kopf.adopt(template)
    cert = pykube.Secret(api, template)
    cert.create()
    return cert


def create_service(template):
    kopf.adopt(template)
    service = pykube.Service(api, template)
    service.create()
    return service


def create_deployment(template):
    kopf.adopt(template)
    deployment = pykube.Deployment(api, template)
    deployment.create()
    return deployment


def create_st(template):
    kopf.adopt(template)
    st = pykube.StatefulSet(api, template)
    st.create()
    return st


def create_ds(template):
    kopf.adopt(template)
    ds = pykube.DaemonSet(api, template)
    ds.create()
    return ds


def create_cron(template):
    kopf.adopt(template)
    cron = pykube.CronJob(api, template)
    cron.create()
    return cron


def create_ingress(template):
    kopf.adopt(template)
    ingress = pykube.Ingress(api, template)
    ingress.create()
    return ingress
