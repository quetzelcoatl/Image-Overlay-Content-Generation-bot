import os
import sqlite3
import time
from shutil import copyfile
import cv2
import numpy as np
from PIL import Image, ImageEnhance
from spintax import spintax

'''q = "ffmpeg -y -i \"background_vids/0cbgoknxmybR.mp4\" -vf \"drawbox=enable='between(t,1,6)':y=ih-ih/4:color=black@1:width=iw:height=400\",\"drawtext=enable='between(t,2,6)':y=h-h/4+10:x=20:text='Test Heading':fontcolor=white:fontsize=72,drawtext=enable='between(t,2,6)':y=h-h/4+30:x=20:text='Test sub heading':fontcolor=white:fontsize=50\" -y background_vids/output.mp4"
'''
q = "ffmpeg -i background_vids/bg1/0gxwmnngkzhR.mp4 -i music/0qft0kkz0jvg0wrbDie-For-You.mp3 -filter_complex amix -map 0:v -map 0:a -map 1:a -shortest videowithbothaudios.mp4"
os.system(f"""{q}""")
'''def text_formatter(message):
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

textfile = open("spintax/0.txt/0.txt", "r", encoding="utf8")
message = ""
for ele in textfile.readline():
    message += ele

spinned = spintax.spin(message).split(" ")
print(text_formatter(spinned))
print(spinned)'''

'''img = cv2.imread("pix/dxprsjyjut.jpg")
safezone = cv2.imread("newsafezone.png")
img = cv2.addWeighted(img,1,safezone,0.5,0)
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
cv2.imshow("asdas",img)
cv2.waitKey(0)
exit(34)



image_paste = "image/Capture.jpg"
img2 = cv2.imread(image_paste)

print("Video Image : ",img.shape)
print("Image from dir : ",img2.shape)

width, height, channels = img2.shape
w, h = width, height

dimensions_w, dimensions_h = 800, 800
scaler = 1
while w < dimensions_w and h < dimensions_h:
    w = width * scaler
    h = height * scaler
    scaler += 0.01
scaler -= 0.01

checkx = False
while w > dimensions_w or h > dimensions_h:
    checkx = True
    if scaler == 0:
        break
    w = width * scaler
    h = height * scaler
    scaler -= 0.01

if checkx:
    scaler += 0.01

print(scaler, w, h)
img_scale_up = cv2.resize(img2, (0, 0), fx=scaler, fy=scaler)

print("SCALED UP IMAGE SIZE : ", img_scale_up.shape)
print("MAIN IMAGE SIZE : ", img.shape)
parent_x, parent_y,cawdawd  = img.shape
child_x, child_y,cwassdw = img_scale_up.shape
x,y = int((parent_y - child_y)/2), int((parent_x - child_x)/1.1)
replace = img.copy()
replace[y: y + child_x, x: x + child_y] = img_scale_up

img3 = cv2.resize(replace, (0, 0), fx=0.5, fy=0.5)
cv2.imshow("asdasd",img3)
cv2.waitKey()'''









#force_style='Angle=45'
#q = "ffmpeg -i background_vids/bg1/0uvjttxynebR.mp4          \"color=black:100x100[c];          [c][0]scale2ref[ct][mv];          [ct]setsar=1,drawtext=              text='test text':fontsize=36:fontcolor=white,split[text][alpha];          [text][alpha]alphamerge,rotate=a:ow=rotw(a):oh=roth(a):c=black@0[txta];          [mv][txta]overlay=x='min(0,-h*sin(a))+100':y='min(0,w*sin(a))+50':shortest=1\"       output_video.mp4"
#q = "ffmpeg -i background_vids/bg1/0uvjttxynebR.mp4 -filter_complex \"[0:v]rotate=45*pi/180[anticlockwiserotated];[anticlockwiserotated]drawtext=text='test text':x=350: y=350: fontsize=36: fontcolor=white:[textapplied];[textapplied]rotate=315*pi/180\" output_video.mp4"
#q = "ffmpeg -i background_vids/bg1/0uvjttxynebR.mp4 -vf \"[in] drawtext=fontsize=42:fontcolor=White:borderw=4:bordercolor=black:text='Hello man':x=500:y=500\" -y background_vids/jamoon.mp4"
'''q = "ffmpeg -i background_vids/bg1/cut.mp4 -filter_complex \
        \"color=black:100x100[c];\
         [c][0]scale2ref[ct][mv];\
         [ct]setsar=1,drawtext=fontfile=fonts/0.otf:\
             text='Test Text':fontsize=36:fontcolor=white,split[text][alpha];\
         [text][alpha]alphamerge,rotate=166:ow=rotw(166):oh=roth(166):c=black@0[txta];\
         [mv][txta]overlay=x='min(0,-H*sin(166))+642':y='min(0,W*sin(166))+728':shortest=1\"\
      output_videoplus166.mp4"

os.system(f"""{q}""")'''

'''source = "image/Capture.jpg"
#source = imagepath + "/" + ele

img = Image.open(source)
rgb_image = img.convert('RGB')
contrast_enhancer = ImageEnhance.Contrast(rgb_image)
pil_enhanced_image = contrast_enhancer.enhance(1)
enhanced_image = np.asarray(pil_enhanced_image)
r, g, b = cv2.split(enhanced_image)
enhanced_image = cv2.merge([b, g, r])

width = img.width
height = img.height
w, h = width, height

scaler = 1
while w < 600 and h < 600:
    w = width * scaler
    h = height * scaler
    scaler += 0.25
scaler -= 0.25

rendered_image = "jamoonRRRR.jpg"
img_scale_up = cv2.resize(enhanced_image, (0, 0), fx=scaler, fy=scaler)
cv2.imwrite(rendered_image, img_scale_up)'''




'''ttsfiles = os.listdir("tts")
for ele in ttsfiles:
    ttsfast = "ffmpeg -i tts/{} -filter:a \"atempo=1.75\" -vn ttsfast/{}".format(ele, ele)
    os.system(ttsfast)'''

#os.system("tts --model_name \"tts_models/en/ljspeech/glow-tts\" --list_speaker_idxs")
'''os.system("tts --text \"P.O.V you just sold a N F T for over $65,000 & earned your professors entire salary after finishing college\" --model_name \"tts_models/en/ljspeech/glow-tts\" \
            --out_path tts/output4.wav")'''


'''musicfiles = os.listdir("music")
mergedfiles = os.listdir("merged")
ttsfiles = os.listdir("tts")
input2 = "tts/output4.wav"
input1 = "music/0.mp3"
#q = "ffmpeg -i {} -filter:a \"volume=0.1\" music/output.wav".format(input1)
input1 = "music/output.wav"
q = "ffmpeg -i {} -i {} -filter_complex amix=inputs=2:duration=longest output/output2.mp3".format(input1, input2)
os.system(q)'''
#os.system("tts --list_models")