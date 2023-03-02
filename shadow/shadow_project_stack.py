from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_iam as iam,
    triggers,
    Aws
)
from constructs import Construct

class ShadowProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here role arn:aws:iam::656930376886:role/lambda-vpc-sqs-role

        # example resource
        # queue = sqs.Queue(
        #     self, "ShadowProjectQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
    # bucket_name = f"sql-lambda-config-{Aws.ACCOUNT_ID}-{Aws.REGION}"
    # lambda_bucket = s3.Bucket('self', 'sqllambda', 
    #                           bucket_name= bucket_name,
    #                           encryption=s3.BucketEncryption.KMS_MANAGED)

        sql_r1 = s3.Bucket.from_bucket_name(self, "ZipBucket", "rds-lambda-test-jofrajim")  
        

        d_vpc = ec2.Vpc.from_lookup(self, "defaultvpc", vpc_id='vpc-0cec27832e5ba2135' )
        trigger_role = iam.Role.from_role_arn(self, "Role",
                                     "arn:aws:iam::656930376886:role/lambda-vpc-sqs-role" 
        )
        sg = ec2.SecurityGroup.from_lookup_by_id(self, "SG",
                                                 "sg-0c847e5678fc12642")
        r1_fn = triggers.TriggerFunction(
            self, "r1_fn", 
            runtime =_lambda.Runtime.PYTHON_3_9,
            handler = "lambda_function.lambda_handler",
            code=_lambda.Code.from_bucket(
                bucket=sql_r1,
                key='lambda_function.zip'
            ),
            vpc=d_vpc,
            vpc_subnets= ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC),
            allow_public_subnet=True,
            role=trigger_role,
            security_groups=[sg]
        )

       

         

