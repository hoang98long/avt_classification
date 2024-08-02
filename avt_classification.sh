#!/bin/bash

CONFIG_FILE=$1

cd /home/avt/github/avt_classification
conda activate avt_classify
python main.py "$CONFIG_FILE"
