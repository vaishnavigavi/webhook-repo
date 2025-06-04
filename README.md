# GitHub Webhook Receiver

This application receives GitHub webhooks for push, pull request, and merge events, stores them in MongoDB, and displays them in a real-time UI.

## Prerequisites

- Python 3.8+
- MongoDB
- GitHub account

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your MongoDB connection string:
   ```
   MONGODB_URI=mongodb://localhost:27017/
   ```

## Running the Application

1. Start MongoDB if it's not already running
2. Run the Flask application:
   ```bash
   python app.py
   ```
3. Open `http://localhost:5000` in your browser

## Setting up GitHub Webhooks

1. Go to your GitHub repository settings
2. Navigate to Webhooks
3. Add a new webhook:
   - Payload URL: `http://your-domain/webhook`
   - Content type: `application/json`
   - Events: Select "Push" and "Pull request" events
   - Secret: (optional) Add a secret for additional security

## Features

- Receives GitHub webhook events for push, pull request, and merge actions
- Stores events in MongoDB with proper schema
- Real-time UI updates every 15 seconds
- Clean and minimal design
- Supports all required event types:
  - Push events
  - Pull request events
  - Merge events

## API Endpoints

- `POST /webhook`: Receives GitHub webhook events
- `GET /events`: Returns all stored events sorted by timestamp 