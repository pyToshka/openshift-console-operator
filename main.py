import base64
import logging
import os
from typing import Optional
import kopf
import yaml
from jinja2 import Environment, FileSystemLoader
from kopf import ConnectionInfo
from loguru import logger
import time

from helpers import destroy_ingress, destroy_service, destroy_deployment, destroy_secret
from helpers.create_objects import (
    create_secret,
    create_service,
    create_ingress,
    create_deployment,
)

root_directory = os.path.dirname(os.path.abspath(__file__))
path = root_directory + "/templates"
env = Environment(
    loader=FileSystemLoader(f"{path}"),
    trim_blocks=True,
    autoescape=True,
    lstrip_blocks=True,
)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


logging.basicConfig(handlers=[InterceptHandler()], level=0)


def rendering_deployment_template(
    namespace,
    name,
    grafana_public_url,
    oidc_id,
    console_base_url,
    oidc_issuer_url,
    oidc_secret,
    alert_manager_url,
    prometheus_url,
    image_url,
    cpu_limit,
    memory_limit,
    cpu_request,
    memory_request,
) -> str:
    logger.info(f"Preparing Deployment for OpenShift console in {namespace}")
    deployment_template = env.get_template("deployment.jinja2")
    deployment = deployment_template.render(
        namespace=namespace,
        name=name,
        grafana_public_url=grafana_public_url,
        oidc_id=oidc_id,
        console_base_url=console_base_url,
        oidc_issuer_url=oidc_issuer_url,
        oidc_secret=oidc_secret,
        alertmanager_url=alert_manager_url,
        prometheus_url=prometheus_url,
        image_url=image_url,
        cpu_limit=cpu_limit,
        memory_limit=memory_limit,
        cpu_request=cpu_request,
        memory_request=memory_request,
    )
    return deployment


def rendering_secret_template(namespace, name, oidc_secret) -> str:
    logger.info(f"Preparing Secret for OpenShift console in {namespace}")

    oidc_secret_encode = base64.b64encode(oidc_secret.encode())
    oidc_secret_encode_base64 = oidc_secret_encode.decode("ascii")

    secret_template = env.get_template("secret.jinja2")
    secret = secret_template.render(
        namespace=namespace, name=name, oidc_secret=oidc_secret_encode_base64
    )
    return secret


def rendering_service_template(namespace, name) -> str:
    logger.info(f"Preparing Service for OpenShift console in {namespace}")
    secret_template = env.get_template("service.jinja2")
    secret = secret_template.render(namespace=namespace, name=name)
    return secret


def rendering_ingress_template(namespace, name, domain_name) -> str:
    logger.info(f"Preparing Ingress for OpenShift console in {namespace}")
    secret_template = env.get_template("ingress.jinja2")
    secret = secret_template.render(
        namespace=namespace, name=name, domain_name=domain_name
    )
    return secret


@kopf.on.login()
def login_fn(**kwargs) -> Optional[ConnectionInfo]:
    return kopf.login_via_client(**kwargs)


@kopf.on.cleanup()
def cleanup_fn(logger, **kwargs) -> None:
    logger.info("Cleaning up in 3s...")
    time.sleep(3)


