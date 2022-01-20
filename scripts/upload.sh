#!/bin/sh

pushd $(dirname $(dirname "$0"))
python3 -m twine upload dist/*
popd
