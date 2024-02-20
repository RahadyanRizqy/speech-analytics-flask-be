import os
from flask import Flask, request
from dotenv import load_dotenv, dotenv_values

load_dotenv()

app = Flask(__name__)

@app.route("/")
def rootRoute():
    return {
        'status': {
            'code': 200,
            'msg': 'Root route of Speech Analytics by Braincore.id, should have the FE'
        }
    }, 200

@app.route('/process', methods=['GET', 'POST']) # Ajax
def processRoute():
        return {
            'status': {
                'code': 200,
                'msg': 'Process route of Speech Analytics by Braincore.id to process the speech',
                'note': 'This is GET, the POST must have data'
            }
        }, 200

@app.route('/transcribes')
@app.route('/transcribes/<id>') # Ajax
def transcribesRoute(id=""):
    returnedData = {
        'status': {
            'code': 200,
            'msg': 'Transcribed from process, fetched from the database, for now it\'s still goign to be dummy',
            'usage': 'Use transcribes/<id>',
            'id': id
        }
    }
    if (id == ""):
        returnedData['status'].pop('id', None)
    return returnedData, 200
    

@app.route('/analytics') # Ajax
def analyticsRoute():
    return {
        'status': {
            'code': 200,
            'msg': 'This route has parameter queries, try to put on it',
            'parameter': request.args
        }
    }

if __name__ == '__main__':
    if (os.getenv('STAGE') == 'dev'):
        app.run(debug=True, host="0.0.0.0", port=8000)
    else:
        app.run(debug=True, host="0.0.0.0", port=80)