# cloudwatch-alarm
**Name:** cloudwatch-alarm<br>
**Description:** Amazon CloudWatch Alarm 2.0. CloudWatch to Slack smart notification<br>
**GitHub:** https://github.com/korniichuk/cloudwatch-alarm

## Table of Contents
* **[Introduction](#introduction)**
  * **[Amazon CloudWatch Alarm 2.0](#amazon-cloudwatch-alarm-20)**
  * **[Standard Amazon CloudWatch Alarm](#standard-amazon-cloudWatch-alarm)**
* **[How it works](#how-it-works)**
* **[Requirements](#requirements)**
* **[Python lib versions](#python-lib-versions)**
* **[Create Slack webhook](#create-slack-webhook)**
* **[Create Amazon SNS topic](#create-amazon-sns-topic)**
* **[Create Amazon S3 bucket](#create-amazon-s3-bucket)**

## Introduction
### Amazon CloudWatch Alarm 2.0
![amazon_cloudwatch_alarm_smart.png](img/amazon_cloudwatch_alarm_smart.png "Amazon CloudWatch Alarm 2.0")

### Standard Amazon CloudWatch Alarm
![amazon_cloudwatch_alarm_standard.png](img/amazon_cloudwatch_alarm_standard.png "Standard Amazon CloudWatch Alarm")

## How it works
![how_it_works.jpg](img/how_it_works.jpg "How it works")

## Requirements
Please, install Python packages:
```
$ sudo pip install -t . -r requirements.txt
```

## Python lib versions
* [boto3](https://pypi.org/project/boto3/) ver. 1.9.41
* [botocore](https://pypi.org/project/botocore/) ver. 1.12.41

## Create Slack webhook
Navigate to https://`<your-team-domain>`.slack.com/apps, like https://example.slack.com/apps. Search for and select `Incoming WebHooks`. Click `Add Configuration` button:

![slack_-_add_configuration.png](img/slack_-_add_configuration.png "Create Slack webhook. Add Configuration")

Choose the default channel where messages will be sent (like `#example`) and click `Add Incoming WebHooks Integration`. Copy and save the webhook URL (like https://hooks.slack.com/services/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) from the setup instructions.

**Note:** You need admin rights to your Slack.

## Create Amazon SNS topic
Create new [Amazon SNS](https://aws.amazon.com/sns/) topic: https://docs.aws.amazon.com/sns/latest/dg/sns-getting-started.html#CreateTopic. Like `example` topic with `arn:aws:sns:eu-west-1:539199393808:example` ARN.

![sns_-_topic_details.png](img/sns_-_topic_details.png "Create Amazon SNS topic. Topic details")

## Create Amazon S3 bucket
Create new Amazon S3 Bucket (e.g. `examplebucket`). Create new lifecyle rule for bucket (e.g. `DeleteTmpAfter72h`) with `tmp/` prefix filter:

![s3_-_lifecycle_rule.png](img/s3_-_lifecycle_rule.png "Create Amazon S3 bucket. Lifecycle rule")

Configure expiration as below. Expire after 3 days. Permanently delete after 3 days. Clean up incomplete multipart uploads after 1 day.

![s3_-_configure_expiration](img/s3_-_configure_expiration.png "Create Amazon S3 bucket. Configure expiration")