@kopf.on.create("openshift.io", "v1", "console")
def create_resources(spec, body, namespace, name, **kwargs) -> None:
    logger.info(f"Starting deployment process for OpenShift resources in {namespace}")
    oidc_id = spec["oidc_id"]
    oidc_issuer_url = spec["oidc_issuer_url"]
    oidc_secret = spec["oidc_secret"]
    console_base_url = spec["console_base_url"]
    grafana_public_url = spec["grafana_public_url"]
    alert_manager_url = spec["alert_manager_url"]
    prometheus_url = spec["prometheus_url"]
    image_url = spec["image_url"]
    cpu_limit = spec["cpu_limit"]
    memory_limit = spec["memory_limit"]
    cpu_request = spec["cpu_request"]
    memory_request = spec["memory_request"]
    try:
        domain_name = spec["domain_name"]
    except KeyError:
        domain_name = None
    try:
        enable_ingress = spec["enable_ingress"]
    except KeyError:
        enable_ingress = False
    generate_secret = rendering_secret_template(
        namespace=namespace, name=name, oidc_secret=oidc_secret
    )
    generate_deployment = rendering_deployment_template(
        namespace=namespace,
        name=name,
        grafana_public_url=grafana_public_url,
        oidc_id=oidc_id,
        console_base_url=console_base_url,
        oidc_issuer_url=oidc_issuer_url,
        oidc_secret=oidc_secret,
        alert_manager_url=alert_manager_url,
        prometheus_url=prometheus_url,
        image_url=image_url,
        cpu_limit=cpu_limit,
        memory_limit=memory_limit,
        cpu_request=cpu_request,
        memory_request=memory_request,
    )
    generate_service = rendering_service_template(namespace=namespace, name=name)

    secret = create_secret(yaml.safe_load(generate_secret))
    logger.info(
        f"Secret {secret} for Openshift Console has been created in {namespace}"
    )
    deployment = create_deployment(yaml.safe_load(generate_deployment))
    logger.info(
        f"Deployment {deployment} for Openshift Console has been created in {namespace}"
    )
    service = create_service(yaml.safe_load(generate_service))
    logger.info(f"Service {service} for Openshift has been created in {namespace}")
    if enable_ingress:
        generate_ingress = rendering_ingress_template(
            namespace=namespace, name=name, domain_name=domain_name
        )
        ingress = create_ingress(yaml.safe_load(generate_ingress))
        logger.info(f"Ingress {ingress} for Openshift has been created in {namespace}")


@kopf.on.delete("openshift.io", "v1", "console")
def delete(spec, body, namespace, name, **kwargs) -> None:
    logger.info(f"Starting termination process for OpenShift resources in {namespace}")
    oidc_id = spec["oidc_id"]
    oidc_issuer_url = spec["oidc_issuer_url"]
    oidc_secret = spec["oidc_secret"]
    console_base_url = spec["console_base_url"]
    grafana_public_url = spec["grafana_public_url"]
    alert_manager_url = spec["alert_manager_url"]
    prometheus_url = spec["prometheus_url"]
    image_url = spec["image_url"]
    cpu_limit = spec["cpu_limit"]
    memory_limit = spec["memory_limit"]
    cpu_request = spec["cpu_request"]
    memory_request = spec["memory_request"]
    domain_name = spec["domain_name"]
    enable_ingress = spec["enable_ingress"]
    generate_secret = rendering_secret_template(
        namespace=namespace, name=name, oidc_secret=oidc_secret
    )
    generate_deployment = rendering_deployment_template(
        namespace=namespace,
        name=name,
        grafana_public_url=grafana_public_url,
        oidc_id=oidc_id,
        console_base_url=console_base_url,
        oidc_issuer_url=oidc_issuer_url,
        oidc_secret=oidc_secret,
        alert_manager_url=alert_manager_url,
        prometheus_url=prometheus_url,
        image_url=image_url,
        cpu_limit=cpu_limit,
        memory_limit=memory_limit,
        cpu_request=cpu_request,
        memory_request=memory_request,
    )
    generate_service = rendering_service_template(namespace=namespace, name=name)
    if enable_ingress:
        generate_ingress = rendering_ingress_template(
            namespace=namespace, name=name, domain_name=domain_name
        )
        ingress = destroy_ingress(yaml.safe_load(generate_ingress))
        logger.info(f"Ingress {ingress} for Openshift has been deleted in {namespace}")

    service = destroy_service(yaml.safe_load(generate_service))
    logger.info(f"Service {service} for Openshift has been deleted in {namespace}")
    deployment = destroy_deployment(yaml.safe_load(generate_deployment))
    logger.info(
        f"Deployment {deployment} for Openshift Console has been deleted in {namespace}"
    )
    secret = destroy_secret(yaml.safe_load(generate_secret))
    logger.info(
        f"Secret {secret} for Openshift Console has been deleted in {namespace}"
    )
