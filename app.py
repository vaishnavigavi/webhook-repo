from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
db = client['github_webhooks']
collection = db['events']

@app.route('/')
def index():
    logger.debug("Accessing index page")
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    logger.debug(f"Received webhook request: {request.headers}")
    if request.headers.get('X-GitHub-Event') not in ['push', 'pull_request']:
        logger.warning(f"Unsupported event type: {request.headers.get('X-GitHub-Event')}")
        return jsonify({'error': 'Unsupported event type'}), 400

    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    logger.debug(f"Processing {event_type} event")
    
    # Extract common fields
    author = data['sender']['login']
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    if event_type == 'push':
        # Handle push event
        request_id = data['head_commit']['id']
        to_branch = data['ref'].split('/')[-1]
        from_branch = to_branch  # For push events, from and to are the same
        
        event_data = {
            'request_id': request_id,
            'author': author,
            'action': 'PUSH',
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp
        }
        
    elif event_type == 'pull_request':
        # Handle pull request event
        request_id = str(data['pull_request']['number'])
        from_branch = data['pull_request']['head']['ref']
        to_branch = data['pull_request']['base']['ref']
        
        # Determine if it's a merge or pull request
        action = 'MERGE' if data['action'] == 'closed' and data['pull_request']['merged'] else 'PULL_REQUEST'
        
        event_data = {
            'request_id': request_id,
            'author': author,
            'action': action,
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp
        }
    
    # Store in MongoDB
    collection.insert_one(event_data)
    logger.debug(f"Stored event: {event_data}")
    
    return jsonify({'message': 'Webhook processed successfully'}), 200

@app.route('/events', methods=['GET'])
def get_events():
    logger.debug("Fetching events")
    events = list(collection.find({}, {'_id': 0}).sort('timestamp', -1))
    return jsonify(events)

@app.route('/test')
def test():
    return "Test route is working!", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050) 