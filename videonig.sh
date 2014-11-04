'raspivid -t 0 -fps 15 -w 640 -h 480 -ex night  -o - |nc -l 9999 &
