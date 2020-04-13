FROM python:3.6
# !!![type=deps:linux]
RUN apt update && apt install -y \
    curl \ 
    wget \
    git

# !!![type=task][cmd=task:install-poetry]
RUN curl -sSL \
    https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
    | python

# !!![type=test][cmd=poetry --version]
ENV PATH="/root/.poetry/bin:${PATH}"
# RUN realpath ~/.poetry/bin
# RUN chmod +x ${HOME}/.poetry/bin/poetry
# RUN echo $PATH
RUN poetry --version

# !!![type=sh][cmd=install_task.sh]
RUN cd /usr && curl -sL https://taskfile.dev/install.sh | sh
# !!![type=test][cmd=poetry --version]
RUN task --version

