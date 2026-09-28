# COIT20260 Assessment 3 – Cloud-Connected Temperature Monitoring

This repository contains the group implementation for **COIT20260 Assessment 3**.

The project develops a cloud-connected smart temperature monitoring solution based on the assessment scenario for **NextGen Technologies**. The application receives simulated IoT temperature readings, processes and stores the readings in the cloud, triggers alerts when temperatures become abnormal, and records system and error events for monitoring and troubleshooting.

## Project Objectives

The solution is designed to demonstrate the following capabilities:

- simulate IoT temperature sensor readings;
- securely publish sensor data to the cloud;
- receive and route MQTT messages through AWS IoT Core;
- process temperature readings using AWS Lambda;
- store temperature data in Amazon DynamoDB;
- trigger alerts for abnormal temperatures using Amazon SNS;
- record processing, warning, and error events using Amazon CloudWatch Logs;
- support deployment evidence, demonstration video, and live demonstration requirements.

## Cloud Platform

The group selected **Amazon Web Services (AWS)** as the cloud platform for the project.

Primary region:

```text
Asia Pacific (Sydney)
ap-southeast-2
```

The planned AWS services are:

| AWS Service | Purpose |
| --- | --- |
| AWS IoT Core | Receives MQTT messages from the simulated temperature sensor |
| AWS Lambda | Validates and processes incoming temperature readings |
| Amazon DynamoDB | Stores temperature readings for later use |
| Amazon SNS | Sends alerts when abnormal temperatures are detected |
| Amazon CloudWatch Logs | Records system activity, warnings, and errors |
| AWS IAM | Controls access to AWS services and project resources |

## High-Level Architecture

```text
+-----------------------------+
| Python Temperature Simulator|
| sensor-001 / Living Room    |
+-------------+---------------+
              |
              | MQTT over TLS
              | X.509 certificate authentication
              v
+-----------------------------+
|        AWS IoT Core         |
| Topic:                      |
| nextgen/home/temperature    |
+-------------+---------------+
              |
              | AWS IoT Rule
              v
+-----------------------------+
|         AWS Lambda          |
| Validate and process data   |
+---------+----------+--------+
          |          |
          |          |
          v          v
+---------------+  +----------------+
|   DynamoDB    |  |   Amazon SNS   |
| Store reading |  | Send alert     |
+---------------+  +----------------+
          |
          |
          v
+-----------------------------+
|    Amazon CloudWatch Logs   |
| System / warning / error    |
| events from processing      |
+-----------------------------+
```

CloudWatch logging is primarily produced by the processing layer so that normal processing, warnings, and failures can be reviewed during testing and demonstration.

## Data Flow

The intended end-to-end workflow is:

1. The Python simulator creates a temperature reading.
2. The simulator connects securely to AWS IoT Core using an X.509 device certificate.
3. The simulator publishes the reading to:

```text
nextgen/home/temperature
```

4. AWS IoT Core receives the MQTT message.
5. An AWS IoT Rule forwards the message to AWS Lambda.
6. Lambda validates the payload.
7. Lambda stores the reading in DynamoDB.
8. Lambda determines whether the reading is normal or abnormal.
9. If the reading is abnormal, Lambda triggers an SNS notification.
10. Processing events, warnings, and errors are recorded in CloudWatch Logs.

## MQTT Data Contract

All group components should use the following MQTT topic:

```text
nextgen/home/temperature
```

Expected payload format:

```json
{
  "deviceId": "sensor-001",
  "room": "Living Room",
  "temperature": 24.0,
  "timestamp": "2026-09-28T16:31:14.341053+00:00"
}
```

### Payload Fields

| Field | Type | Description |
| --- | --- | --- |
| `deviceId` | String | Unique identifier for the simulated temperature sensor |
| `room` | String | Room associated with the sensor |
| `temperature` | Number | Temperature reading in degrees Celsius |
| `timestamp` | String | UTC timestamp in ISO 8601 format |

This payload contract allows the sensor, Lambda processing, storage, alerting, and monitoring components to be developed independently while remaining compatible.

## Test Values

The following controlled values are currently used for development and demonstration:

| Temperature | Purpose |
| ---: | --- |
| `24°C` | Normal-temperature test |
| `35°C` | High-temperature test |
| `12°C` | Low-temperature test |

The simulator generates these values, while the final abnormal-temperature thresholds are enforced by the processing component.

## Repository Structure

The repository is organised by project workstream:

```text
coit20260-assessment3-temperature-monitoring/
├── sensor-simulator/
│   ├── simulator.py
│   ├── requirements.txt
│   ├── config.example.json
│   ├── README.md
│   └── certs/                     # Local only - ignored by Git
│
├── lambda/                        # Processing component
│
├── dynamodb/                      # Storage configuration/documentation
│
├── monitoring-alerts/             # SNS and CloudWatch work
│
├── docs/
│   ├── architecture/
│   ├── testing/
│   └── evidence/
│
├── .gitignore
└── README.md
```

Some directories will be added as their corresponding workstreams begin development.

## Group Workstreams

The four-person group is divided into four technical workstreams.

| Workstream | Main Responsibility |
| --- | --- |
| Member 1 – IoT Ingestion | AWS IoT Core and Python temperature sensor simulator |
| Member 2 – Processing | AWS Lambda validation and temperature-processing logic |
| Member 3 – Storage | Amazon DynamoDB table design and stored-reading verification |
| Member 4 – Alerts and Monitoring | Amazon SNS notifications and CloudWatch logs |

All members share responsibility for:

