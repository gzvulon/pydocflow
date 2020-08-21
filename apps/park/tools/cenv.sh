#!/bin/bash # no --login
### @@@DOC@@@ ###
# Usage:
#   - ./cenv.sh python file.py # run python script with venv
#   - $(./cenv bash) # enter interactive environment
### @@@/DOC@@@ ###

set -e
# set -x

VENV_NAME=$(cat venv.name.txt)
IS_INSIDE=$(which python | grep ${VENV_NAME} 2>&1 > /dev/null && echo 1 || echo 0 )


if [[ "$1" == "bash" ]] && [[ "$2" == "" ]];then
    echo conda activate ${VENV_NAME}
else
    if [[ "${IS_INSIDE}" == "1" ]]; then
        echo "already activated. runing here"
        exec "$@"
    else
        echo "run in environment"
        conda run -n ${VENV_NAME} "$@"
    fi
fi


