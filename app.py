import os
from flask import Flask, request, jsonify, send_file, render_template
from PIL import Image
import numpy as np
from werkzeug.utils import secure_filename
import pydub
import moviepy.editor as mp

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

# Fungsi Steganografi LSB
def embed_message(image_path, message, output_path):
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_array = np.array(img)
        h, w, _ = img_array.shape

        # Konversi pesan ke biner
        message += '###'  # Penanda akhir
        binary_message = ''.join(format(ord(c), '08b') for c in message)

        # Cek kapasitas
        max_bits = h * w * 3  # 3 bit per piksel (R, G, B)
        if len(binary_message) > max_bits:
            return False, f"Image too small. Max characters: {max_bits // 8 - 3}"

        # Sisipkan pesan ke LSB
        msg_idx = 0
        for i in range(h):
            for j in range(w):
                for c in range(3):  # R, G, B
                    if msg_idx < len(binary_message):
                        pixel = img_array[i, j, c]
                        pixel = (pixel & ~1) | int(binary_message[msg_idx])
                        img_array[i, j, c] = pixel
                        msg_idx += 1
                    else:
                        break
                if msg_idx >= len(binary_message):
                    break
            if msg_idx >= len(binary_message):
                break

        # Simpan gambar
        Image.fromarray(img_array).save(output_path, format="PNG")
        return True, "Message embedded successfully"
    except Exception as e:
        return False, f"Error embedding message: {str(e)}"

def extract_message(image_path):
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_array = np.array(img)
        h, w, _ = img_array.shape

        binary_message = ""
        max_bits = h * w * 3
        for i in range(h):
            for j in range(w):
                for c in range(3):
                    if len(binary_message) < max_bits:
                        pixel = img_array[i, j, c]
                        binary_message += str(pixel & 1)
                    else:
                        break
                if len(binary_message) >= max_bits:
                    break
            if len(binary_message) >= max_bits:
                break

        # Konversi biner ke teks
        message = ""
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if len(byte) < 8:
                break
            char_code = int(byte, 2)
            if char_code == 0:
                break
            message += chr(char_code)
            if message.endswith('###'):
                message = message[:-3]
                return True, message
        return False, "No message found"
    except Exception as e:
        return False, f"Error extracting message: {str(e)}"

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
    message = request.form.get('message', '')

    if not file or not media_type or not action:
        return jsonify({'error': 'Missing required parameters'}), 400

    if media_type not in ['image', 'audio', 'video']:
        return jsonify({'error': 'Invalid media type'}), 400

    if action not in ['compress', 'decompress', 'embed', 'extract']:
        return jsonify({'error': 'Invalid action'}), 400

    if action == 'embed' and not message:
        return jsonify({'error': 'Message required for embedding'}), 400

    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(input_path)

    base_name = os.path.splitext(filename)[0]
    ext = 'jpg' if media_type == 'image' and action == 'compress' else \
          'png' if media_type == 'image' and action in ['decompress', 'embed', 'extract'] else \
          'mp3' if media_type == 'audio' and action == 'compress' else \
          'wav' if media_type == 'audio' and action == 'decompress' else \
          'mp4'

    output_filename = f"{base_name}_{action}ed.{ext}"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

    compression_params = {
        'image': {'very_small': 10, 'medium': 50, 'small': 80},
        'audio': {'very_small': '64k', 'medium': '128k', 'small': '256k'},
        'video': {'very_small': 35, 'medium': 28, 'small': 18}
    }

    processors = {
        'image': {
            'compress': compress_image,
            'decompress': decompress_image,
            'embed': lambda ip, op: embed_message(ip, message, op),
            'extract': lambda ip, op: extract_message(ip)
        },
        'audio': {'compress': compress_audio, 'decompress': decompress_audio},
        'video': {'compress': compress_video, 'decompress': decompress_video}
    }

    if action == 'compress':
        param = compression_params[media_type].get(compression_level, compression_params[media_type]['medium'])
        success, message = processors[media_type][action](input_path, output_path, param)
    elif action in ['embed', 'extract'] and media_type == 'image':
        success, message = processors[media_type][action](input_path, output_path)
        if action == 'extract':
            return jsonify({'message': message, 'file': None})
    else:
        success, message = processors[media_type][action](input_path, output_path)

    if success and action != 'extract':
        return jsonify({'message': message, 'file': f'/download/{output_filename}'})
    elif success and action == 'extract':
        return jsonify({'message': message, 'file': None})
    else:
        return jsonify({'error': message}), 500

@app.route('/download/<filename>')
def download_file(filename):
    response = send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    return response

if __name__ == '__main__':
    app.run(debug=True)