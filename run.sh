#!/bin/bash
DATETIME=`date +%y%m%d-%H_%M_%S`
SRC=$BUCKET
for i in $(/vault/vault-env env | grep DATABASE); do export $i; done
export RESTOREDATE=$RESTOREPOINT

echo "Beginning restore for $SITE_NAME at $DATETIME"
echo "Retrieving backups from restore point at $RESTOREDATE"

export DATABASE_FILE=`/vault/vault-env s3cmd -c /root/.s3cfg ls s3://$SRC/$SITE_NAME/ | grep database | grep "$RESTOREDATE" | awk '{print $4}'`
export UPLOADS_FILE=`/vault/vault-env s3cmd -c /root/.s3cfg ls s3://$SRC/$SITE_NAME/ | grep uploads | grep "$RESTOREDATE" | awk '{print $4}'`

/vault/vault-env s3cmd -c /root/.s3cfg get $DATABASE_FILE
/vault/vault-env s3cmd -c /root/.s3cfg get $UPLOADS_FILE

export DATABASE_RESTORE_FILE=`ls | grep database`
export UPLOADS_RESTORE_FILE=`ls | grep uploads`
gunzip $DATABASE_RESTORE_FILE
export DATABASE_SQL_FILE=`ls | grep .sql | grep -v gz`


echo "Restoring $DATABASE_FILE to database $DATABASE_NAME"
mysql -h $DATABASE_HOST -u$DATABASE_USER -p$DATABASE_PASS $DATABASE_NAME <$DATABASE_SQL_FILE
echo "Database restored."

echo "Restoring $UPLOADS_FILE to domain $SITE_NAME"
tar xzvf $UPLOADS_RESTORE_FILE --strip-components=4 -C /content
echo "Uploads for $SITE_NAME restored."

echo 'Done!'

#sleep 3;
done
