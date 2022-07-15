import os
import boto3
from chalice import Chalice


app = Chalice(app_name='the-daily-q')
s3 = boto3.resource('s3')
s3_bucket = s3.Bucket(os.environ.get('S3_BUCKET_NAME', ''))

@app.route('/questions', methods=['GET'])
def get_questions():
    questions = ["https://the-daily-q.s3.eu-west-2.amazonaws.com/" + q.key for q in s3_bucket.objects.all()]

    return questions