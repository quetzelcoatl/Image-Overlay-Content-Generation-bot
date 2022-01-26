import os
import random
import string
import time
from functools import reduce

import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import cv2
from matplotlib import pyplot as plt, image as mpimg
from moviepy.editor import *
from spintax import spintax


def text_formatter(message):
    messagelist = []
    temp = ""
    line_size = 0
    letter_count = 0
    for word in message:
        letter_count += 1
        for ele in word:
            letter_count += 1
        if letter_count <= 20:
            temp += word + " "
        else:
            temp = temp[:-1]
            messagelist.append(temp)
            temp = word + " "
            letter_count = 0
    if temp:
        messagelist.append(temp[:-1])
    return messagelist

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str



path = "background_vids/bg1/0uvjttxynebR.mp4"
video = cv2.VideoCapture(path)
length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
rangee = length//2
for i in range(rangee):
    ret, frame = video.read()

bodyPathExactFile = "spintax/0.txt/0.txt"####
textfile = open(bodyPathExactFile, "r", encoding="utf8")
message = ""
for ele in textfile.readline():
    message += ele
spinnedMessage = spintax.spin(message).split(" ")
messagelist = text_formatter(spinnedMessage)
angle = 45

def draw_rotated_text(image, angle, xy, text, fill, *args, **kwargs):
    """ Draw text at an angle into an image, takes the same arguments
        as Image.text() except for:

    :param image: Image to write text into
    :param angle: Angle to write text at
    """
    # get the size of our image
    width, height = image.size
    max_dim = max(width, height)

    # build a transparency mask large enough to hold the text
    mask_size = (max_dim * 2, max_dim * 2)
    mask = Image.new('L', mask_size, 0)

    # add text to mask
    draw = ImageDraw.Draw(mask)
    draw.text((max_dim, max_dim), text, 255, *args, **kwargs)

    if angle % 90 == 0:
        # rotate by multiple of 90 deg is easier
        rotated_mask = mask.rotate(angle)
    else:
        # rotate an an enlarged mask to minimize jaggies
        bigger_mask = mask.resize((max_dim*8, max_dim*8),
                                  resample=Image.BICUBIC)
        rotated_mask = bigger_mask.rotate(angle).resize(
            mask_size, resample=Image.LANCZOS)

    # crop the mask to match image
    mask_xy = (max_dim - xy[0], max_dim - xy[1])
    b_box = mask_xy + (mask_xy[0] + width, mask_xy[1] + height)
    mask = rotated_mask.crop(b_box)

    # paste the appropriate color, with the text transparency mask
    color_image = Image.new('RGBA', image.size, fill)
    image.paste(color_image, mask)

'''def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        global xaxis, yaxis
        xaxis = x * 2
        yaxis = y * 2
        font = cv2.FONT_HERSHEY_SIMPLEX
        font = ImageFont.truetype("arial.ttf", 18)
        halfa = np.asarray(half)
        pillowImage = Image.fromarray(halfa)
        for ele in messagelist:
            draw_rotated_text(pillowImage, angle, (x, y), ele, (128, 255, 128), font=font)

            y += 15
        char_image = np.array(pillowImage, np.uint8)
        cv2.imshow('image', char_image)'''

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        global xaxis, yaxis
        xaxis = x * 2
        yaxis = y * 2
        font = ImageFont.truetype("arial.ttf", 18)
        halfa = np.asarray(half)
        pillowImage = Image.fromarray(halfa)
        draw_rotated_text(pillowImage, angle, (x, y), "Sample Text To View", (128, 255, 128), font=font)
        char_image = np.array(pillowImage, np.uint8)
        cv2.imshow('image', char_image)


'''def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        global xaxis, yaxis
        xaxis = x * 2
        yaxis = y * 2
        font = cv2.FONT_HERSHEY_SIMPLEX
        for ele in messagelist:
            cv2.putText(half, ele, (x, y), font, 0.5, (255, 255, 255), 1.5)
            y += 15

        cv2.imshow('image', half)'''

