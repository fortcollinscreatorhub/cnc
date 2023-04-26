#!/bin/bash

cd $(dirname "$0")

for n in $(seq 2 5); do
    ./straight.py "${n}" > "straight-${n}.ngc"
done

for n in $(seq 2 5); do
    ./corner.py "${n}" > "corner-${n}.ngc"
done
