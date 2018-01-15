#!/bin/sh
exec docker run -it --rm -p 127.0.0.1:1342:80 --name superblog niklasb/superblog
