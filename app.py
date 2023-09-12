from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/info', methods=['GET'])
def get_info():
    # Get query parameters
    slack_name = request.args.get('slack_name', 'Aroso')
    track = request.args.get('track', 'Backend')

    # Get current day of the week
    now = datetime.utcnow()
    current_day = now.strftime('%A')

    # Get current UTC time with validation of +/-2 minutes
    utc_time = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    valid_time_range = now + timedelta(hours=-2), now + timedelta(hours=2)
    if ('since' in request.args) and ('until' in request.args):
        try:
            since = datetime.fromisoformat(request.args['since'])
            until = datetime.fromisoformat(request.args['until'])
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
        if (since < valid_time_range[0]) or (until > valid_time_range[1]):
            return jsonify({'error': 'Date range is out of valid time range'}), 400

    # Define GitHub URLs
    github_file_url = "https://github.com/username/repo/blob/main/file_name.ext"
    github_repo_url = "https://github.com/username/repo"

    # Prepare the response JSON
    response = {
        "slack_name": slack_name,
        "current_day": current_day,
        "utc_time": utc_time,
        "track": track,
        "github_file_url": github_file_url,
        "github_repo_url": github_repo_url,
        "status_code": 200
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
