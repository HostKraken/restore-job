#!/bin/bash
echo "Generating job config"
export SITE_NAME=$1
export SITE_NAME_HYPHEN=`echo $SITE_NAME|tr '.' '-'`
export RESTOREPOINT=$2
envsubst <restorejob.yml >do_restore.yml
cat do_restore.yml

kubectl apply -n wordpress -f do_restore.yml

rm do_restore.yml
