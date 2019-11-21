import subprocess as commands
import os

from os import sys, path
from importlib import reload
reload(sys)
sys.path.append(path.dirname(path.abspath(__file__)))
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from conf import env_conf


def login():
    """docker login"""
    username = env_conf.global_params['docker']['username']
    password = env_conf.global_params['docker']['password']
    cmd = "docker login -u {username} -p {password}".format(username=username, password=password)
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception(output)


def logout():
    pass


def image_exists(id, tag):
    cmd = "docker images | grep {id} | grep {tag}".format(id=id, tag=tag)
    print(cmd)
    (status, output) = commands.getstatusoutput(cmd)
    return status == 0


def image_pull(id, tag):
    cmd = "docker pull {id}:{tag}".format(id=id, tag=tag)
    print(cmd)
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception(output)
    print(output)


def image_pull_v2(image):
    cmd = "docker pull {image}".format(image=image)
    print(cmd)
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception(output)
    print(output)


def image_tag_v2(image, new_image):
    cmd = "docker tag {image} {new_image}".format(
        image=image,
        new_image=new_image
    )
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception(output)
    print(output)


def image_tag(id, tag, new_id, new_tag):
    cmd = "docker tag {id}:{tag} {new_id}:{new_tag}".format(
        id=id,
        tag=tag,
        new_id=new_id,
        new_tag=new_tag
    )
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception(output)
    print(output)


def image_push(id, tag):
    cmd = "docker push {id}:{tag}".format(id=id, tag=tag)
    print(cmd)
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception(output)
    print(output)


def image_push_v2(image):
    cmd = "docker push {image}".format(image=image)
    print(cmd)
    (status, output) = commands.getstatusoutput(cmd)
    if status != 0:
        raise Exception(output)
    print(output)


if __name__ == '__main__':
    login()
    tag1 = image_exists("aaa", "bb")
    tag2 = image_exists("k8s.gcr.io/etcd", "3.3.10")
    print(tag1, tag2)
    image_pull("k8s.gcr.io/etcd", "3.3.10")
