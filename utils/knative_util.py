


from pathlib import Path
import requests
import http_util
import os
import re

from os import sys, path
from importlib import reload
reload(sys)
sys.path.append(path.dirname(path.abspath(__file__)))
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from conf import env_conf
from utils import file_util
from utils import docker_util

def download_deployments():
    urls = env_conf.global_params['deploy_urls']
    deploy_dir = env_conf.root_dir + "/deploy/origin"
    Path(deploy_dir).mkdir(parents=True, exist_ok=True)
    for url in urls:
        http_util.download_raw_file(url, deploy_dir)


def scan_images():
    default_tag = env_conf.global_params["knative_version"]
    deploy_dir = env_conf.root_dir + "/deploy/origin"
    generated_dir = env_conf.root_dir + "/deploy/generated"
    Path(generated_dir).mkdir(parents=True, exist_ok=True)

    pattern = re.compile(r"(gcr\.io.*|k8s\.gcr\.io.*)")

    images = []
    for f in os.listdir(deploy_dir):
        if not f.endswith(".yaml"):
            continue
        content = file_util.read_str_file(deploy_dir + "/" + f)
        images += pattern.findall(content)

    mapping = []
    images = set(images)
    image_prefix = "{username}/mykubeflow.".format(username=env_conf.global_params['docker']['username'])
    for image in images:
        if "@sha256" in image:
            image_id = image.split("@sha256")[0]
            image_tag = default_tag
        else:
            parts = image.split(":")
            image_id = parts[0]
            image_tag = parts[1]
        new_image_addr = image_prefix + image_id.replace("/", ".").strip() + ":" + image_tag.strip()
        mapping.append({"from": image, "to": new_image_addr})
        record_path = env_conf.root_dir + "/deploy/records.yaml"
        file_util.write_yaml_file(mapping, record_path)


def make_new_deploy():
    mapping_file = env_conf.root_dir + "/deploy/records.yaml"
    mappings = file_util.read_yaml_file(mapping_file)

    di = {}
    for r in mappings:
        for pair in r:
            di[pair['from']] = pair['to']

    deploy_dir = env_conf.root_dir + "/deploy/origin"
    generated_dir = env_conf.root_dir + "/deploy/generated"
    for f in os.listdir(deploy_dir):
        if not f.endswith(".yaml"):
            continue
        content = file_util.read_str_file(deploy_dir + "/" + f)
        for key, value in di.items():
            content = content.replace(key, value)
        file_util.write_str_file(content, generated_dir + "/" + f)

    for r in mappings:
        for pair in r:
            print(pair)


def diy_docker_images():
    mapping_file = env_conf.root_dir + "/deploy/records.yaml"
    mappings = file_util.read_yaml_file(mapping_file)

    docker_util.login()

    for r in mappings:
        for pair in r:
            image = pair['from']
            new_image = pair['to']
            docker_util.image_pull_v2(image)
            docker_util.image_tag_v2(image, new_image)
            docker_util.image_push_v2(new_image)


if __name__ == '__main__':
    # download_deployments()
    # scan_images()
    # make_new_deploy()
    diy_docker_images()
