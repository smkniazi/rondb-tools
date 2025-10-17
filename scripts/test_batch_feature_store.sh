#!/bin/bash

# Test script for batch_feature_store endpoint
# Usage: ./test_batch_feature_store.sh [batch_size]

BATCH_SIZE=${1:-512}
ENDPOINT="http://10.0.0.207:4406/0.1.0/batch_feature_store"

echo "Testing batch_feature_store with batch_size=$BATCH_SIZE"
echo "Endpoint: $ENDPOINT"
echo ""

curl -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -d "$(python3 -c "
import json
import random

entries = [{'id1': random.randint(1, 1000)} for _ in range($BATCH_SIZE)]
payload = {
    'featureStoreName': 'fsdb002',
    'featureViewName': 'sample_2',
    'featureViewVersion': 1,
    'passedFeatures': [],
    'entries': entries,
    'metadataOptions': None,
    'options': None
}
print(json.dumps(payload))
")"

echo ""
echo "Request completed"