- end-to-end integration;
- testing;
- architecture documentation;
- report preparation;
- deployment evidence;
- demonstration video;
- live demonstration.

## Member 1 – IoT Ingestion

The Member 1 component is located in:

```text
sensor-simulator/
```

Its responsibilities include:

- creating the AWS IoT Thing;
- generating and activating the device certificate;
- creating the restricted AWS IoT policy;
- configuring the MQTT topic;
- identifying the AWS IoT Core data endpoint;
- building the Python temperature simulator;
- publishing normal, high, and low test readings;
- creating the AWS IoT Rule; and
- connecting the IoT Rule to the Lambda processing component.

Detailed setup and operating instructions are available in:

```text
sensor-simulator/README.md
```

## Current Project Status

### Completed

- AWS account created for Assessment 3
- AWS region confirmed as `ap-southeast-2`
- project budget alert configured
- IAM administrator identity configured
- AWS IoT Core accessed successfully
- IoT Thing `nextgen-temperature-sensor-01` created
- X.509 device certificate created and activated
- AWS IoT policy `nextgen-temperature-sensor-policy` created
- IoT policy attached to the device certificate
- AWS IoT `iot:Data-ATS` endpoint identified
- MQTT topic `nextgen/home/temperature` defined
- AWS MQTT Test Client publishing and subscription tested
- Python sensor simulator created
- local simulator authenticated successfully using the AWS IoT certificate
- `24°C` normal reading published successfully
- `35°C` high reading published successfully
- `12°C` low reading published successfully
- AWS IoT certificate files and local configuration excluded from Git

### In Progress / Remaining

- AWS IoT Rule configuration
- Lambda processing component
- DynamoDB storage component
- SNS alerting component
- CloudWatch logging and error evidence
- end-to-end integration
- final test cases
- deployment screenshots
- report content
- demonstration video
- live demonstration preparation

## Sensor Simulator Quick Start

Detailed instructions are available in `sensor-simulator/README.md`.

Install the Python dependency:

```powershell
python -m pip install -r .\sensor-simulator\requirements.txt
```

Copy the example configuration:

```powershell
Copy-Item .\sensor-simulator\config.example.json .\sensor-simulator\config.json
```

Update `config.json` with the AWS IoT device data endpoint.

The required certificate files must exist locally under:

```text
sensor-simulator/certs/
```

Required files:

```text
AmazonRootCA1.pem
device-certificate.pem.crt
private.pem.key
```

Run a normal reading:

```powershell
python .\sensor-simulator\simulator.py --temperature 24
```

Run a high reading:

```powershell
python .\sensor-simulator\simulator.py --temperature 35
```

Run a low reading:

```powershell
python .\sensor-simulator\simulator.py --temperature 12
```

## Security

Sensitive credentials must never be committed to the repository.

The repository `.gitignore` excludes:

```gitignore
certs/
**/certs/
*.pem
*.key
*.crt
.env
.env.*
config.json
```

Do not commit or share:

- AWS IoT private keys;
- AWS IoT device certificates;
- AWS passwords;
- MFA codes;
- AWS access keys;
- local configuration containing account-specific details.

The simulator uses a restricted IoT policy instead of unrestricted `iot:*` permissions.

## Branching

Development work should be performed on individual or workstream branches before being merged into `main`.

Example Member 1 branch:

```text
jerald/member1-iot-sensor
```

Changes should be reviewed before merging so that credentials, private configuration, and incomplete work are not accidentally committed.

## Testing Strategy

The project should demonstrate at least the following end-to-end test cases.

### Test 1 – Normal Temperature

Input:

```text
24°C
```

Expected outcome:

- message received by AWS IoT Core;
- Lambda processes the reading;
- reading stored in DynamoDB;
- normal processing event recorded;
- no abnormal-temperature alert generated.

### Test 2 – High Temperature

Input:

```text
35°C
```

Expected outcome:

- message received by AWS IoT Core;
- Lambda processes the reading;
- reading stored in DynamoDB;
- abnormal-temperature warning recorded;
- SNS alert generated.

### Test 3 – Low Temperature

Input:

```text
12°C
```

Expected outcome:

- message received by AWS IoT Core;
- Lambda processes the reading;
- reading stored in DynamoDB;
- abnormal-temperature warning recorded;
- SNS alert generated.

### Test 4 – Invalid Input

A malformed or invalid temperature payload will be used to verify:

- validation handling;
- error logging;
- system stability; and
- CloudWatch error evidence.

The exact invalid payload will be finalised with the processing component.

## Assessment Deliverables

The completed project will support the following Assessment 3 deliverables:

- cloud-based smart application;
- step-by-step deployment evidence;
- screenshots of configuration and operation;
- system and error logs;
- alert evidence;
- written report;
- deployment/configuration demonstration video; and
- live demonstration.

## Live Demonstration

The group plans to demonstrate the completed application on **6 October 2026**.

The intended demonstration sequence is:

```text
Sensor simulator
      |
      v
AWS IoT Core
      |
      v
Lambda
   /      \
  v        v
DynamoDB   SNS
      |
      v
CloudWatch Logs
```

The demonstration will use controlled sensor values so the behaviour is repeatable.

## Documentation

Component-specific documentation should be stored with the relevant component.

Current documentation:

```text
sensor-simulator/README.md
```

Additional component documentation will be added as Lambda, DynamoDB, SNS, and CloudWatch work begins.

## Project Notes

This repository is for the COIT20260 Assessment 3 group project.

Assessment resources, code, screenshots, and documentation should remain focused on the Assessment 3 temperature-monitoring solution and should not reuse unrelated Assessment 2 BookHaven resources.
