from flask import Flask, render_template, request, url_for, jsonify, redirect, send_from_directory
from tester import ask_perplexity, insert_perplexity
from texttosspeech import tts, save_audio, play_audio
import speech_recognition as sr
import os
from pydub import AudioSegment
import logging
# import soundfile
# import wave

# Initialize the Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/audio'
ALLOWED_EXTENSIONS = {'wav'}
AUDIO_DIRECTORY = 'static/audio'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_audio_to_wav(file_path):
    """Convert the audio file to a standard PCM WAV format."""
    sound = AudioSegment.from_file(file_path)
    wav_path = file_path.rsplit('.', 1)[0] + '.wav'
    # Ensure mono channel, 16-bit, and 16kHz sample rate
    sound = sound.set_channels(1).set_frame_rate(16000).set_sample_width(2)
    sound.export(wav_path, format='wav')
    return wav_path

def transcribe_audio(file_path):
    # data, samplerate = soundfile.read(file_path)
    # new_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'audio.wav')
    # soundfile.write(new_filename, data, samplerate, subtype='PCM_16')
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 386
    # ChatGPT version
    file_path = convert_audio_to_wav(file_path)
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
    # with wave.open(file_path, 'rb') as wf:
    #     audio_data = wf.readframes(wf.getnframes())
    #     audio = sr.AudioData(audio_data, wf.getframerate(), wf.getsampwidth())

    #     try:
    #         text = recognizer.recognize_google(audio)
            return text, 0
        except sr.UnknownValueError:
            return "Could not understand audio", 1
        except sr.RequestError as e:
            return f"Could not request results; {e}", 1

def parse_reply(reply):
    out = ''.join([i for i in reply if (i.isalpha() or i.isspace() or i in [',', '.', '?', '!', "'", "-", ";", "+", "=", "*"])])
    return out

# Define the home route with a form
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        return render_template('result.html', name=name, message=message)
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    if 'file' not in request.files:
        return jsonify({'response': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'response': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # logging.info(f'File saved to {file_path}')
        status = 1
        transcription, status = transcribe_audio(file_path)
        # logging.info(f'Transcribed text: {transcription}')
        user_input = transcription
        reply = None
        if (status == 0):
            response = ask_perplexity(transcription)
            reply, citation = response
            reply = parse_reply(reply)
            audio = tts(reply)
            save_audio(audio, os.path.join(app.config['UPLOAD_FOLDER'], 'reply.mp3'))
            play_audio(audio)
        if (status != 0):
            user_input = 'Please record it again.'
        
        return jsonify({'user_input': user_input, 'status': status, 'response': reply, 'audio_filename': os.path.join(app.config['UPLOAD_FOLDER'], 'reply.mp3')})

@app.route('/updateparams', methods=['POST'])
def updateparams():
    if request.method == 'POST':
        company = request.form['company']
        field = request.form['field']
        role = request.form['role']
        insert_perplexity("Your name is Connor. Your role is an interviewer at {}. Please initiate the interview by introducing yourself, and telling the candidate the structure of the interview. Wait for the candidate confirmation before asking technical questions. The topic is {}. The candidate is interviewing for job {}. Do not apologize unnecessarily!".format(company, field, role))
        print(company, flush=True)
        return render_template('index.html', company=company, field=field, role=role)
    return redirect(url_for('home'))

# @app.route('/audio/<filename>')
# def serve_audio(filename):
#     return send_from_directory(AUDIO_DIRECTORY, filename, as_attachment=True, mimetype='audio/mp3')

# Additional route example
@app.route('/about')
def about():
    return render_template('about.html')

# The main function to run the app
if __name__ == '__main__':
    app.run(debug=False)



# import os
# import logging
# from flask import Flask, render_template, request, jsonify
# from tester import ask_perplexity
# import speech_recognition as sr
# from pydub import AudioSegment

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'static/audio'
# ALLOWED_EXTENSIONS = {'wav', 'mp3'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def transcribe_audio(file_path):
#     recognizer = sr.Recognizer()
#     # Convert MP3 to WAV for compatibility with speech_recognition
#     if file_path.endswith('.mp3'):
#         sound = AudioSegment.from_mp3(file_path)
#         file_path = file_path.replace('.mp3', '.wav')
#         sound.export(file_path, format='wav')

#     with sr.AudioFile(file_path) as source:
#         audio = recognizer.record(source)
#         try:
#             text = recognizer.recognize_google(audio)
#             return text
#         except sr.UnknownValueError:
#             return "Could not understand audio"
#         except sr.RequestError as e:
#             return f"Could not request results; {e}"

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/ask', methods=['POST'])
# def ask():
#     if 'file' not in request.files:
#         return jsonify({'response': 'No file part'}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'response': 'No selected file'}), 400

#     if file and allowed_file(file.filename):
#         filename = file.filename
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
#         logging.info(f'File saved to {file_path}')

#         transcription = transcribe_audio(file_path)
#         logging.info(f'Transcribed text: {transcription}')

#         user_input = transcription
#         response = ask_perplexity(transcription)
#         reply, citation = response
#         return jsonify({'response': response})

#     return jsonify({'response': 'Invalid file type'}), 400

# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     app.run(debug=True)





