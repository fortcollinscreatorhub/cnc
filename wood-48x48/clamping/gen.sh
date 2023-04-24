#!/bin/bash

for n in $(seq 2 5); do
    ~/git_wa/gcmc/src/gcmc \
        -i \
        -o straight-${n}.ngc \
        -Dmount_hole_count=${n} \
        straight.gcmc
done

for n in $(seq 2 5); do
    ~/git_wa/gcmc/src/gcmc \
        -i \
        -o corner-${n}.ngc \
        -Dmount_hole_count=${n} \
        corner.gcmc
done
