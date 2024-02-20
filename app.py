import os
from flask import Flask, send_from_directory, request
from dotenv import load_dotenv, dotenv_values

load_dotenv()

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def rootRoute():
    return {
        'status': {
            'code': 200,
            'msg': 'Root route of Speech Analytics by Braincore.id, will be used for the FE'
        }
    }, 200

@app.route('/process', methods=['GET', 'POST']) # Ajax
def processRoute():
        if request.method == "POST":
            if 'audio_file' not in request.files:
                return {
                    'status': {
                        'code': 400,
                        'error': 'no_audio_file',
                    }
                }, 400
            else:
                return {
                    'status': {
                        'code': 201,
                        'msg': 'success',
                        'audio_file': request.files['audio_file'].filename
                    }
                }
        else:
            return {
                'status': {
                    'code': 200,
                    'msg': 'Process route of Speech Analytics by Braincore.id to process the speech',
                    'note': 'This is GET, the POST must have multipart/form-data'
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
    if id == "":
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
    if (os.getenv('STAGE') == 'test'):
        app.run(debug=True, host="0.0.0.0", port=8000)
    elif (os.getenv('STAGE') == 'dev'):
        app.run(debug=True, host="0.0.0.0", port=8001)
    else:
        app.run(debug=True, host="0.0.0.0", port=80)