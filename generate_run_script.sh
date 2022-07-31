#!/bin/sh

grep '\$' README.md | cut -f 2 -d "$" > run.sh
chmod +x run.sh
