# AWS for Workflow Samples

[AWS for Workflows](https://docs.dynatrace.com/docs/platform-modules/automations/workflows/actions/aws) enables seamless integration and automation in your AWS environments within Dynatrace workflows. Based on events and schedules defined in a workflow, you can automate interactions with various AWS services, including EC2, S3, Lambda, and Auto Scaling.

Below are examples of workflows demonstrating how to use AWS workflow actions effectively.

## Store BizEvents in an S3 bucket

This example demonstrates how to store a [Dynatrace BizEvent](https://docs.dynatrace.com/docs/platform-modules/business-analytics/ba-basic-concepts#business-events-end-to-end-use-case) in an S3 Bucket.
It includes an [AWS CloudFormation](https://aws.amazon.com/cloudformation/) template defining the required AWS resources and the workflow template.
The example aims to offer a minimal yet self-contained workflow that utilizes AWS S3 actions.

### Setup AWS using a CloudFormation template
The provided CloudFormation template assists in the [setup](https://docs.dynatrace.com/docs/platform-modules/automations/workflows/actions/aws/aws-workflows-setup) of your AWS environment.
Specifically, Step 2 of the documentation outlines how to set up your AWS environment, including the provisioning of an Identity Provider and a Role in [AWS IAM](https://docs.aws.amazon.com/iam/).
You can automate the provisioning of these resources using the CloudFormation template found in `cloudformation_store_bizevents_in_s3_bucket.json`.
This template defines two resources:
1. An Identity Provider in [AWS IAM](https://docs.aws.amazon.com/iam/) that allows for identities issued by `https://token.dynatrace.com`.
2. An IAM role in [AWS IAM](https://docs.aws.amazon.com/iam/) that uses the identity provider as a trusted entity and defines inline policies for `account:ListRegions`, `s3:PutObject`, `s3:ListAllMyBuckets`, and `s3:CreateBucket`.


To create a new CloudFormation stack using the provided template, use the [AWS CLI](https://aws.amazon.com/cli/). Before executing the command, replace `[TENANT-ID]` with your Dynatrace Tenant ID:

```
aws cloudformation create-stack --stack-name dynatrace-s3-workflow-example --template-url https://raw.githubusercontent.com/Dynatrace/Dynatrace-workflow-samples/main/samples/aws/cloudformation_store_bizevents_in_s3_bucket.json --parameters ParameterKey=TenantUrl,ParameterValue=[TENANT-ID].apps.dynatrace.com ParameterKey=ConnectionName,ParameterValue=S3-Example --capabilities CAPABILITY_IAM
```

Step 3 of the documentation details the connection setup in Dynatrace. Use `S3-Example` as connection name and retrive the ARN of the previously provisioned IAM Role to complete this step. You can retrieve this ARN using the AWS CLI with the following command:
```
aws iam list-roles --query 'Roles[?starts_with(RoleName, `DynatraceS3WorkflowExample`)].Arn'
```

After completing all the steps described in the [setup](https://docs.dynatrace.com/docs/platform-modules/automations/workflows/actions/aws/aws-workflows-setup), you can import and run the provided workflow. 

### Workflow for storing BizEvents in an S3 Bucket
The workflow template in `wftpl_store_bizevent_in_s3_bucket.yaml` defines an on-demand trigger and consists of the following four actions:
1. The action [S3 list buckets](https://docs.dynatrace.com/docs/platform-modules/automations/workflows/actions/aws/aws-workflows-actions-s3#list-buckets) lists all S3 buckets in the region `eu-central-1`.
2. The action [S3 create bucket](https://docs.dynatrace.com/docs/platform-modules/automations/workflows/actions/aws/aws-workflows-actions-s3#create-bucket) creates a new S3 bucket named `dynatrace-bizevents` in the region `eu-central-1`. This action is only executed if there is not yet an S3 bucket named `dynatrace-bizevents`. For this check, the action uses the result of the previous action listing the available S3 buckets.
3. The action [Fetch BizEvent](https://docs.dynatrace.com/docs/platform-modules/automations/workflows/default-workflow-actions/dql-query-workflow-action) queries the last BizEvent using [DQL](https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language). Note that this action could produce an empty result if no BizEvents were available in the previous 30 days.
4. The action [S3 put object](https://docs.dynatrace.com/docs/platform-modules/automations/workflows/actions/aws/aws-workflows-actions-s3#put-object) stores available BizEvent in the S3 bucket `dynatrace-bizevents` using the current timestamp as key.