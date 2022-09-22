#!/bin/sh

grep '\$' README.md | sed "s/$ //g" | cut -f 2  > run.sh
chmod +x run.sh
