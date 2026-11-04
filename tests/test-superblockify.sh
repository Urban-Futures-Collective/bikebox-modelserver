#!/bin/bash

process="localhost:5000/processes/superblockify/execution"
curl -X POST $process -H "Content-Type: application/json" -H "Prefer: respond-async" -d @./tests/test-superblockify.json

# process variable indicates the process to run on localhost
# -H passes headers for content type and response type
# -d passes input data to the superblockify process 
# (city name, unit, and approach)