import os
from utils import docker_util
from conf import env_conf
import requests
import subprocess as commands

deploy_dir = env_conf.root_dir + "/deploy/generated"


def install_meta(prefix):
    parts = []
    for f in os.listdir(deploy_dir):
        parts.append("--filename " + deploy_dir + "/" + f)
    cmd = prefix + " ".join(parts)
    print(cmd)
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception(output)


def install_crd():
    install_meta("kubectl apply --selector knative.dev/crd-install=true ")


def install_fully():
    install_meta("kubectl apply ")


if __name__ == '__main__':
    install_crd()
    install_crd()
    install_fully()
