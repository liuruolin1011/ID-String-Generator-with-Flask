from flask import Flask, request, render_template
import socket
import os

# Environment configuration
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
PORT = int(os.environ.get('PORT', '5013'))
HOST = os.environ.get('HOST') or socket.gethostbyname(socket.gethostname())

# Application constants
SEARCH_TYPES = [
    'Alert ID',
    'Account ID',
    'Full Name'
]

print(f'Starting server on {HOST}:{PORT}, DEBUG={DEBUG}')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', search_types=SEARCH_TYPES, search_type=None)

@app.route('/generate', methods=['POST'])
def generate():
    search_type = request.form.get('search_type')
    ids = request.form.get('ids', '')
    
    # Validate input
    if not search_type or search_type not in SEARCH_TYPES:
        app.logger.warning(f"Invalid search type: {search_type}")
        return render_template('index.html', 
                              search_types=SEARCH_TYPES, 
                              search_type=None,
                              error="Invalid search type")
    
    # Process IDs
    ids_list = [id.strip() for id in ids.split('\n') if id.strip()]
    if not ids_list:
        return render_template('index.html', 
                              search_types=SEARCH_TYPES, 
                              search_type=search_type,
                              error="No valid IDs provided")
    
    # Format the query
    formatted_ids = [f'"{id}"' for id in ids_list]
    result = f'( [{search_type}] Is {" | ".join(formatted_ids)} )'
    
    return render_template('index.html', 
                          result=result, 
                          search_types=SEARCH_TYPES, 
                          search_type=search_type)

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
