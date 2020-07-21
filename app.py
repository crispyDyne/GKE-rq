import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/hello')
def hello():
    """Test endpoint"""
    return {'hello': 'world'}


if __name__ == '__main__':
	app.run(
        debug=True, 
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 8080)),
        # threaded=False,
        # processes=50
    )