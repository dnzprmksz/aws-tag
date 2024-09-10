from src.core.aws.api_gateway import ApiGateway
from src.core.aws.base_aws_service import BaseAwsService
from src.core.aws.cloudwatch_logs import CloudWatchLogs
from src.core.aws.dynamodb import DynamoDB
from src.core.aws.ec2 import EC2
from src.core.aws.ecr import ECR
from src.core.aws.ecs import ECS
from src.core.aws.elastic_block_store import ElasticBlockStore
from src.core.aws.elasticache import ElastiCache
from src.core.aws.elb import ELB
from src.core.aws.elbv2 import ELBv2
from src.core.aws.kinesis_data_analytics import KinesisDataAnalytics
from src.core.aws.kinesis_data_firehose import KinesisDataFirehose
from src.core.aws.kinesis_data_streams import KinesisDataStreams
from src.core.aws.kms import KMS
from src.core.aws.lambda_function import Lambda
from src.core.aws.rds import RDS
from src.core.aws.s3 import S3
from src.core.aws.sns import SNS
from src.core.aws.sqs import SQS


class ServiceFactory:
    __services = [
        KinesisDataStreams(),
        KinesisDataFirehose(),
        KinesisDataAnalytics(),
        ApiGateway(),
        SQS(),
        EC2(),
        S3(),
        Lambda(),
        RDS(),
        KMS(),
        CloudWatchLogs(),
        DynamoDB(),
        ElastiCache(),
        ElasticBlockStore(),
        SNS(),
        ECR(),
        ECS(),
        ELB(),
        ELBv2(),
    ]

    services = {service.short_name: service for service in __services}

    def get_service(self, service_name: str) -> BaseAwsService:
        """
        Get the service class for the given service name.

        :param service_name: Service name.
        :return: Service class.
        """
        if service_name in self.services:
            return self.services[service_name]
        else:
            raise ValueError(f'Service not found: {service_name}')