img = frame
half = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5)
cv2.imshow('image', half)
cv2.setMouseCallback('image', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

global xaxis, yaxis
print("ASDAS", xaxis,yaxis)



'''images = "pix/vrmwlnpdsv.jpg"
#im = Image.open(images)
#im.show()
images = mpimg.imread(images)
imgplot = plt.imshow(images)
plt.show()'''
'''
video = cv2.VideoCapture(path)
while video.isOpened():
    ret, frame = video.read()
    if ret == True:
        #im = cv2.resize(frame, (1080,1920))
        #cv2.imshow('Frame', im)
        filename = "pix/" + get_random_string(10) + ".jpg"
        cv2.imwrite(filename, frame)
    else:
        break


length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
width  = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("length :", length)
print("length :", width)
print("length :", height)

cv2.waitKey(0)'''


'''path = "background_vids/bg1/0pbeipqsuapR.mp4"
vcap = cv2.VideoCapture(path)
width = vcap.get(cv2.CAP_PROP_FRAME_WIDTH )
height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT )
fps =  vcap.get(cv2.CAP_PROP_FPS)

print(width, height, fps)'''


'''#img = cv2.imread('image/output4.png', 1)

from gtts import gTTS
import os
#os.system("pip install -U TTS")
#os.system("tts --list_models")

os.system("tts --text \"P.O.V you just sold a N F T for over $65,000 & earned your professors entire salary after finishing college\" \
    --model_name tts_models/en/ljspeech/glow-tts\
    --vocoder_name vocoder_models/en/ljspeech/hifigan_v2 \
    --out_path output/output2.wav")'''

'''os.system("tts --text \"P.O.V you just sold a N F T for over $65,000 & earned your professors entire salary after finishing college\" \
    --model_name tts_models/en/ljspeech/glow-tts \
    --vocoder_name vocoder_models/en/ljspeech/multiband-melgan \
    --out_path output/output3.wav")

os.system("tts --text \"P.O.V you just sold a N F T for over $65,000 & earned your professors entire salary after finishing college\" \
    --model_name tts_models/en/ljspeech/tacotron2-DDC \
    --vocoder_name vocoder_models/en/ljspeech/hifigan_v2 \
    --out_path output/output4.wav")

os.system("tts --text \"P.O.V you just sold a N F T for over $65,000 & earned your professors entire salary after finishing college\" \
    --model_name tts_models/en/ljspeech/tacotron2-DDC \
    --vocoder_name vocoder_models/en/ljspeech/multiband-melgan \
    --out_path output/output5.wav")'''

#os.system("tts --text \"P.O.V you just sold a N F T for over $65,000 & earned your professors entire salary after finishing college\" --out_path tts/testai.wav")

'''mytext = 'POV you just sold a NFT for over $65,000 & earned your professors entire'
language = 'en'

myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("tts/welcome.mp3")
os.system("mpg321 welcome.mp3")'''

'''import pyttsx3
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[2].id)
engine.save_to_file('POV you just sold a NFT for over $65,000 & earned your professors entire salary after finishing college', 'tts/test2.mp3')
engine.runAndWait()'''

'''filepath = "image/2.jpg"
img = Image.open(filepath)
contrast_enhancer = ImageEnhance.Contrast(img)
pil_enhanced_image = contrast_enhancer.enhance(1)
enhanced_image = np.asarray(pil_enhanced_image)
r, g, b = cv2.split(enhanced_image)
enhanced_image = cv2.merge([b, g, r])

width = img.width
height = img.height
w, h, wx, hx = width, height, width, height
scaler = 1
while w < 700 and h < 700:
    wx = w
    hx = h
    w = width * scaler
    h = height * scaler
    scaler += 0.25

dim = (int(width * (scaler - 0.25)), int(height * (scaler - 0.25)))
image_data = np.asarray(img)
img_scale_up = cv2.resize(enhanced_image, (0, 0), fx=scaler, fy=scaler)
cv2.imwrite("image/output4.jpg", img_scale_up)

print(width, height, wx, hx, h, w, scaler - 0.25)
#q = "ffmpeg -i image/1.PNG -vf scale=720:1280 image/output2.png"
#os.system(f"""{q}""")'''
