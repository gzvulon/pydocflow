#!/bin/bash --login

exec conda run -n  $(cat venv.name.txt) exec $@

