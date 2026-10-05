import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from awscrt import mqtt
from awsiot import mqtt_connection_builder


BASE_DIR = Path(__file__).resolve().parent
CERT_DIR = BASE_DIR / "certs"
CONFIG_PATH = BASE_DIR / "config.json"

CERT_PATH = CERT_DIR / "device-certificate.pem.crt"
PRIVATE_KEY_PATH = CERT_DIR / "private.pem.key"
ROOT_CA_PATH = CERT_DIR / "AmazonRootCA1.pem"


def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Missing configuration file: {CONFIG_PATH}\n"
            "Copy config.example.json to config.json and add your AWS IoT endpoint."
        )

    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_files():
    required_files = [
        CERT_PATH,
        PRIVATE_KEY_PATH,
        ROOT_CA_PATH,
        CONFIG_PATH,
    ]

    missing = [str(path) for path in required_files if not path.exists()]

    if missing:
        raise FileNotFoundError(
            "Required files are missing:\n- " + "\n- ".join(missing)
        )


def parse_temperature(value):
    """
    Convert numeric temperature input to float.

    If the value is not numeric, keep it as a string so that intentionally
    invalid test data can still be published to AWS IoT Core and validated
    by the downstream Lambda function.
    """
    try:
        return float(value)
    except ValueError:
        return value


def create_payload(config, temperature):
    return {
        "deviceId": config["deviceId"],
        "room": config["room"],
        "temperature": temperature,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Simulated temperature sensor for COIT20260 Assessment 3."
    )

    parser.add_argument(
        "--temperature",
        required=True,
        help=(
            "Temperature reading in degrees Celsius. "
            "Text values may also be supplied for invalid-data testing."
        ),
    )

    args = parser.parse_args()

    try:
        validate_files()
        config = load_config()

        temperature = parse_temperature(args.temperature)

        payload = create_payload(config, temperature)
        payload_json = json.dumps(payload)

        mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=config["endpoint"],
            cert_filepath=str(CERT_PATH),
            pri_key_filepath=str(PRIVATE_KEY_PATH),
            ca_filepath=str(ROOT_CA_PATH),
            client_id=config["clientId"],
            clean_session=True,
            keep_alive_secs=30,
        )

        print("Connecting to AWS IoT Core...")
        connect_future = mqtt_connection.connect()
        connect_future.result()
        print("Connected successfully.")

        print(f"\nTopic: {config['topic']}")
        print("Publishing:")
        print(json.dumps(payload, indent=2))

        publish_future, _ = mqtt_connection.publish(
            topic=config["topic"],
            payload=payload_json,
            qos=mqtt.QoS.AT_LEAST_ONCE,
        )

        publish_future.result()
        print("\nPublished successfully.")

        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()
        print("Disconnected.")

    except Exception as exc:
        print(f"\nERROR: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()