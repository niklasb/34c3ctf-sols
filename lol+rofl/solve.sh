#!/bin/bash
for f in lol rofl; do
  sage solve.py flag-$f.txt.enc
done
