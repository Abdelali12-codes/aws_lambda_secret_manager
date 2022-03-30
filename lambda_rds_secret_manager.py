import sys
import logging
import mysql.connector
import rds_config_secret

#rds settings
RDS_HOSTNAME = rds_config_secret.RDS_HOSTNAME
RDS_DB = rds_config_secret.RDS_DB
RDS_USERNAME = rds_config_secret.RDS_USERNAME
RDS_PASSWD = rds_config_secret.RDS_PASSWD


print(RDS_HOSTNAME)



logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = mysql.connector.connect(host=RDS_HOSTNAME, user=RDS_USERNAME, passwd=RDS_PASSWD, db=RDS_DB)
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))
    logger.error(err)
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
