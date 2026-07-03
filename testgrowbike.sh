#!/bin/bash

process="https://bikebox.urbanfuturescollective.org/processes/growbike/execution"
curl -X POST $process -H "Content-Type: application/json" -H "Prefer: respond-async" -d @testgrowbike.json

# process variable indicates the process to run on localhost
# -H passes headers for content type and response type
# -d passes input data to the growbike process 
# (city name, projected coordinate reference system, and ranking method)