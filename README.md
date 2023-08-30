# Testing Webhook Validation Key

- Install Docker and ngrok

- Run the flask app

```bash
docker-compose up
```

- Expose flask app to the internet:

```bash
ngrok http 8000
```

- Create a new webhook subscription with the URL that ngrok gives set as an endpoint.

- Change the value of SIGNATURE_HEADER_NAME and VALIDATION_KEY to the correct values.

- Trigger some events, and you should see "signature_is_valid=True" in the logs
