# AWS Tag

Bulk AWS resource tagging utility. Tag AWS resources using a single interface with filter support
to operate on a subset of resources.

## Installation

Install the package using pip. Alternatively, you can also use 
[pipx](https://packaging.python.org/en/latest/guides/installing-stand-alone-command-line-tools/), which installs 
the package in an isolated environment and adds the package to the system path.

```bash
pip install aws-tag
```

## Usage

There are four different operations that can be performed using this tool. Each operation (except import) supports
filtering resources by name and tag values. Read [filters and operators](#filters-and-operators) section for more
details.

- [List resources](#list-resources)
- [Tag resources](#tag-resources)
- [Export tags](#export-tags)
- [Import tags](#import-tags)

### Available AWS Services

Services are selected using the `--service` flag. The following services are currently supported.

```
--service <service-parameter>
```

| Service                | Parameter   |
|------------------------|-------------|
| API Gateway            | agw         |
| DynamoDB               | dynamodb    |
| Elastic Block Store    | ebs         |
| EC2                    | ec2         |
| ECR                    | ecr         |
| ElastiCache            | elasticache |
| Kinesis Data Analytics | kda         |
| Kinesis Data Firehose  | kdf         |
| Kinesis Data Stream    | kds         |
| KMS                    | kms         |
| Lambda                 | lambda      |
| CloudWatch Logs        | logs        |
| RDS                    | rds         |
| S3                     | s3          |
| SNS                    | sns         |
| SQS                    | sqs         |

### Filters and Operators

Filters are used to filter resources by name and tag values. Filters are specified using the following format:

```
--filter <key><operator><value>
```

Keys are the resource name or tag key. For tag keys just use the tag key as key. For resource names use the special
`@name` key. Operators are used to specify the comparison operator. See the table below.

| Operator | Description         |
|----------|---------------------|
| `= `     | Equals              |
| `!=`     | Not equal           |
| `~`      | Contains            |
| `!~`     | Does not contain    |
| `--`     | Does not exist      |
| `^ `     | Starts with         |
| `!^`     | Does not start with |
| `$ `     | Ends with           |
| `!$`     | Does not end with   |

Note that ``--`` operator is used to check if a tag does not exist and has no `value` associated with it. Please check
examples below.

### List Resources

Find resources that have `team=data` and `environment=production` tags.

```bash
aws-tag list --service dynamodb --filter 'team=data' --filter 'environment=production'
```

Find resources that does not have a `team` tag.

```bash
aws-tag list --service ec2 --filter 'team--'
```

### Tag Resources

Add `subteam=intelligence` tag for resources that have `team=data` tag and resource name starting with `intel-`.

```bash
aws-tag tag --service kds --filter 'team=data' --filter '@name^intel-' --tag 'subteam=intelligence'
```

Add `environment=staging` tag for resources that have `team=data` tag and resource name ending
with `staging`.

```bash
aws-tag tag --service kdf --filter 'team=data' --filter '@name$staging' --tag 'environment=staging'
```

### Export Tags

Export the tags of the resources that have `team=data` tag to a csv file.

```bash
aws-tag export --service ebs --filter 'team=data' --file tags.csv
```

Export the `team` and `Name` tags for the resources that have `team=data` tag to a csv file.

```bash
aws-tag export --service ebs --filter 'team=data' --export-tag 'team' --export-tag 'Name' --file tags.csv
```

### Import Tags

Import the tags from a csv file and tag those resources.

```bash
aws-tag import --file tags.csv
```
