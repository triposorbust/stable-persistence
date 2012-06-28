#!/bin/bash

shopt -s nullglob

for f in ./data/*.data
do
    echo "processing $f file..."
    ./main.py $f # > "$f.results"
done

# mv ./data/*.results ./results/