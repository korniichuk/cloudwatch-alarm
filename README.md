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
* **[Create Amazon CloudWatch Alarm](#create-amazon-cloudWatch-alarm)**
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

## Create Amazon CloudWatch Alarm
Navigate to https://console.aws.amazon.com/cloudwatch/ and create new Amazon CloudWatch Alarm. Click `Select metric` button:

![cloudwatch_-_select_metric.png](img/cloudwatch_-_select_metric.png "Create Amazon CloudWatch Alarm. Select metric")

Select metric, like `EC2 -> Per-Instance Metrics -> CPUUtilization`:

![cloudwatch_-_cpuutilization.png](img/cloudwatch_-_cpuutilization.png "Create Amazon CloudWatch Alarm. CPUUtilization")

Choose `Source` tab and select `Image API` checkbox. Copy and save json code. Click `Select metric` button:

![cloudwatch_-_image_api.png](img/cloudwatch_-_image_api.png "Create Amazon CloudWatch Alarm. Image API")

Saved json code example:
```
{
    "metrics": [
        [ "AWS/EC2", "CPUUtilization", "InstanceId", "i-0d91fdf2dbb765977" ]
    ],
    "start": "-PT3H",
    "end": "P0D",
    "timezone": "+0100"
}
```

Set up `Alarm details`. Enter `Name` (e.g. `CPUUtilization`) and `Description` (e.g. `The percentage of CPU utilization`). Specify the alarm condition. For example: select `>=`, enter `80`, and enter `3` datapoints.

![cloudwatch_-_alarm_details.png](img/cloudwatch_-_alarm_details.png "Create Amazon CloudWatch Alarm. Alarm details")

Connect CloudWatch Alarm to [created SNS topic](#create-amazon-sns-topic) and finally click `Create Alarm` button:
![cloudwatch_-_actions.png](img/cloudwatch_-_actions.png "Create Amazon CloudWatch Alarm. Actions")

**AWS docs:** https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html

## Create Amazon S3 bucket
Navigate to https://console.aws.amazon.com/s3/ and create new S3 bucket (e.g. `examplebucket`). Create new lifecyle rule for bucket (e.g. `DeleteTmpAfter72h`) with `tmp/` prefix filter:

![s3_-_lifecycle_rule.png](img/s3_-_lifecycle_rule.png "Create Amazon S3 bucket. Lifecycle rule")

Configure expiration as below. Expire after 3 days. Permanently delete after 3 days. Clean up incomplete multipart uploads after 1 day.

![s3_-_configure_expiration](img/s3_-_configure_expiration.png "Create Amazon S3 bucket. Configure expiration")

## Create Amazon Lambda function
Navigate to https://console.aws.amazon.com/lambda/. Click `Create function`. Click `Blueprints`. Search for and select `cloudwatch-alarm-to-slack-python3`. Click `Configure` button:

![lambda_-_blueprints.png](img/lambda_-_blueprints.png "Create Amazon Lambda function. Blueprints")

Enter function name (e.g. `example`) to `Name` field. In `Role` select `Create a new role from one or more templates.` In `Role name` field enter role name (e.g. `example`).

![lambda_-_basic_information.png](img/lambda_-_basic_information.png "Create Amazon Lambda function. Basic information")

Go to `SNS trigger` section and select [your SNS topic]((#create-amazon-sns-topic)). For example: `example` topic with `arn:aws:sns:eu-west-1:539199393808:example` ARN. Select the `Enable trigger` checkbox.

![lambda_-_sns_trigger.png](lambda_-_sns_trigger.png "Create Amazon Lambda function. SNS trigger")

[Create KMS Key](http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html) or use an existing KMS Key. For example: `arn:aws:kms:eu-west-1:539199393808:key/4c3126f2-f3bf-453e-b32d-58c9356d84b7`.

Go to `Lambda function code` section. Go to `Encryption configuration` subsection and select the `Enable helpers for encryption in transit` checkbox. Choose `AWS KMS key to encrypt in transit` (e.g. `arn:aws:kms:eu-west-1:539199393808:key/4c3126f2-f3bf-453e-b32d-58c9356d84b7`).

![lambda_-_encryption_configuration.png](img/lambda_encryption_configuration.png "Create Amazon Lambda function. Encryption configuration")

Paste [Slack channel](#create-slack-webhook) into the `slackChannel` environment variable, like `example`. The Slack channel does not contain private info, so do NOT click `Encrypt` button.

Paste [Slack webhook URL](#create-slack-webhook) into the `kmsEncryptedHookUrl` environment variable. You must exclude the protocol from the URL (e.g. `hooks.slack.com/services/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`). Click `Encrypt` button. Finally click `Create function` button:

![lambda_-_environment_variables.png](img/lambda_-_environment_variables.png "Create Amazon Lambda function. Environment variables")
