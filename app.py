import os
from flask import Flask, request, render_template, redirect, url_for
from colorthief import ColorThief # Importing ColorThief class from colorthief library
import io # Importing the io module to handle byte streams
from urllib.request import urlopen # For Python 3, import urlopen from urllib.request

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if an image file is uploaded
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            # Save the uploaded image
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Use ColorThief to extract colors
            color_thief = ColorThief(filepath)
            dominant_color = color_thief.get_color(quality=10)
            palette = color_thief.get_palette(quality=10)

            image_url = url_for('static', filename='uploads/' + file.filename)

            

            return render_template('index.html', dominant_color=dominant_color, palette=palette, image_url=image_url)
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
