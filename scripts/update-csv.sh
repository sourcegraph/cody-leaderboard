#!/bin/bash
set -eux
if ! command -v xsv &>/dev/null; then
    echo "xsv could not be found, installing..."
    cargo install xsv
fi

for task in fix chat chat-context unit-test; do
    xsv cat rows $(find "output/$task" -type f -name cody-bench.csv) >"$task.csv"
done
