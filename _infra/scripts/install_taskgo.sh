#! /bin/bash

TASKGO_VERSION=v2.0.3
TASKGO_ZIPNAME=task_linux_amd64.tar.gz

echo install task executable completions
pushd /tmp
    rm -rf task_linux_amd64.tar.gz
    wget https://github.com/go-task/task/releases/download/${TASKGO_VERSION}/${TASKGO_ZIPNAME}
    tar xzvf ${TASKGO_ZIPNAME}
    mv task /bin/
    rm -rf task_linux_amd64.tar.gz
popd

echo install zsh completions
COMPLETIONS_DIR=/usr/local/share/zsh/site-functions/
mkdir -p "${COMPLETIONS_DIR}"
curl https://raw.githubusercontent.com/go-task/task/master/completion/zsh/_task \
-o "${COMPLETIONS_DIR}/_task"
