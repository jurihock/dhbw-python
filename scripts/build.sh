#!/bin/sh

pushd $(dirname $(dirname "$0"))
rm -rf dist
python3 -m build
popd
