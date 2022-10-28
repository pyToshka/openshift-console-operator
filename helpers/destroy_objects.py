import kopf
import pykube

from .k8s_client import kubernetes_api, create_k8s_client

api = kubernetes_api()

k8s_client = create_k8s_client().CustomObjectsApi()
core_api = create_k8s_client().CoreV1Api()


def destroy_cm(template):
    kopf.adopt(template)
    cm = pykube.ConfigMap(api, template)
    cm.delete()
    return cm


def destroy_secret(template):
    kopf.adopt(template)
    cert = pykube.Secret(api, template)
    cert.delete()
    return cert


def destroy_service(template):
    kopf.adopt(template)
    service = pykube.Service(api, template)
    service.delete()
    return service


def destroy_deployment(template):
    kopf.adopt(template)
    deployment = pykube.Deployment(api, template)
    deployment.delete()
    return deployment


def destroy_st(template):
    kopf.adopt(template)
    st = pykube.StatefulSet(api, template)
    st.delete()
    return st


def destroy_ds(template):
    kopf.adopt(template)
    ds = pykube.DaemonSet(api, template)
    ds.delete()
    return ds


def destroy_cron(template):
    kopf.adopt(template)
    cron = pykube.CronJob(api, template)
    cron.delete()
    return cron


def destroy_ingress(template):
    kopf.adopt(template)
    ingress = pykube.Ingress(api, template)
    ingress.delete()
    return ingress
