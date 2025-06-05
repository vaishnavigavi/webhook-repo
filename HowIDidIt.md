# Webhook Assignment: How I Completed It

## Overview
I built a Flask-based webhook server to receive and validate external events, stored them in MongoDB, and created a simple React dashboard to display recent events. To expose the local server publicly for testing, I used ngrok. CI/CD automation was handled via GitHub Actions, and deployments were done to a small VPS.

---

## 1. Project Setup

- Repository and Environment-  
  I initialized a new GitHub repository and created a virtual environment. Environment variables (database URI, webhook secret) were defined in a local `.env` file and never committed to version control.

- Ngrok for Public Endpoint-
  To allow external services (e.g., GitHub webhooks) to reach my locally running Flask server, I installed ngrok and established a tunnel. This gave me a publicly accessible URL that forwarded incoming HTTP requests to my local development port.

---

## 2. Webhook Server Implementation

- Signature Validation-
  Incoming POST requests pass through a validation step that verifies the request signature against the shared secret. If validation fails, the server returns an unauthorized response; otherwise, it processes the payload.

- Payload Validation-
  Before inserting any data into MongoDB, I validated the JSON structure against a predefined schema. This ensured that required fields were present and of the correct type, guarding against malformed requests.

- Database Integration-
  I connected to a local (and later remote) MongoDB instance. Each valid webhook event is saved as a document, including fields such as event type, timestamp, raw payload, and a “processed” flag. I also added an index to speed up queries for unprocessed events.

- Concurrency Considerations-
  To handle bursts of incoming requests, I implemented a simple batching mechanism: when multiple events arrived in quick succession, they were grouped and inserted together to reduce database overhead.

---

## 3. React Dashboard

- Polling for Recent Events-
  I created a lightweight React application that periodically fetched the latest events from the API. Every few seconds, the dashboard retrieved a limited set of recent entries and displayed them in a scrolling table.

- Efficient Rendering-
  To ensure smooth performance even when many events accumulated, I used a table virtualization technique. This kept the UI responsive by only rendering the rows currently visible in the viewport.

- CORS Configuration- 
  Since the dashboard ran on a different port during development, I configured the Flask server to allow requests only from the React application’s origin. In production, I restricted CORS to the dashboard’s deployed domain.

---

## 4. CI/CD and Deployment

- GitHub Actions Workflow-
  I set up a continuous integration workflow that ran on every push and pull request to the main branch. This pipeline:
  1. Started a MongoDB service in the runner.
  2. Installed backend dependencies, ran lint checks, and executed unit tests.
  3. Built the React frontend to verify there were no errors.

- Manual Deployment Workflow-
  For staging, I created a separate workflow that could be triggered on demand. It built a Docker image of the Flask server, pushed it to Docker Hub, then connected via SSH to the VPS, pulled the new image, and restarted the container with the updated code.

- Environment Variables and Secrets- 
  Sensitive information—such as database credentials, webhook secret, SSH keys, and Docker Hub tokens—were stored as encrypted GitHub Secrets. Locally, I used a `.env` file.

---

## 5. Security and Best Practices

- Signature Verification- 
  I supported multiple signing algorithms, so the server could validate HMAC-SHA256 or RSA-based signatures depending on the webhook provider. Invalid signatures were logged and rejected immediately.

- Rate Limiting- 
  To guard against abuse or accidental floods, I implemented an in-memory rate limiter that temporarily blocked any IP making too many requests within a short time window.

- Input Sanitization- 
  By using schema validation, I prevented any unexpected or malicious fields from reaching the database. All data inserted into MongoDB was a validated dictionary, never constructed via string interpolation.

- CORS Restrictions-  
  During development, only the local React port was allowed. In production, I limited access to the actual dashboard domain. This prevented unauthorized cross-origin calls.

---

## 6. Testing Strategy

- Backend Tests-
  I used a test runner to cover core functionality:
  - Signature-validation logic with both valid and invalid headers.
  - Schema-validation errors for malformed JSON.
  - Database insertion and flagging of “processed” events.
  A temporary MongoDB instance was spun up in each test run to isolate test data.

- Frontend Tests-  
  The React app included a handful of tests that:
  - Verified the dashboard component rendered without crashing.
  - Mocked API responses to confirm table rows appeared as expected.

- Coverage and Speed-
  By focusing on unit tests rather than full end-to-end integration tests, I kept CI times under one minute while still achieving high coverage on critical paths.

---

## 7. Ngrok Integration

- Tunnel Setup-
  I launched an ngrok tunnel pointed at the local Flask port. Ngrok provided a stable, randomly generated URL (e.g., `https://abcd1234.ngrok.io`) that I registered as the webhook endpoint in external settings.

- Automatic Tunnel Refresh-
  Every time I restarted the Flask server, I also restarted ngrok. To make this easier, I kept a simple note reminding myself to copy the new URL into the webhook configuration of any service (e.g., GitHub) before running tests.

- Local vs. Production-
  In development, ngrok ensured I could test end-to-end without deploying. Once the code was ready for staging, I replaced the ngrok URL with the VPS domain in the webhook settings and disabled ngrok.

---


## 8. Summary of My Workflow

1. Initialize repository: and set up environment variables.  
2. Implement Flask server: validate signatures, enforce schema, store events in MongoDB.  
3. Expose local server via ngrok to test external webhook deliveries.  
4. Create React dashboard: poll API, render recent events, and optimize for large data sets.  
5. Configure GitHub Actions: run Cypress checks, Python lint/tests, and React build steps.  
6. Deploy to staging by building a Docker image, pushing it to Docker Hub, and restarting the container on the VPS.  
7. Iterate on security: add rate limiting, strict CORS, and signature verification for multiple signing algorithms.  
8. Write tests to cover core functionality and keep CI fast.  

This process gave me a reliable, end-to-end webhook solution—accessible locally via ngrok and automatically tested and deployed through CI/CD. ```
