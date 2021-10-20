#!/bin/bash
zip -jr restore-bucket.zip function.py
fission package delete --name=bucket-restore --force
fission package create --name=bucket-restore --sourcearchive=restore-bucket.zip --env=python-faximatic
fission function update --name restorefunction --pkg bucket-restore --entrypoint "function.main"
