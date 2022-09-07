import os

from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3_deployment

try:
    from aws_cdk import core as cdk
except ImportError:
    import aws_cdk as cdk

from chalice.cdk import Chalice


RUNTIME_SOURCE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), os.pardir, "runtime"
)
STATIC_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), os.pardir, "static"
)


class ChaliceApp(cdk.Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.s3_bucket = self._create_s3_bucket()
        self.chalice = Chalice(
            self,
            "ChaliceApp",
            source_dir=RUNTIME_SOURCE_DIR,
            stage_config={
                "environment_variables": {
                    "S3_BUCKET_NAME": self.s3_bucket.bucket_name,
                }
            },
        )
        self.s3_bucket.grant_read(self.chalice.get_role("DefaultRole"))
        self._deploy_static_assets()

    def _create_s3_bucket(self):
        bucket = s3.Bucket(
            self,
            "TheDailyQ",
            bucket_name="the-daily-q",
            website_redirect=s3.RedirectTarget(host_name="aws.amazon.com"),
            public_read_access=True,
        )
        cdk.CfnOutput(self, "S3BucketName", value=bucket.bucket_name)
        cdk.CfnOutput(self, "BucketDomain", value=bucket.bucket_website_domain_name)
        return bucket