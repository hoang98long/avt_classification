#!/bin/bash

CONFIG_FILE=$1

# shellcheck disable=SC2164
cd /home/avt/github/avt_classification
conda activate avt_classify
python main.py --config_file "$CONFIG_FILE"
