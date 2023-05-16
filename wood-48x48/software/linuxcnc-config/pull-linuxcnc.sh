#!/bin/sh

cd $(dirname "$0")
exec rsync -avzr --delete fcch@10.1.10.110:/home/fcch/linuxcnc/ ./linuxcnc/
