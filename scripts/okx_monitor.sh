#!/bin/bash
# Fetch OKX BTC price via GitHub Actions
BTC_PRICE=$(gh run view $(gh run list --workflow=fetch-okx.yml --limit=1 --json databaseId --jq '.[0].databaseId') --log 2>/dev/null | grep '"740' | tail -1)
echo "BTC: $BTC_PRICE"
