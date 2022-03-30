

import boto3
import os

from base64 import b64decode

RDS_HOSTNAME = os.environ['RDS_HOSTNAME']
RDS_DB = os.environ['RDS_DB']
RDS_USERNAME = os.environ['RDS_USERNAME']
RDS_PASSWD = os.environ['RDS_PASSWD']

# Decrypt code should run once and variables stored outside of the function
# handler so that these are decrypted once per container
DECRYPTED = boto3.client('kms').decrypt(
    CiphertextBlob=b64decode(RDS_PASSWD),
    EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
)['Plaintext'].decode('utf-8')

print(DECRYPTED)
