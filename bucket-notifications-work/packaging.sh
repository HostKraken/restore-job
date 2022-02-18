#!/bin/bash
zip -jr restore-bucket.zip function.py build.sh requirements.txt
fission package delete --name=bucket-restore --force
fission package create --name=bucket-restore --sourcearchive=restore-bucket.zip --env=python-faximatic 
fission function delete --name restorefunction
fission function create --name restorefunction --pkg bucket-restore --entrypoint "function.main" --method POST --url /restorefunction --buildcmd "./build.sh"
