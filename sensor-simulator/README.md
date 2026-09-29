# Temperature Sensor Simulator

This directory contains the simulated IoT temperature sensor for **COIT20260 Assessment 3**.

The simulator publishes temperature readings from a local Python program to **AWS IoT Core** using **MQTT over TLS** with **X.509 certificate authentication**.

## Purpose

The simulator represents a smart-home temperature sensor in the Assessment 3 cloud-connected thermal monitoring solution.

Its responsibility is to:

- simulate temperature readings;
- connect securely to AWS IoT Core;
- publish readings to the agreed MQTT topic;
- provide normal, high, and low temperature test values for the rest of the system; and
- support later integration with AWS Lambda, DynamoDB, SNS, and CloudWatch.

The simulator does not decide whether a temperature is abnormal. That processing will be handled by the downstream Lambda component.

## AWS Configuration

- **AWS Region:** `ap-southeast-2`
- **Region Name:** Asia Pacific (Sydney)
- **IoT Thing:** `nextgen-temperature-sensor-01`
- **IoT Policy:** `nextgen-temperature-sensor-policy`
- **MQTT Topic:** `nextgen/home/temperature`
- **Client ID:** `nextgen-temperature-sensor-01`
- **Device ID:** `sensor-001`
- **Room:** `Living Room`

## Architecture

The current Member 1 component uses the following flow:

```text
Python Temperature Simulator
            |
            | MQTT over TLS
            v
       AWS IoT Core
            |
            | Topic:
            | nextgen/home/temperature
            v
nextgenTemperatureProcessingRule
            |
            v
nextgen-temperature-processor
```

The IoT Rule and Lambda integration are complete and have been verified using live sensor messages.

The complete group solution is intended to follow this architecture:

```text
Simulated Temperature Sensor
            |
            | MQTT
            v
       AWS IoT Core
            |
            v
        AWS Lambda
         /       \
        v         v
   DynamoDB      SNS
        |
        v
 CloudWatch Logs
```

## MQTT Payload

Temperature readings are published as JSON.

Example payload:

```json
{
  "deviceId": "sensor-001",
  "room": "Living Room",
  "temperature": 24.0,
  "timestamp": "2026-09-28T16:31:14.341053+00:00"
}
```

### Payload Fields

| Field | Description |
| --- | --- |
| `deviceId` | Unique identifier for the simulated temperature sensor |
| `room` | Room where the simulated sensor is located |
| `temperature` | Temperature reading in degrees Celsius |
| `timestamp` | UTC timestamp in ISO 8601 format |

## Project Structure

The simulator directory is structured as follows:

```text
sensor-simulator/
├── simulator.py
├── requirements.txt
├── config.example.json
├── config.json
├── README.md
└── certs/
    ├── AmazonRootCA1.pem
    ├── device-certificate.pem.crt
    └── private.pem.key
```

The following files are local-only and must not be committed to Git:

```text
config.json
certs/
*.pem
*.key
*.crt
```

## Requirements

The simulator requires:

- Python 3;
- internet access;
- AWS IoT Core access;
- an active AWS IoT device certificate;
- the corresponding private key;
- Amazon Root CA 1; and
- the AWS IoT Core device data endpoint.

## Python Dependencies

The simulator uses the AWS IoT Device SDK for Python.

Install the required dependency from the repository root:

```powershell
python -m pip install -r .\sensor-simulator\requirements.txt
```

The `requirements.txt` file currently contains:

```text
awsiotsdk
```

## Configuration

Copy the example configuration:

```powershell
Copy-Item .\sensor-simulator\config.example.json .\sensor-simulator\config.json
```

The example configuration uses the following structure:

```json
{
  "endpoint": "YOUR_AWS_IOT_ENDPOINT",
  "clientId": "nextgen-temperature-sensor-01",
  "topic": "nextgen/home/temperature",
  "deviceId": "sensor-001",
  "room": "Living Room"
}
```

