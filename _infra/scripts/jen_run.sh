#!/usr/bin/env bash
set -x
set -e
BASE_DIR=$(dirname $(realpath $0))
ROOT_DIR
JSON='{"parameter": [{"name": "param1", "value": "value1"},{"name":"fileParam", "file":"file0"}]}'
JOB_FULLNAME=INFRA/job/JobConfig
TOKEN=MYTOKEN1

TRIGGER_URL=https://jenkins.uveye.xyz/job/${JOB_FULLNAME}/buildWithParameters?token=${TOKEN}

curl -v ${TRIGGER_URL} -F file0=@fname -F json="${JSON}" --user builduseruveye:$(cat ~/ppp/_p_jenkins)
