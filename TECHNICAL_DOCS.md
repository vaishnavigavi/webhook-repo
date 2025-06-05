# Technical Documentation: GitHub Events Monitor

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Webhook Server (webhook-repo)](#webhook-server)
3. [GitHub Repository (action-repo)](#github-repository)
4. [Database Schema](#database-schema)
5. [API Endpoints](#api-endpoints)
6. [Frontend Implementation](#frontend-implementation)
7. [Security Implementation](#security-implementation)
8. [Testing and Deployment](#testing-and-deployment)

## System Architecture

### Overview
The system follows a client-server architecture with the following components:

```
GitHub Repository (action-repo)
         ↓
GitHub Actions Workflow
         ↓
Webhook Server (webhook-repo)
         ↓
MongoDB Database
         ↓
Web UI (Auto-refreshing)
```

### Data Flow
1. GitHub events trigger Actions workflow
2. Workflow sends event data to webhook server
3. Server processes and stores data in MongoDB
4. Web UI polls server every 15 seconds
5. UI updates with new events

## Webhook Server

### Core Components

#### 1. Flask Application (`app.py`)
```python
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client.github_events
events = db.events
```

Key features:
- CORS enabled for cross-origin requests
- MongoDB connection using environment variables
- Database and collection initialization

#### 2. Webhook Endpoint
```python
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('X-GitHub-Event') == 'push':
        data = request.json
        event = {
            'type': 'PUSH',
            'author': data['pusher']['name'],
            'branch': data['ref'].split('/')[-1],
            'timestamp': datetime.utcnow()
        }
        events.insert_one(event)
        return jsonify({'status': 'success'}), 200
```

Event processing:
- Validates GitHub event type
- Extracts relevant information
- Stores in MongoDB with timestamp
- Returns success response

#### 3. Events Endpoint
```python
@app.route('/events')
def get_events():
    all_events = list(events.find({}, {'_id': 0}).sort('timestamp', -1))
    return jsonify(all_events)
```

Features:
- Retrieves all events from MongoDB
- Sorts by timestamp (newest first)
- Excludes MongoDB _id field
- Returns JSON response

## GitHub Repository

### GitHub Actions Workflow

#### 1. Workflow Configuration (`webhook.yml`)
```yaml
name: Send Webhook

on:
  push:
    branches: [ main ]
  pull_request:
    types: [opened, closed]
  pull_request_target:
    types: [closed]

jobs:
  send-webhook:
    runs-on: ubuntu-latest
    steps:
      - name: Send webhook
        run: |
          curl -X POST ${{ secrets.WEBHOOK_URL }} \
            -H "Content-Type: application/json" \
            -H "X-GitHub-Event: ${{ github.event_name }}" \
            -d '${{ toJSON(github.event) }}'
```

Features:
- Triggers on push, PR open/close
- Uses GitHub secrets for webhook URL
- Sends event data as JSON
- Includes GitHub event type header

## Database Schema

### Events Collection
```javascript
{
    type: String,      // "PUSH", "PULL_REQUEST", "MERGE"
    author: String,    // GitHub username
    branch: String,    // Branch name
    timestamp: Date    // UTC timestamp
}
```

Indexes:
- `timestamp`: -1 (descending) for efficient sorting
- `type`: 1 for filtering by event type

## Frontend Implementation

### 1. HTML Structure (`index.html`)
```html
<!DOCTYPE html>
<html>
<head>
    <title>GitHub Events Monitor</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>GitHub Events Monitor</h1>
        <div class="stats">
            <!-- Statistics cards -->
        </div>
        <div class="search-filter">
            <!-- Search and filter controls -->
        </div>
        <div class="events">
            <!-- Event list -->
        </div>
    </div>
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
```

### 2. JavaScript Implementation (`script.js`)
```javascript
// Auto-refresh implementation
function refreshEvents() {
    fetch('/events')
        .then(response => response.json())
        .then(events => {
            updateUI(events);
            updateStats(events);
        });
}

// Update every 15 seconds
setInterval(refreshEvents, 15000);
```

Features:
- Real-time updates
- Event filtering
- Statistics calculation
- Error handling

### 3. CSS Styling (`style.css`)
```css
:root {
    --primary-color: #0366d6;
    --secondary-color: #24292e;
    --background-color: #ffffff;
    --text-color: #24292e;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    :root {
        --background-color: #1a1a1a;
        --text-color: #ffffff;
    }
}
```

Features:
- CSS variables for theming
- Dark mode support
- Responsive design
- Modern animations

## Security Implementation

### 1. Environment Variables
```bash
# .env file
MONGODB_URI=mongodb://localhost:27017/
FLASK_ENV=development
FLASK_DEBUG=1
```

### 2. CORS Configuration
```python
CORS(app, resources={
    r"/webhook": {"origins": "*"},
    r"/events": {"origins": "*"}
})
```

### 3. GitHub Secrets
- `WEBHOOK_URL`: Securely stored webhook endpoint
- Environment-specific configuration

## Testing and Deployment

### 1. Local Testing
```bash
# Start MongoDB
mongod

# Start Flask server
python app.py

# Start ngrok
ngrok http 5050
```

### 2. GitHub Actions Testing
1. Push to repository
2. Check Actions tab
3. Verify webhook delivery
4. Check UI updates

### 3. Monitoring
- Check MongoDB logs
- Monitor Flask server
- Watch ngrok traffic
- Verify GitHub Actions

## Error Handling

### 1. Server-side
```python
@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({
        'error': str(error),
        'status': 'error'
    }), 500
```

### 2. Client-side
```javascript
function handleError(error) {
    console.error('Error:', error);
    showErrorNotification();
}
```

## Performance Considerations

1. **Database**
   - Indexed queries
   - Efficient sorting
   - Connection pooling

2. **Frontend**
   - Debounced search
   - Efficient DOM updates
   - Cached responses

3. **API**
   - Rate limiting
   - Response compression
   - Connection keep-alive

## Future Improvements

1. **Authentication**
   - JWT implementation
   - OAuth integration
   - Role-based access

2. **Real-time Updates**
   - WebSocket implementation
   - Server-sent events
   - Long polling fallback

3. **Scalability**
   - Load balancing
   - Database sharding
   - Caching layer

## Contributing Guidelines

1. **Code Style**
   - PEP 8 for Python
   - ESLint for JavaScript
   - Prettier for formatting

2. **Testing**
   - Unit tests
   - Integration tests
   - End-to-end tests

3. **Documentation**
   - Code comments
   - API documentation
   - Setup instructions 