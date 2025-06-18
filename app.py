import os
from flask import Flask, request, jsonify, send_file, render_template
from PIL import Image
import pydub
import moviepy.editor as mp
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Konfigurasi folder output
UPLOAD_FOLDER = 'output'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {
    'image': {'jpg', 'jpeg', 'png', 'bmp', 'gif'},
    'audio': {'mp3', 'wav', 'm4a', 'flac'},
    'video': {'mp4', 'mov', 'avi', 'mkv'}
}

def allowed_file(filename, media_type):
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS[media_type]

def compress_image(input_path, output_path, quality=50):
    try:
        img = Image.open(input_path)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img.save(output_path, format="JPEG", quality=quality, optimize=True)
        return True, f"Image compressed successfully (quality: {quality})"
    except Exception as e:
        return False, f"Error compressing image: {str(e)}"

def decompress_image(input_path, output_path):
    try:
        img = Image.open(input_path)
        img.save(output_path, format="PNG")
        return True, "Image decompressed successfully (saved as PNG)"
    except Exception as e:
        return False, f"Error decompressing image: {str(e)}"

def compress_audio(input_path, output_path, bitrate="128k"):
    try:
        audio = pydub.AudioSegment.from_file(input_path)
        audio.export(output_path, format="mp3", bitrate=bitrate)
        return True, f"Audio compressed successfully (bitrate: {bitrate})"
    except Exception as e:
        return False, f"Error compressing audio: {str(e)}"

def decompress_audio(input_path, output_path):
    try:
        audio = pydub.AudioSegment.from_file(input_path)
        audio.export(output_path, format="wav")
        return True, "Audio decompressed successfully (saved as WAV)"
    except Exception as e:
        return False, f"Error decompressing audio: {str(e)}"

def compress_video(input_path, output_path, crf=28):
    try:
        video = mp.VideoFileClip(input_path)
        video.write_videofile(output_path, codec="libx264", preset="fast", ffmpeg_params=["-crf", str(crf)])
        video.close()
        return True, f"Video compressed successfully (CRF: {crf})"
    except Exception as e:
        return False, f"Error compressing video: {str(e)}"

def decompress_video(input_path, output_path):
    try:
        video = mp.VideoFileClip(input_path)
        video.write_videofile(output_path, codec="libx264", preset="medium", ffmpeg_params=["-crf", "18"])
        video.close()
        return True, "Video decompressed successfully (saved with high quality)"
    except Exception as e:
        return False, f"Error decompressing video: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    media_type = request.form.get('media_type')
    action = request.form.get('action')
    compression_level = request.form.get('compression_level', 'medium')

    if not file or not media_type or not action:
        return jsonify({'error': 'Missing required parameters'}), 400

    if media_type not in ['image', 'audio', 'video']:
        return jsonify({'error': 'Invalid media type'}), 400

    if action not in ['compress', 'decompress']:
        return jsonify({'error': 'Invalid action'}), 400

    if not allowed_file(file.filename, media_type):
        return jsonify({'error': 'File type not allowed'}), 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)

    base_name = os.path.splitext(filename)[0]
    ext = 'jpg' if media_type == 'image' and action == 'compress' else \
          'png' if media_type == 'image' and action == 'decompress' else \
          'mp3' if media_type == 'audio' and action == 'compress' else \
          'wav' if media_type == 'audio' and action == 'decompress' else \
          'mp4'

    output_filename = f"{base_name}_{action}ed.{ext}"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

    # Tentukan parameter berdasarkan tingkat kompresi
    compression_params = {
        'image': {'very_small': 10, 'medium': 50, 'small': 80},
        'audio': {'very_small': '64k', 'medium': '128k', 'small': '256k'},
        'video': {'very_small': 35, 'medium': 28, 'small': 18}
    }

    processors = {
        'image': {'compress': compress_image, 'decompress': decompress_image},
        'audio': {'compress': compress_audio, 'decompress': decompress_audio},
        'video': {'compress': compress_video, 'decompress': decompress_video}
    }

    if action == 'compress':
        param = compression_params[media_type].get(compression_level, compression_params[media_type]['medium'])
        success, message = processors[media_type][action](input_path, output_path, param)
    else:
        success, message = processors[media_type][action](input_path, output_path)

    if success:
        return jsonify({'message': message, 'file': f'/download/{output_filename}'})
    else:
        return jsonify({'error': message}), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)