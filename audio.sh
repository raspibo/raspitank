#!/bin/bash
arecord -D hw:1,0 -f S16_LE | nc -l 9998
