#!/bin/bash

process="localhost:5000/processes/linkbike/execution"
curl -X POST $process -H "Content-Type: application/json" -H "Prefer: respond-async" -d @./tests/test-linkbike.json

# process variable indicates the process to run on localhost
# -H passes headers for content type and response type
# -d passes input data to the linkbike process 
# (city query & link strategy)