Update the local `config.json` file with the AWS IoT Core device data endpoint.

The endpoint normally has a format similar to:

```text
xxxxxxxxxxxxxx-ats.iot.ap-southeast-2.amazonaws.com
```

The real `config.json` file is intentionally excluded from Git.

## Device Certificates

The simulator authenticates to AWS IoT Core using X.509 certificates.

The following files must exist in:

```text
sensor-simulator/certs/
```

Required files:

```text
AmazonRootCA1.pem
device-certificate.pem.crt
private.pem.key
```

### Certificate Purpose

| File | Purpose |
| --- | --- |
| `AmazonRootCA1.pem` | Verifies the AWS IoT Core server certificate |
| `device-certificate.pem.crt` | Identifies the simulated IoT device |
| `private.pem.key` | Proves possession of the device identity during TLS authentication |

## Security

The device certificate files and private configuration must remain private.

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

Do not commit, upload, or share the private key.

Do not place any of the following in GitHub, Teams, the assessment report, or public screenshots:

```text
private.pem.key
device-certificate.pem.crt
config.json
AWS passwords
AWS access keys
MFA codes
```

## AWS IoT Policy

The simulated sensor uses the following AWS IoT policy:

```text
nextgen-temperature-sensor-policy
```

The policy allows the device to:

- connect to AWS IoT Core using the client ID `nextgen-temperature-sensor-01`; and
- publish messages to `nextgen/home/temperature`.

The device is not granted unrestricted `iot:*` permissions.

The policy is intentionally restricted to the minimum actions currently required by the simulator.

## Running the Simulator

Run commands from the repository root.

### Normal Temperature Test

```powershell
python .\sensor-simulator\simulator.py --temperature 24
```

Expected output:

```text
Connecting to AWS IoT Core...
Connected successfully.

Topic: nextgen/home/temperature
Publishing:
{
  "deviceId": "sensor-001",
  "room": "Living Room",
  "temperature": 24.0,
  "timestamp": "..."
}

Published successfully.
Disconnected.
```

### High Temperature Test

```powershell
python .\sensor-simulator\simulator.py --temperature 35
```

This publishes a high-temperature test reading for later Lambda and SNS testing.

### Low Temperature Test

```powershell
python .\sensor-simulator\simulator.py --temperature 12
```

This publishes a low-temperature test reading for later Lambda and SNS testing.

## Test Values

The simulator currently uses these controlled values for development and demonstration:

| Temperature | Test Purpose |
| ---: | --- |
| `24°C` | Normal temperature reading |
| `35°C` | High-temperature reading |
| `12°C` | Low-temperature reading |

These values are generated by the simulator only.

The final normal and abnormal thresholds will be enforced by the processing component rather than by the sensor simulator.

## Testing with AWS IoT Core

AWS IoT Core includes an MQTT Test Client that can be used to verify that messages from the simulator are received successfully.

In AWS IoT Core:

1. Open **Test**.
2. Open **MQTT test client**.
3. Subscribe to:

```text
nextgen/home/temperature
```

4. Run the simulator locally.
5. Confirm that the published JSON message appears in the received messages panel.

A successful test proves the following path:

```text
Local Python Simulator
        |
        | MQTT over TLS
        v
AWS IoT Core
        |
        v
nextgen/home/temperature
```

## Current Test Results

The following tests have been completed successfully.

### Normal Reading

Command:

```powershell
python .\sensor-simulator\simulator.py --temperature 24
```

Result:

```text
Connected successfully.
Published successfully.
Disconnected.
```

### High Reading

Command:

```powershell
python .\sensor-simulator\simulator.py --temperature 35
```

Result:

```text
Connected successfully.
Published successfully.
Disconnected.
```

### Low Reading

Command:

```powershell
python .\sensor-simulator\simulator.py --temperature 12
```

Result:

```text
Connected successfully.
Published successfully.
Disconnected.
```

## Member 1 Responsibilities

