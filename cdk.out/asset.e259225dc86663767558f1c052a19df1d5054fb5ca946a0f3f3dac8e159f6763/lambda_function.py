import sys
import logging
import pymysql
import json
import boto3
from botocore.exceptions import ClientError

#rds settings
# rds_host  = "mysqlforlambda.cicbsfmpxiqr.us-east-2.rds.amazonaws.com"
# user_name = "admin"
# password = "t3st1ng123"
# db_name = "ExampleDB"
secret_name = "test/mysql-lambda"
region_name = "us-east-2"
#--------
# Create a Secrets Manager client
print("gettin secret manager session")
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name=region_name
)
try:
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
except ClientError as e:
    # For a list of exceptions thrown, see
    # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    raise e
secrets = json.loads(get_secret_value_response['SecretString'])
print(secrets)
rds_host  = secrets["host"]
user_name = secrets["username"]
password = secrets['password']
db_name = secrets['dbname']
#-------
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# create the database connection outside of the handler to allow connections to be
# re-used by subsequent function invocations. mysql -h mysqlforlambda.cicbsfmpxiqr.us-east-2.rds.amazonaws.com -P 3306 -u admin -p
try:
    conn = pymysql.connect(host=rds_host, user=user_name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

def lambda_handler(event, context):
    """
    This function creates a new RDS database table and writes records to it
    """
    #message = event['Records'][0]['body']
    #data = json.loads(message)
    print("starting handler")
    CustID = '1017'
    Name = 'Pedro'

    item_count = 0
    sql_string = f"insert into Customer (CustID, Name) values({CustID}, '{Name}')"

    with conn.cursor() as cur:
        cur.execute("create table if not exists Customer ( CustID  int NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (CustID))")
        cur.execute(sql_string)
        conn.commit()
        cur.execute("select * from Customer")
        logger.info("The following items have been added to the database:")
        for row in cur:
            item_count += 1
            logger.info(row)
    conn.commit()

    return "Added %d items to RDS MySQL table" %(item_count)