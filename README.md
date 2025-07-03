# 🚨 AutoGuard: AWS Lambda Security Scanner & Auto-Remediation

**AutoGuard** is a serverless AWS security and compliance tool that scans your cloud resources for misconfigurations, compliance gaps, and cost anomalies. It automatically detects and remediates common issues, sending you alerts and reports—all powered by AWS Lambda for zero-ops, always-on security.

---

## 🌟 Features

* **Multi-Resource Scanning**: Checks EC2, S3, IAM, compliance, and cost.
* **Auto-Remediation**: Automatically fixes common security/config issues.
* **Modular Handlers**: Easily extend with your own resource handlers.
* **Audit Logging & Reporting**: All actions and findings are logged for compliance and sent as detailed email reports via SNS.
* **Cloud Native**: Deploys quickly with CloudFormation.
* **Cost Awareness**: Built-in cost scan/handler to identify waste.
* **Minimal Browser Interface**: Trigger scans via the provided `static/index.html` page.
* **Enhanced Compliance Checks**: Includes root account MFA and S3 encryption validation for CIS coverage.
* **Detailed Web Reports**: Uploads scan results to S3 and shares a link via SNS.
* **Web Dashboard**: View reports in `static/dashboard.html`.
* **Organization-Wide Scanning**: Optional multi-account scans via AWS Organizations.
* **AI-Based Monitoring**: Simple anomaly detection to trigger auto-scaling.
* **Slack & Webhook Alerts**: Receive notifications in chat or custom systems.
* **Scheduled Scans**: CloudWatch Events trigger periodic executions.
* **Immediate HTTP Results**: The `/scan` API responds with a JSON summary when the run completes.

---

## 🛠️ How It Works

There are **two ways to deploy and use AutoGuard**:

### 1. Using the Zip File (Manual Setup)

* Download or build `Autoguard.zip`, which contains all dependencies and code.
* Upload this ZIP as a new AWS Lambda function via the AWS Console.
* **Manually** set up:

  * API Gateway endpoints
  * SNS notification topics/subscriptions
  * Lambda environment variables
  * IAM roles and permissions
* This is good for testing or customizing code, but **requires manual AWS resource configuration**.

### 2. Using the CloudFormation Template (Recommended)

You can deploy the entire stack with one command using the helper script
`scripts/deploy_stack.py`:

```bash
python3 scripts/deploy_stack.py you@example.com
```

This script calls CloudFormation to create the stack defined in
`Cloudformation.yml` and waits for it to finish.

* Alternatively, you can deploy the template manually. It automatically creates and connects:

  * Lambda function
  * API Gateway (with all stages and endpoints)
  * SNS topics and subscriptions (for email reporting)
  * Audit logs S3 bucket
  * Environment variables, IAM roles, permissions
  * All other required AWS infrastructure
* **Best for production and quick, error-free setup.**

---

## 🚦 Triggering a Scan & Usage Limitations

* **Scans are triggered by sending a POST request to the `/scan` API endpoint.**
* You can use a REST client like Postman or cURL, or open `static/index.html` in your browser and click **Run Scan** after setting your API endpoint.
* When you trigger a scan, the Lambda function runs to completion and the API returns a JSON **summary** of the findings.
* A full HTML report with remediation details is still uploaded to S3 and emailed via SNS for reference.

**Example:**

```sh
curl -X POST https://your-api-id.execute-api.region.amazonaws.com/prod/scan
```

---

## 🖼️ Deployment & Architecture Diagram

```plaintext
+--------------------------+
| User / API (POST /scan)  |
+-----------+--------------+
            |
            v
     +-------------+
     | API Gateway |
     +-------------+
            |
            v
  +---------------------+
  | Lambda (AutoGuard)  |
  +---------------------+
            |
  +---------+---------+---------+--------+--------+
  |         |         |         |        |        |
[EC2]     [S3]     [IAM]  [Compliance] [Cost]
            |
            v
     +---------------------+
     |    Audit Logger     |
     +---------------------+
        |             |
        v             v
   S3 Bucket     SNS → Email
```

**How it works:**
When AutoGuard is triggered by a POST API call, API Gateway routes the request to Lambda. Lambda uses modular handlers to scan AWS resources, attempts auto-remediation, logs results, and sends a detailed report to your email via SNS.
All infrastructure is created automatically with the CloudFormation template.

---

### End-to-End Workflow

1. **Deploy** AutoGuard using `scripts/deploy_stack.py` or the CloudFormation console.
2. **Trigger** a scan via `curl` or the simple web UI in `static/index.html`.
3. **Scanning & Remediation**: Lambda scans EC2, S3, IAM, cost and compliance across all configured accounts, performs auto-remediation where possible and logs everything to S3.
4. **AI Monitoring & Auto-Scaling** watches for anomalies and scales the scanning Lambda if needed.
5. **Results**: A JSON summary is returned immediately in the API response. A detailed HTML report is uploaded to S3, emailed via SNS, and viewable in `static/dashboard.html`.

---

## 🧩 CloudFormation Stack Logic

