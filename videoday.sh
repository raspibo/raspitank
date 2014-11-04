#!/bin/bash
raspivid -t 0 -fps 15 -w 640 -h 480 -ex antishake  -o - |nc -l 9999 &
