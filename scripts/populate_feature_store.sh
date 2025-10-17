#!/usr/bin/env bash
source ./scripts/include.sh

set -x 
$mysql < ./scripts/feature_store.sql
