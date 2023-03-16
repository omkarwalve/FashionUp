from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
import requests
from colorthief import ColorThief
import matplotlib.pyplot as plt
import colorsys
import numpy as np
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'C:/Users/Dell/Desktop'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}




app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def get_contrast_ratio(color1, color2):
    # Convert colors to sRGB
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    
    # Calculate relative luminance of each color
    def get_relative_luminance(color):
        if color <= 0.03928:
            return color / 12.92
        else:
            return ((color + 0.055) / 1.055) ** 2.4
    
    l1 = 0.2126 * get_relative_luminance(r1) + 0.7152 * get_relative_luminance(g1) + 0.0722 * get_relative_luminance(b1)
    l2 = 0.2126 * get_relative_luminance(r2) + 0.7152 * get_relative_luminance(g2) + 0.0722 * get_relative_luminance(b2)
    
    # Calculate contrast ratio
    if l1 > l2:
        return (l1 + 0.05) / (l2 + 0.05)
    else:
        return (l2 + 0.05) / (l1 + 0.05)

@app.route('/fashionIndex', methods=['GET', 'POST'])
def fashionIndex():
     if request.method == 'GET':
       button = "#about"
       return render_template('home.html',button=button)
     if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        #file = request.files.get('file')
        
        if not file:
            return render_template('home.html')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        url = r"C:\Users\Dell\Desktop\ " + filename
        url = url.replace(" ","")
        ct = ColorThief(url)
        average_color = ct.get_color()
        print(f"average color is {average_color}")

# Scale the average color to the valid range
        # average_color = np.array(average_color).astype(np.float32) / 255.0
        # print(f'average color are {average_color}')
        # plt.imshow([[average_color]])
        # plt.show()

        palette = ct.get_palette(color_count=5)
        print(f"palette is {palette}")

# Scale the palette colors to the valid range
        # palette = np.array(palette).astype(np.float32) / 255.0
        # print(palette)
        # print(np.array(palette).astype(np.float32)*10)
        # print(f'palette color are {palette}')
        # plt.imshow([palette])
        # plt.show()

# Convert RGB color to HSL color
        h, s, l = colorsys.rgb_to_hls(*average_color)
        print(s)
        

# Get contrasting colors by adding/subtracting a fixed value from the Lightness value
        contrasting_color1 = colorsys.hls_to_rgb(h, s, min(l + 0.1, 5.0))
        contrasting_color2 = colorsys.hls_to_rgb(h, s, max(l - 0.5, 0.0))
        contrasting_color3 = colorsys.hls_to_rgb(h, min(s + 0.1, 8.0), l)

        contrasting_color4 = colorsys.hls_to_rgb(h + 0.6, s, min(l + 0.4, 1.0))
        contrasting_color5 = colorsys.hls_to_rgb(h + 0.2, s, max(l + 11.3, 0.0))
        contrasting_color6 = colorsys.hls_to_rgb(h + 0.4, min(s - 100, 50.0), l+0.2)

        contrasting_color7 = colorsys.hls_to_rgb(h - 0.6, s, min(l + 0.4, 1.0))
        contrasting_color8 = colorsys.hls_to_rgb(h + 1.5, s, max(l + 11.3, 0.0))
        contrasting_color9 = colorsys.hls_to_rgb(h + 1.6, min(s - 100, 50.0), l+0.2)



        

# Scale the contrasting colors to the valid range
        # contrasting_colors = np.array([contrasting_color1, contrasting_color2, contrasting_color3]).astype(np.float32)
        # contrasting_colors /= np.max(contrasting_colors)
        contrasting_colors1= (contrasting_color1,contrasting_color2,contrasting_color3)
        contrasting_colors2= (contrasting_color4,contrasting_color5,contrasting_color6)
        contrasting_color3= (contrasting_color7,contrasting_color8,contrasting_color9)
        # print(f'contrasting colors are{contrasting_colors}')

        colors = palette
        ratioArray = []
        for i in range(1,4):
            ratio = get_contrast_ratio(colors[i], colors[i+1])
            while (ratio >= 10):
              ratio = ratio // 10
            print(f"Contrast between {colors[i]} and {colors[i+1]}: {ratio:.2f}")
            ratioArray.append(ratio)
        print(f"ratioArray is {ratioArray}")    
        ratiomean = np.mean(ratioArray)
        print(f"ratio mean is {ratiomean}")
        fashionIndex = "%.2f" % ratiomean
        if float(fashionIndex) > 100:
            fashionIndex=fashionIndex/100.0
        fashionIndex=float(fashionIndex)+5
        if float(fashionIndex) > 10:
            fashionIndex=10
        fashionIndex='%.2f' % fashionIndex

        return render_template('fashionIndex.html', fashionIndex=fashionIndex ,inputcolor=palette, recommendedcolors1=contrasting_colors1,recommendedcolors2=contrasting_colors2,recommendedcolors3=contrasting_color3)

 
@app.route('/', methods=['GET', 'POST'])
def home():


  if request.method == 'GET':
     name="redered successfully"
     button="/fashionIndex"
     return render_template('layout.html', name=name,button=button)
  

  