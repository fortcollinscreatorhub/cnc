#!/bin/sh

cd $(dirname "$0")
exec rsync -avzr --delete fcch@10.1.10.26:/home/fcch/linuxcnc/ ./linuxcnc/
