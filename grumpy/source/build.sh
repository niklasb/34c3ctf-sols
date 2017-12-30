#!/bin/bash
python2 make.py
stack setup
stack build --fast --no-strip --ghc-options="-ddump-cmm -ddump-simpl -ddump-stg -ddump-ds -ddump-asm -ddump-to-file"
