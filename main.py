from PIL import Image
import numpy as np
from colormap import rgb2hex
from collections import Counter
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        img = Image.open(file)
        img_array = np.array(img)
        rows, columns, colours = img_array.shape
        vector_len = rows * columns * colours
        pixels = vector_len / 3

        colors = []
        for row in range(rows):
            for column in range(columns//10):
                r = img_array[row, column, :][0]
                g = img_array[row, column, :][1]
                b = img_array[row, column, :][2]

                hex_value = rgb2hex(r, g, b)
                colors.append(hex_value)

        color_freq = dict(Counter(colors))

        color_freq = dict(sorted(color_freq.items(), key=lambda item: item[1], reverse=True))

        color_freq = {k: (v / pixels) * 100 for (k, v) in color_freq.items()}

        if len(color_freq) >= 1000:
            num = 100
        elif 1000 > len(color_freq) > 500:
            num = 50
        elif 500 > len(color_freq) > 300:
            num = 10
        else:
            num = 5

        top_10_colors = [c for c in color_freq.keys()][::num]
        top_10_colors = top_10_colors[
                        :: (len(top_10_colors) // 10) if (len(top_10_colors) // 10) else (len(top_10_colors))]
        return render_template('display1.html', colors=top_10_colors, total_colors=len(color_freq))
    return render_template('display1.html')


if __name__ == '__main__':
    app.run(debug=True)
