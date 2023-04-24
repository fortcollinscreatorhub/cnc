The design is created using GCMC:
https://www.vagrearg.org/content/gcmc

TBH, GCMC could easily be re-written as a Python module, without too many
changes to the design file.

To simulate with LinuxCNC:
```shell
~swarren/git_wa/linuxcnc/scripts/linuxcnc \
    /home/swarren/git_wa/linuxcnc/configs/sim/axis/axis.ini
```
