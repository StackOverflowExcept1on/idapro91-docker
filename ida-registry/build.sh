#!/usr/bin/env bash
set -ex

mkdir -p build && cd build

cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=. ..

cmake --build .
cmake --install .
