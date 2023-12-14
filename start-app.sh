#!/bin/bash

nohup jupyter notebook --ip=* --NotebookApp.token='' --NotebookApp.password='' --no-browser --allow-root </dev/null >/dev/null 2>&1 &

python3 view.py
