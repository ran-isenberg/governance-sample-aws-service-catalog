
# Governance Sample AWS Service Catalog

## Serverless Platform Engineering Example

[![license](https://img.shields.io/github/license/ran-isenberg/governance-sample-aws-service-catalog)](https://github.com/ran-isenberg/governance-sample-aws-service-catalog/blob/master/LICENSE)
![PythonSupport](https://img.shields.io/static/v1?label=python&message=3.12&color=blue?style=flat-square&logo=python)
[![codecov](https://codecov.io/gh/ran-isenberg/governance-sample-aws-service-catalog/branch/main/graph/badge.svg?token=P2K7K4KICF)](https://codecov.io/gh/ran-isenberg/governance-sample-aws-service-catalog)
![version](https://img.shields.io/github/v/release/ran-isenberg/governance-sample-aws-service-catalog)
![github-star-badge](https://img.shields.io/github/stars/ran-isenberg/governance-sample-aws-service-catalog.svg?style=social)
![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/ran-isenberg/governance-sample-aws-service-catalog/badge)
![issues](https://img.shields.io/github/issues/ran-isenberg/governance-sample-aws-service-catalog)
![alt text](https://github.com/ran-isenberg/governance-sample-aws-service-catalog/blob/main/docs/media/banner.png?raw=true)

**[📜Documentation](https://ran-isenberg.github.io/governance-sample-aws-service-catalog/)** | **[Blogs website](https://www.ranthebuilder.cloud)**
> **Contact details | ran.isenberg@ranthebuilder.cloud**

[![Twitter Follow](https://img.shields.io/twitter/follow/IsenbergRan?label=Follow&style=social)](https://twitter.com/IsenbergRan)
[![Website](https://img.shields.io/badge/Website-www.ranthebuilder.cloud-blue)](https://www.ranthebuilder.cloud/)

This repository provides a sample implementation to showcase how to enforce governance policies through AWS Service Catalog, helping ensure compliance and efficient management of AWS resources while keeping a high level
of visibility on deployed service across your organization.

AWS Service Catalog allows organizations to create and manage catalogs of IT services that are approved for use on AWS.

Platform engineering teams can use this repository as a basis for their own organizational portfolio of security and governance solutions.

This repository contains a sample serverless Python based implementation for governance using AWS Service Catalog, Amazon SNS, SQS, DynamoDB, CloudWatch and Lambda.

It demonstrates how to create and manage service catalog portfolios and products, as well as enforce governance policies.

Another important feature is tracking provisioned products - a global DynamoDB table stores detailed information about provisioned products automatically, their versions, regions, and users, enhancing platform engineering visibility.

Two samples products are included:
1. WAF rules
2. IAM role for CI/CD pipelines


## Prerequisites
- AWS account with necessary permissions.
- AWS CLI installed and configured.
- Node.js and npm installed.
- AWS CDK (Cloud Development Kit) installed.
- AWS account after running the CDK bootstrap command in the designated region
- Python 3.12 installed
- Poetry
- Docker

## Setup
1. **Clone the repository**
   ```sh
   git clone https://github.com/ran-isenberg/governance-sample-aws-service-catalog.git
   cd governance-sample-aws-service-catalog
   ```
2. **Setup environment**
  ```sh
   poetry config --local virtualenvs.in-project true
   poetry shell
   poetry install
   make dev
   ```
3. **Deploy service catalog portfolio**
  ```sh
   make deploy
   ```
4. Share the portfolio with an account of your choice and provision a product. Refer to the [documentation](https://docs.aws.amazon.com/servicecatalog/latest/adminguide/introduction.html)

## Architecture
The solution architecture includes:
- AWS Service Catalog for managing portfolios and products.
- Global DynamoDB table for tracking provisioned products.
- Custom resource for creating visibility entries
- SNS topic and SQS queue
- AWS Lambda for handling custom resource requests
- AWS CloudWatch logs, metrics, traces (AWS X-Ray), alarms and dashboards for observability.

## Step-by-Step Provisioned Product Deployment Flow

This section describes the step-by-step deployment flow for the architecture depicted in the diagram.


![alt text](https://github.com/ran-isenberg/governance-sample-aws-service-catalog/blob/main/docs/media/design.png?raw=true)

### 1. Provision Product by Admin
**Step 1**: The Admin initiates the provisioning of a product through the AWS Service Catalog service and the platform engineering portfolio.
- **Action**: Admin provisions the product.
- **Outcome**: The provisioning process starts for the selected product.

### 2. Create Stack
**Step 2**: The AWS Service Catalog triggers the creation of a CloudFormation stack for the provisioned product.
- **Action**: AWS Service Catalog creates the CloudFormation stack.
- **Outcome**: A new CloudFormation stack is created and ready to deploy resources.

### 3. Create Resources with CI/CD Pipeline Role
**Step 3**: The CI/CD pipeline role is used to create resources defined in the CloudFormation stack.
- **Action**: Resources are created using the CI/CD pipeline role.
- **Outcome**: The resources defined in the stack template are provisioned.

### 4. Custom Resource Execution
**Step 4**: The stack includes a custom resource that is executed during the stack creation process.
- **Action**: The custom resource is created.
- **Outcome**: Custom logic defined in the custom resource is triggered.

### 5. Publish Message with Product Details
**Step 5**: The custom resource publishes a message containing the provisioned product metadata to an Amazon SNS topic.
- **Action**: Publish message to SNS.
- **Outcome**: The message with necessary details is published to the SNS topic.

### 6. Send Message to SQS Queue
**Step 6**: The SNS topic forwards the message to an SQS queue in the Platform Engineering Service Catalog Account.
- **Action**: SNS sends the message to the SQS queue.
- **Outcome**: The message is queued for processing.

### 7. Handle Message with AWS Lambda
**Step 7**: An AWS Lambda function is triggered to handle the message from the SQS queue.
- **Action**: Lambda function processes the message.
- **Outcome**: The message is processed, and necessary actions are taken.

### 8. Add Provisioned Product Information to DynamoDB
**Step 8**: The Lambda function adds information about the provisioned product, including its version, region, and user details, to a global DynamoDB table for enhanced visibility.
- **Action**: Add provisioned product information to DynamoDB.
- **Outcome**: The global DynamoDB table is updated with the new product details.

Here's an example of two entries in the DynamoDB table after two products are provisioned.
![alt text](https://github.com/ran-isenberg/governance-sample-aws-service-catalog/blob/main/docs/media/table.png?raw=true)

### 9. Release from Wait State and Finish Stack Deployment
**Step 9**: The stack is released from the wait state, and the deployment process is completed.
- **Action**: Release stack from wait state.
- **Outcome**: The CloudFormation stack deployment is finalized, and the provisioned product is ready for use.


## Code Contributions
Code contributions are welcomed. Read this [guide.](https://github.com/ran-isenberg/governance-sample-aws-service-catalog/blob/main/CONTRIBUTING.md)

## Code of Conduct
Read our code of conduct [here.](https://github.com/ran-isenberg/governance-sample-aws-service-catalog/blob/main/CODE_OF_CONDUCT.md)

## Connect
* Email: [ran.isenberg@ranthebuilder.cloud](mailto:ran.isenberg@ranthebuilder.cloud)
* Blog Website [RanTheBuilder](https://www.ranthebuilder.cloud)
* LinkedIn: [ranisenberg](https://www.linkedin.com/in/ranisenberg/)
* Twitter: [IsenbergRan](https://twitter.com/IsenbergRan)


## License
This library is licensed under the MIT License. See the [LICENSE](https://github.com/ran-isenberg/governance-sample-aws-service-catalog/blob/main/LICENSE) file.
