from flask import Flask, render_template, send_from_directory, request, send_file
from PIL import Image, ImageDraw, ImageFont
import random
import io
app = Flask(__name__, template_folder="src", static_folder="src")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/captcha', methods=['GET'])
def generate_captcha():
    captcha_text = request.args.get('txt', '')

    font_size = 60
    font = ImageFont.truetype("src/captcha.otf", font_size)

    total_text_width = len(captcha_text) * font_size

    image = Image.new('RGB', (total_text_width, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(image)
    
    x = (image.width + 20 - total_text_width) / 2
    
    y = (image.height - font_size) / 2
    
    char_width_estimate = font_size * 1
    
    for char in captcha_text:
        text_color = (random.randint(0, 192), random.randint(0, 192), random.randint(0, 192))
        d.text((x, y), char, fill=text_color, font=font)
        x += char_width_estimate

    for _ in range(100):
        d.point((random.randint(0, 400), random.randint(0, 100)), fill=(0, 0, 0))

    img_buffer = io.BytesIO()
    image.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype='image/png')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)