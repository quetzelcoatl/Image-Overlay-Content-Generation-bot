import cv2
from PIL import Image, ImageOps, ImageDraw, ImageFont
import textwrap

#im = Image.open('download.jpg')
'''
im = cv2.imread('sadboy.jpg',1)
half = cv2.resize(im, (0, 0), fx = 2, fy = 2)
height, width, colors = half.shape

#width = half.width
#height = half.height
print(width, height)

w,h = width, height
dimensions_w, dimensions_h = 800,800
scaler = 1
while w < dimensions_w and h < dimensions_h:
    w = width * scaler
    h = height * scaler
    scaler += 0.25
scaler -= 0.25

checkx = False
while w > dimensions_w or h > dimensions_h:
    checkx = True

    if scaler == 0:
        break

    if w < dimensions_w or h < dimensions_h:
        break

    w = width * scaler
    h = height * scaler
    scaler -= 0.01

if checkx:
    scaler += 0.25

print(scaler, w, h)
#rendered_image = "tempimg/" + str(ind) + "RR.jpg"
img_scale_up = cv2.resize(im, (0, 0), fx=scaler, fy=scaler)
cv2.imwrite('sadboy_resized.jpg', img_scale_up)
#cv2.imshow('awodm', img_scale_up)
#cv2.waitKey(0)
'''

im = Image.open('sadboy_resized.jpg')
fill_color = (255, 255, 255)
border_u = 100
border_l = 40
border_r = 40
border_d = 40
im_1 = ImageOps.expand(im, (border_l, border_u, border_r, border_d), fill_color)
draw = ImageDraw.Draw(im_1)

font = ImageFont.truetype("fonts/0.otf",int(im.width*0.04))
text='Sample Text this will go on as this is how it is supposed to be but no worries we will figure it out isn\'t it no worries loren ipojsdf dsf '
#text = 'sample text that has 5 words'
text = textwrap.fill(text=text, width=58)
draw.text((40, 40),text,(0,0,0),font=font)

savedImg= 'newfilesad.jpg'
im_1.save(savedImg)

'''
def textsize(self, text, font=None, *args, **kwargs):
    """Get the size of a given string, in pixels."""
    if self._multiline_check(text):
        return self.multiline_textsize(text, font, *args, **kwargs)
    if font is None:
        font = self.getfont()
    return font.getsize(text)

im = Image.open('sadboy_resized.jpg')
print(im.width)
width_img = im.width
path = "fonts/0.otf"
font = ImageFont.truetype(path,int(im.width*0.04))
sample='Sample Text this will go on as this is how it is supposed'


text='Sample Text this will go on as this is how it is supposed to be but no worries we will figure it out isn\'t it no worries loren ipojsdf dsf '

words = text.split(" ")
final = ""
slow_width = 0
slow_final = ""
for ele in words:
    final += ele + " "
    width = font.getsize(final)[0]
    #print(width, final)
    if width > width_img:
        break
    slow_width = width
    slow_final = final

print("pruned width :", slow_width)
print("text :", slow_final)
print("size of text :", len(slow_final))


#width = font.getsize(sample)[0]
#print(width)

'''