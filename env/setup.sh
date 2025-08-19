#!/bin/bash

ENV_NAME="yolov8-bone"
ENV_FILE="environment.yml"


if ! command -v conda &> /dev/null; then
    echo "Conda not found. Make sure Anaconda / Miniconda is installed properly"
    exit 1
fi


if conda info --envs | grep -qE "^$ENV_NAME\s"; then
    echo "Environment '$ENV_NAME' exist. Activating..."
else
    echo "Environment '$ENV_NAME' not exist. Creating from '$ENV_FILE'..."
    if [ ! -f "$ENV_FILE" ]; then
        echo "File environment.yml not found"
        exit 1
    fi
    conda env create -f "$ENV_FILE"
    if [ $? -ne 0 ]; then
        echo "Fail to create environment."
        exit 1
    fi
fi

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"