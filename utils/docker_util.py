import subprocess

from conf import env_conf

def login():
    """docker login"""
    username = env_conf.global_params['docker']['username']
    password = env_conf.global_params['docker']['password']
    print(username)
    # cmd = "docker login -u {username} -p {password}".format(username=username, password=password)
    # (status, output) = commands.getstatusoutput(cmd)
    # if status != 0:
    #     raise Exception(output)


if __name__ == '__main__':
    login()

