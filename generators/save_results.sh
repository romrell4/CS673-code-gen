#!/bin/bash
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 school_name" >&2
  exit 1
fi
current_time=$(date "+%Y.%m.%d-%H.%M.%S")
mkdir -p ~/results/$1_$current_time
cp results/$1/* ~/results/$1_$current_time
cp index.html ~/results/$1_$current_time
