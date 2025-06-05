# GitHub Events Monitor

A real-time GitHub events monitoring system that captures and displays push, pull request, and merge events from your repositories.

## Project Overview

This project consists of two main components:

1. **Webhook Server** (`webhook-repo`): A Flask application that receives GitHub webhooks and stores events in MongoDB
2. **GitHub Repository** (`action-repo`): A repository with GitHub Actions workflow that sends events to the webhook server

## Features

- 🔄 Real-time event monitoring
- 📊 Beautiful, responsive UI
- 🔍 Search and filter events
- 📈 Event statistics dashboard
- 🌙 Dark mode support
- ⚡ 15-second auto-refresh
- 🔒 Secure webhook handling

## System Architecture

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

## Components

### 1. Webhook Server (webhook-repo)

#### Technologies Used
- Flask (Python web framework)
- MongoDB (Database)
- Flask-CORS (Cross-Origin Resource Sharing)
- Python-dotenv (Environment variables)

#### Key Files
- `app.py`: Main Flask application
- `templates/index.html`: Web UI
- `.env`: Environment configuration
- `requirements.txt`: Python dependencies

#### API Endpoints
- `GET /`: Serves the web UI
- `POST /webhook`: Receives GitHub webhook events
- `GET /events`: Returns all stored events

### 2. GitHub Repository (action-repo)

#### Components
- GitHub Actions workflow
- Sample files for testing
- Webhook configuration

#### Workflow Features
- Triggers on push, pull request, and merge events
- Sends event data to webhook server
- Uses GitHub Secrets for secure configuration

## Setup Instructions

### 1. Webhook Server Setup

```bash
# Clone the repository
git clone <webhook-repo-url>
cd webhook-repo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your MongoDB URI

# Run the server
python app.py
```

### 2. GitHub Repository Setup

1. Create a new repository on GitHub
2. Add the following secrets in repository settings:
   - `WEBHOOK_URL`: Your webhook server URL (e.g., ngrok URL + /webhook)
3. Push the workflow file to `.github/workflows/webhook.yml`

### 3. Testing the Integration

1. Start the webhook server
2. Start ngrok to expose your local server:
   ```bash
   ngrok http 5050
   ```
3. Update the `WEBHOOK_URL` secret with the new ngrok URL
4. Make changes to the repository to trigger events

## UI Features

### 1. Event Display
- Shows author, action type, branches, and timestamp
- Color-coded badges for different event types
- Hover effects and animations

### 2. Search and Filter
- Search by author or branch name
- Filter by event type (Push, PR, Merge)
- Real-time filtering

### 3. Statistics Dashboard
- Total events count
- Push events count
- Pull request count
- Merge count

### 4. Auto-refresh
- Updates every 15 seconds
- Shows last update time
- Loading indicators

## Event Types

### 1. Push Events
- Triggered when code is pushed to any branch
- Shows author and target branch

### 2. Pull Request Events
- Triggered when a PR is created
- Shows author, source branch, and target branch

### 3. Merge Events
- Triggered when a PR is merged
- Shows author and merged branches

## Security Features

1. **GitHub Secrets**
   - Secure storage of webhook URL
   - Environment-specific configuration

2. **CORS Configuration**
   - Properly configured for webhook endpoints
   - Secure cross-origin requests

3. **Environment Variables**
   - Sensitive data stored in .env file
   - Not committed to repository

## Development

### Local Development
1. Run Flask in debug mode
2. Use ngrok for webhook testing
3. Monitor MongoDB for data storage

### Testing
1. Make changes to action-repo
2. Watch events appear in UI
3. Verify statistics update
4. Test search and filters

## Troubleshooting

### Common Issues
1. **Webhook Not Receiving Events**
   - Check ngrok URL is correct
   - Verify GitHub secret is updated
   - Check Flask server is running

2. **UI Not Updating**
   - Check browser console for errors
   - Verify MongoDB connection
   - Check network requests

3. **MongoDB Connection Issues**
   - Verify MongoDB is running
   - Check connection string in .env
   - Check network connectivity

## Future Improvements

1. **Authentication**
   - Add user authentication
   - Secure API endpoints

2. **Additional Features**
   - Event notifications
   - Custom webhook endpoints
   - More event types

3. **Performance**
   - Pagination for large datasets
   - Caching for better performance
   - WebSocket for real-time updates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use this project for your own purposes! 