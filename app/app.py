import hmac

from flask import Flask, Response, jsonify, request

app = Flask(__name__)

SIGNATURE_HEADER_NAME = ""
VALIDATION_KEY = ""


def compute_signature(validation_key: str, body: bytes, timestamp: str) -> str:
    timestamp_in_bytes = timestamp.encode()
    data_to_hash = timestamp_in_bytes + b"." + body

    signature = hmac.new(
        validation_key.encode(),
        data_to_hash,
        "SHA256",
    ).hexdigest()
    return f"timestamp={timestamp},signature={signature}"


def parse_timestamp(header_value: str) -> str:
    components = header_value.split(",")
    _, timestamp = components[0].strip().split("=")

    return timestamp


@app.route("/", methods=["POST"])
def receive_webhook_request() -> Response:
    received_signature = request.headers.get(SIGNATURE_HEADER_NAME)
    timestamp = parse_timestamp(received_signature)

    computed_signature = compute_signature(
        validation_key=VALIDATION_KEY,
        body=request.data,
        timestamp=timestamp,
    )
    signature_is_valid = hmac.compare_digest(received_signature, computed_signature)

    print(f"{signature_is_valid=}", flush=True)
    return (
        jsonify({"signature_is_valid": signature_is_valid}),
        200 if signature_is_valid else 401,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