When you deploy AutoGuard using the provided `Cloudfront.yml` CloudFormation template, **all necessary AWS resources are created and connected automatically**. Here’s how it works:

### What Gets Created

* **API Gateway Endpoint**
  Exposes a REST API endpoint (`/scan`) for triggering the Lambda scan.
* **Lambda Function**
  The core of AutoGuard for scanning, remediation, logging, and notifications.
* **SNS Topic and Email Subscription**
  For sending detailed reports to your provided email.
* **Audit Logs S3 Bucket**
  Stores audit logs of every scan and remediation.
* **IAM Role and Permissions**
  Grants Lambda access to necessary AWS services.

### CloudFormation Component Flow

![CloudFormation Component Flow](assets/image.svg)



### CloudFormation Highlights

* **AWSTemplateFormatVersion:** Uses the standard CloudFormation version for AWS resources.
* **Parameters:** Accepts your email address (`UserEmail`) for report delivery.
* **Resources Created:**

  * SNS topic and email subscription for notifications
  * Audit S3 bucket for logs
  * IAM role and policies for Lambda execution
  * Lambda function with environment variables for SNS and S3
  * API Gateway with `/scan` endpoint (POST method)
  * Permissions for API Gateway to invoke Lambda
  * Automatic deployment of the API to a production stage

### Outputs

After stack creation, CloudFormation outputs:

* The `/scan` API endpoint URL for triggering scans
* Lambda function name
* SNS Topic ARN (for notifications)
* Audit S3 bucket name

**This stack ensures you have a ready-to-use, fully connected scanning system with a single deployment command and minimal setup.**

---

## 🗂️ Project Structure

```
autoguard-aws_lambda_app/
├── audit/
│   └── logger.py
├── autoguard/
│   ├── __init__.py
│   ├── config.py
│   ├── fixer.py
│   ├── reporter.py
│   └── scanner.py
├── handlers/
│   ├── compliance_handler.py
│   ├── cost_handler.py
│   ├── ec2_handler.py
│   ├── iam_handler.py
│   └── s3_handler.py
├── integrations/
│   ├── slack_notifier.py         # (Planned/future)
│   └── webhook_notifier.py       # (Planned/future)
├── .env
├── Autoguard.zip
├── Cloudfront.yml
├── lambda_handler.py
├── requirements.txt
└── README.md
```

---

## ✅ What Was Achieved

* Core Lambda function to scan EC2, S3, IAM, compliance, and cost.
* Modular handler system for easy extensibility.
* Working auto-remediation for common security issues (S3, IAM).
* Audit logging and reporting using SNS (email).
* Automated deployment with CloudFormation.

---

## 💡 Plans & Ideas To Achieve

| Feature/Idea                                                                                      | Achieved    |
| ------------------------------------------------------------------------------------------------- | ----------- |
| Core AWS resource scanning (EC2, S3, IAM, cost, compliance)                                       | ✅           |
| Modular handler architecture                                                                      | ✅           |
| Auto-remediation for common issues                                                                | ✅           |
| Audit logging and reporting with email via SNS                                                    | ✅           |
| Automated deployment with CloudFormation                                                          | ✅           |
| Static webpage: explaining the solution and assisting with direct AWS scans                       | ✅           |
| UI/UX for the scan trigger (web or minimal interface)                     | ✅           |
| Automating CloudFormation deployment with little/no manual interaction                            | ✅           |
| Enhanced security and compliance checks (full CIS coverage, custom rules, etc.)                   | ✅ (partial) |
| SNS template modification: include a detailed web report (e.g., unverified IPs, unused IAM, etc.) | ✅           |
| Web-based dashboard for extended reporting                    | ✅           |
| Multi-account and AWS Organization-wide scanning                    | ✅           |
| AI integration: advanced security monitoring & auto-scaling/reactive actions                      | ✅ (basic)   |
| Slack and webhook alert integrations                    | ✅           |
| Built-in scheduler (CloudWatch Events trigger)                    | ✅           |
| Can trigger scan via browser                                                                      | ✅           |
| Can trigger scan via REST client (Postman/cURL)                                                   | ✅           |
| Immediate HTTP scan results in response                    | ✅           |
| Results/reports delivered by email (SNS)                    | ✅           |

---

### Notes

* **Slack and webhook alert integrations**: Configurable via environment variables.
* **Dashboard and AI features**: Basic reporting dashboard in `static/dashboard.html` with simple anomaly detection.
* **Built-in scheduling via CloudWatch Events**: Enabled by default through the CloudFormation template.
* **A minimal web UI is available in `static/index.html` for triggering scans in the browser.**
* **Run `scripts/deploy_stack.py` for one-command CloudFormation deployment.**

---

## 🏗️ Original Plan vs. Final Implementation

* **Original Plan:**
  Support for all major AWS services, web-based dashboard, multi-account scanning, advanced compliance frameworks, extensive integrations, AI-driven security monitoring, and minimal setup friction.
* **Final Implementation:**
  Focused on core resource types (EC2, S3, IAM), modularity, production-ready remediation for the most critical findings, and reliable, serverless deployment with email reporting.

---