Member 1 is responsible for the IoT ingestion and simulated sensor component.

Current responsibilities include:

- configuring AWS IoT Core;
- creating the IoT Thing;
- creating and activating the device certificate;
- creating the IoT policy;
- attaching the policy to the certificate;
- identifying the AWS IoT Core data endpoint;
- defining the MQTT topic;
- building the Python temperature simulator;
- securing the certificate and private key;
- testing normal temperature publishing;
- testing high-temperature publishing;
- testing low-temperature publishing; and
- later configuring the AWS IoT Rule that forwards readings to Lambda.

## Completed Work

The following Member 1 tasks have already been completed:

- AWS IoT Core opened in `ap-southeast-2`;
- IoT Thing `nextgen-temperature-sensor-01` created;
- device certificate generated;
- device certificate activated;
- certificate files downloaded securely;
- IoT policy `nextgen-temperature-sensor-policy` created;
- IoT policy attached to the device certificate;
- default `iot:Data-ATS` endpoint identified;
- MQTT topic `nextgen/home/temperature` defined;
- MQTT Test Client subscription tested;
- manual MQTT publishing tested;
- local Python project created;
- AWS IoT Device SDK installed;
- certificate files excluded from Git;
- local configuration excluded from Git;
- Python simulator connected successfully to AWS IoT Core;
- normal reading `24°C` published successfully;
- high reading `35°C` published successfully; and
- low reading `12°C` published successfully;
- IoT Rule `nextgenTemperatureProcessingRule` created and activated;
- Lambda target `nextgen-temperature-processor` attached to the rule;
- AWS IoT Core `lambda:InvokeFunction` permission verified;
- end-to-end sensor-to-Lambda integration verified;
- CloudWatch confirmed integrated classifications:
  - `24°C` → `NORMAL`
  - `35°C` → `HIGH`
  - `12°C` → `LOW`.

## Remaining Member 1 Work

The remaining work for Member 1 is:

- support full-system integration once DynamoDB and SNS are ready;
- collect final deployment screenshots;
- collect final operation screenshots;
- contribute Member 1 deployment and integration notes to the report; and
- prepare the Member 1 portion of the demonstration video and live demonstration.

## Verified Sensor-to-Lambda Integration

The following live integration path has been tested successfully:

```text
Python Sensor Simulator
        |
        v
AWS IoT Core
        |
        v
nextgenTemperatureProcessingRule
        |
        v
nextgen-temperature-processor
        |
        v
CloudWatch Logs
```

Verified results:

| Sensor input | Lambda classification |
| ---: | --- |
| `24°C` | `NORMAL` |
| `35°C` | `HIGH` |
| `12°C` | `LOW` |

## Integration Contract

The other group components should expect messages from the following topic:

```text
nextgen/home/temperature
```

Payload format:

```json
{
  "deviceId": "sensor-001",
  "room": "Living Room",
  "temperature": 24.0,
  "timestamp": "ISO-8601 UTC timestamp"
}
```

The Lambda processing component should use this contract when processing incoming IoT readings.

## Assessment Context

This simulator supports the COIT20260 Assessment 3 requirement to create a cloud-based smart application that:

- receives IoT sensor data;
- stores sensor data in the cloud;
- detects abnormal temperatures;
- triggers alerts;
- records system events; and
- records error messages.

The simulator provides the sensor-data generation and cloud-ingestion portion of that workflow.

## Notes for Demonstration

For the final demonstration, Member 1 can use controlled commands instead of random sensor values.

Normal test:

```powershell
python .\sensor-simulator\simulator.py --temperature 24
```

High-temperature test:

```powershell
python .\sensor-simulator\simulator.py --temperature 35
```

Low-temperature test:

```powershell
python .\sensor-simulator\simulator.py --temperature 12
```

This makes the live demonstration repeatable and allows the downstream Lambda, DynamoDB, SNS, and CloudWatch components to be tested using known inputs.
