# AWS Tagger

Bulk AWS resources tagging utility. This tool is intended to be used to tag AWS resources using a single interface as
opposed to using the AWS console, CLI or SDK with different API interfaces for each service.

### Available AWS Services

Services are selected using the `--service` flag. The following services are currently supported.

```
--service <service-parameter>
```

| Service               | Parameter   |
| --------------------- | ----------- |
| API Gateway           | agw         |
| DynamoDB              | dynamodb    |
| Elastic Block Store   | ebs         |
| EC2                   | ec2         |
| ElastiCache           | elasticache |
| Kinesis Data Analytics| kda         |
| Kinesis Data Firehose | kdf         |
| Kinesis Data Stream   | kds         |
| KMS                   | kms         |
| Lambda                | lambda      |
| CloudWatch Logs       | logs        |
| RDS                   | rds         |
| S3                    | s3          |
| SNS                   | sns         |
| SQS                   | sqs         |

## How to install?

[Build from source](#development-how-to-build-and-distribute) or download the wheel file for the latest release and
install it to your system using pip.

```bash
pip install aws_tagger-py3-none-any.whl
```

## How to use?

There are four different operations that can be performed using this tool. Each operation (except import) supports
filtering resources by name and tag values. Read [filters and operators](#filters-and-operators) section for more
details.

- [List resources](#list-resources)
- [Tag resources](#tag-resources)
- [Export tags](#export-tags)
- [Import tags](#import-tags)

### Filters and Operators

Filters are used to filter resources by name and tag values. Filters are specified using the following format:

```
--filter <key><operator><value>
```

Keys are the resource name or tag key. For tag keys just use the tag key as key. For resource names use the special
`@name` key. Operators are used to specify the comparison operator. See the table below.

| Operator | Description         |
| -------- | ------------------- |
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
aws-tagger list --service dynamodb --filter 'team=data' --filter 'environment=production'
```

Find resources that does not have a `team` tag.

```bash
aws-tagger list --service ec2 --filter 'team--'
```

### Tag Resources

Add `subteam=intelligence` tag for resources that have `team=data` tag and resource name starting with `intel-`.

```bash
aws-tagger tag --service kds --filter 'team=data' --filter '@name^intel-' --tag 'subteam=intelligence'
```

Add `environment=staging` tag for resources that have `team=data` tag and resource name ending
with `staging`.

```bash
aws-tagger tag --service kdf --filter 'team=data' --filter '@name$staging' --tag 'environment=staging'
```

### Export Tags

Export the tags of the resources that have `team=data` tag to a csv file.

```bash
aws-tagger export --service ebs --filter 'team=data' --file tags.csv
```

Export the `team` and `Name` tags for the resources that have `team=data` tag to a csv file.

```bash
aws-tagger export --service ebs --filter 'team=data' --export-tag 'team' --export-tag 'Name' --file tags.csv
```

### Import Tags

Import the tags from a csv file and tag those resources.

```bash
aws-tagger import --file tags.csv
```

## Development: How to build and distribute?

Use python build tool to package the application. This will create two output files in `dist` directory. The file
with `.whl` extension is the wheel file and the file with `.tar.gz` extension is the source distribution.

```bash
python -m build
```

Distribute the wheel file to install the application. See [How to install?](#how-to-install) section for installation
instructions.
