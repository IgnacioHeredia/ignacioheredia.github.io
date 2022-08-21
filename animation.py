"""
Create animated icon (beating heart)

Frames are saved in `demo` folder. Then mp4 video can be created with ffmpeg.

    ffmpeg -framerate 45 -pattern_type glob -i '*.png' -c:v libx264 -pix_fmt yuv420p -crf 10 icon.mp4
"""


from PIL import Image, ImageOps
import numpy as np

fp_in = "icon-crop-square-light.png"
bk_color = (48, 44, 44)  # background color of the webpage
mr = 1.07  # max downscaling ratio
nframes = 100  # number of frames (actual frames is the double of this number)


ori = Image.open(fp_in)
h, w = ori.size

# Remove alpha channel because if not frames are going to be melting
background = Image.new('RGBA', ori.size, bk_color)
ori = Image.alpha_composite(background, ori.convert('RGBA'))

# Create frames
imgs = []
for r in np.linspace(1, mr, nframes):
    tmp_size = (int(h/r), int(w/r))
    tmp_img = ori.resize(tmp_size)
    tmp_img = ImageOps.expand(
        tmp_img,
        border= int((h-tmp_size[0])/2),
        fill=bk_color,
    )
    imgs.append(tmp_img)
    
imgs = imgs + imgs[::-1][::5]  # add growing back phase

for i, img in enumerate(imgs):
    img.save(f'demo/{i:03d}.png')
