from flask import current_app
from flask import request
import json 
import re
import os
import boto3

def restore_site(key, domain, archive_type):
    current_app.logger.info("Restoring "+archive_type+" for site: "+domain )
    if archive_type == "database":
      current_app.logger.info("Do databasey things here")
    if archive_type == "uploads":
      current_app.logger.info("Do uploadey things here")

def delete_backup(key):
    # some code here to delete the file from the bucket
    aws_access_key=os.environ['aws_access_key']
    aws_secret_key=os.environ['aws_secret_key']
    s3 = boto3.client('s3',
                      endpoint_url="http://rook-ceph-rgw-objectkraken.rook-ceph.svc:80",
                      aws_access_key_id=aws_access_key,
                      aws_secret_access_key=aws_secret_key)
    s3.delete_object(Bucket='hostkraken-backup',Key=key)

def main():
    current_app.logger.info("S3 Bucket Object Created!")
    data = request.get_data()
    data_dict = json.loads(data)

    s3_key = data_dict['Records'][0]['s3']['object']['key']
    domain = s3_key.split('/')[0]
    archive = s3_key.split('/')[1]
    archive_type = "invalid"
    if re.match(".*uploads.*", archive):
      archive_type = "uploads" 
    if re.match(".*database.*", archive):
      archive_type = "database" 
    current_app.logger.info("Key: %s" % (s3_key) )
    current_app.logger.info("Domain: %s" % (domain))
    current_app.logger.info("Archive type: %s" % (archive_type))
    if "invalid" != archive_type:
      restore_site(s3_key,domain,archive_type)
      delete_backup(s3_key)
    else:
      current_app.logger.info("Invalid archive type. Doing nothing.")
      delete_backup(s3_key)
#    current_app.logger.info("\nBODY\n%s" % (request.get_data()))
    return "S3 Bucket Object Created!"  
