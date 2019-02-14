# -*- coding: utf-8 -*-
# Version: 0.1a1

import json
import logging
import os
import uuid

import boto3

from base64 import b64decode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ENCRYPTED_HOOK_URL = os.environ['kmsEncryptedHookUrl']
SLACK_CHANNEL = os.environ['slackChannel']
HOOK_URL = 'https://' + boto3.client('kms') \
        .decrypt(CiphertextBlob=b64decode(ENCRYPTED_HOOK_URL))['Plaintext'] \
        .decode('utf-8')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    confluence_url = 'http://www.korniichuk.com'
    cloudwatch_url = 'http://www.korniichuk.com'
    icon_url = 'https://raw.githubusercontent.com/korniichuk/' \
               'cloudwatch-alarm/master/img/amazon_cloudwatch_icon.png'
    metric ="""{
        "metrics": [[
            "LogMetrics",
            "MetricName",
            {"period": 3600, "stat": "Sum"}]],
        "title": "Title",
        "start": "-P1D",
        "end": "P0D",
        "timezone": "+0100"}"""
    bucket_name = 'examplebucket' # for temporary public file
    filename = 'tmp/cloudwatch_metric_chart_%s.png' % uuid.uuid4()

    # Get MetricWidgetImage from CloudWatch Metrics
    response = boto3.client('cloudwatch') \
                    .get_metric_widget_image(MetricWidget=metric)
    data = response['MetricWidgetImage']
    # Create temporary public file on S3
    boto3.client('s3').put_object(ACL='public-read', Body=data,
                                  Bucket=bucket_name, Key=filename)
    # Get URL of piblic file on S3
    response = boto3.client('s3').get_bucket_location(Bucket=bucket_name)
    bucket_location = response['LocationConstraint']
    image_url = 'https://s3-{0}.amazonaws.com/{1}/{2}'.format(
            bucket_location, bucket_name, filename)
    logger.info('Event: ' + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info('Message: ' + str(message))
    alarm_name = message['AlarmName']
    reason = message['NewStateReason']
    attachments = [{
        'title': 'Reason :fire:',
        'text': reason,
        'color': 'danger',
        'fields': [
            {
            'title': 'Confluence',
            'value': confluence_url,
            'short': True},
            {
            'title': 'CloudWatch',
            'value': cloudwatch_url,
            'short': True}],
        'image_url': image_url}]
    slack_message = {
        'channel': SLACK_CHANNEL,
        'username': 'Amazon CloudWatch',
        'icon_url': icon_url,
        'text': '`%s`' % alarm_name,
        'attachments': attachments}

    req = Request(HOOK_URL, json.dumps(slack_message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info('Message posted to %s', slack_message['channel'])
    except HTTPError as e:
        logger.error('Request failed: %d %s', e.code, e.reason)
    except URLError as e:
        logger.error('Server connection failed: %s', e.reason)
