#!/bin/bash
set -eux
if ! command -v xsv &>/dev/null; then
    echo "xsv could not be found, installing..."
    cargo install xsv
fi

xsv cat rows $(find output/fix -type f -name cody-bench.csv) >fix.csv
xsv cat rows $(find output/chat -type f -name cody-bench.csv) >chat.csv
xsv cat rows $(find output/chat_context -type f -name cody-bench.csv) >chat_context.csv
