import sys
import logging
import mysql.connector
import os
import boto3
from base64 import b64decode

#rds settings
RDS_HOSTNAME = os.environ['RDS_HOSTNAME']
RDS_DB = os.environ['RDS_DB']
RDS_USERNAME = os.environ['RDS_USERNAME']
RDS_PASSWD = os.environ['RDS_PASSWD']

# Decrypt code should run once and variables stored outside of the function
# handler so that these are decrypted once per container



print(RDS_PASSWD)

try:
    DECRYPTED = boto3.client('kms').decrypt(
       CiphertextBlob=b64decode(RDS_PASSWD),
       EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
    )['Plaintext'].decode('utf-8')
except ERROR as er:
    print(er)

print(DECRYPTED)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = mysql.connector.connect(host=RDS_HOSTNAME, user=RDS_USERNAME, passwd=DECRYPTED, db=RDS_DB)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def handler(event, context):
    """
    This function fetches content from MySQL RDS instance
    """

    item_count = 0

    with conn.cursor() as cur:
        cur.execute("drop table if exists Employee")
        cur.execute("create table Employee ( EmpID  int NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (EmpID))")
        cur.execute('insert into Employee (EmpID, Name) values(1, "Joe")')
        cur.execute('insert into Employee (EmpID, Name) values(2, "Bob")')
        cur.execute('insert into Employee (EmpID, Name) values(3, "Mary")')
        conn.commit()
        cur.execute("select * from Employee")
        for row in cur:
            item_count += 1
            logger.info(row)
            #print(row)
    conn.commit()

    return "Added %d items from RDS MySQL table" %(item_count)
