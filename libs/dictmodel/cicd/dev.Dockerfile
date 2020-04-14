FROM python:3.6
# !!![type=deps:linux]
RUN apt update && apt install -y \
    curl \
    wget \
    git \
    sudo


# !!![type=deps:linux-docker]
RUN apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common


RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

RUN apt-get remove docker docker-engine docker.io containerd runc || true

RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"

RUN apt-get update && apt-get install -y docker-ce docker-ce-cli

# !!![type=task][cmd=task:install-poetry]
RUN curl -sSL \
    https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
    | python

# !!![type=test][cmd=poetry --version]
ENV PATH="/root/.poetry/bin:${PATH}"
# RUN chmod +x ${HOME}/.poetry/bin/poetry
RUN poetry --version

# !!![type=sh][cmd=install_task.sh]
RUN cd /usr && curl -sL https://taskfile.dev/install.sh | sh

# !!![type=test][cmd=poetry --version]
RUN task --version

# !!![type=pip][cmd=install-pip-prod]
RUN pip install ruamel.yaml fire
# !!![type=pip][cmd=install-pip-dev]
RUN pip install pytest

# RUN mkdir /src
# VOLUME [ "/src" ]
# WORKDIR /src
# https://jenkins.io/doc/book/pipeline/syntax/
# sudo apt update
# sudo apt install openjdk-8-jdk openjdk-8-jre