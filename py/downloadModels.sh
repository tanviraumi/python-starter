#!/bin/bash

if [ $# -eq 0 ]; then
    echo "data directory required"
    exit 1
fi

DATA_DIR=$1

if [ ! -f $DATA_DIR/lid.176.bin ]; then
    wget -P $DATA_DIR -nv --show-progress --progress=bar:force:noscroll https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
fi

if [ ! -f $DATA_DIR/en_core_web_lg-3.0.0-py3-none-any.whl ]; then
    wget -P $DATA_DIR -nv --show-progress --progress=bar:force:noscroll https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.0.0/en_core_web_lg-3.0.0-py3-none-any.whl
fi