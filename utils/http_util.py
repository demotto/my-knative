import requests
import os


def download_raw_file(url, loc):
    if not os.path.exists(loc) or os.path.isfile(loc):
        dest = loc
    else:
        parts = url.split("/")
        dest = loc + "/" + parts[-1]
    f = requests.get(url)
    with open(dest, "wb") as code:
        code.write(f.content)


if __name__ == "__main__":
    url = "https://github.com/knative/serving/releases/download/v0.10.0/serving.yaml"
    download_raw_file(url, "d:\\caocao")
