import os
from flask import Flask, send_from_directory, request
from dotenv import load_dotenv, dotenv_values
import whisper

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
            'message': 'Success fetching the API',
        },
        'data': None
    }, 200

@app.route('/transcribe', methods=['GET', 'POST']) # Ajax
def processRoute():
        if request.method == "POST":
            if 'audio_file' not in request.files:
                return {
                    'status': {
                        'code': 400,
                        'error': 'no_audio_file',
                    },
                    'data': None
                }, 400
            else:
                audio_file = request.files['audio_file']

                if audio_file:
                    file_path = os.path.join(os.path.dirname(__file__), 'uploads', audio_file.filename)
                    audio_file.save(file_path)
                    model = whisper.load_model("medium")
                    result = model.transcribe(file_path)
                    transcribed_text = result['text']
                return {
                    'status': {
                        'code': 201,
                        'message': 'Success processing the audio',
                    },
                    'data': {
                        'audio_file': request.files['audio_file'].filename,
                        'result': transcribed_text
                    }
                }
        else:
            return {
                'status': {
                    'code': 200,
                    'message': 'Success fetching the API',
                },
                'data': None
            }, 200

@app.route('/transcribes')
@app.route('/transcribes/<id>') # Ajax
def transcribesRoute(id=""):
    returnedData = {
        'status': {
            'code': 200,
            'message': 'Success fetching the API',
        },
        'data': {
            'id': id
        }
    }
    if id == "":
        returnedData['status']['data'] = None
    return returnedData, 200
    

@app.route('/analytics') # Ajax
def analyticsRoute():
    return {
        'status': {
            'code': 200,
            'note': 'Success fetching the API',
        },
        'data': None if (len(request.args) == 0) else {
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