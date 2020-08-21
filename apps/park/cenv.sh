#!/usr/bin/env bash

conda activate $(cat venv.name.txt)

exec $@