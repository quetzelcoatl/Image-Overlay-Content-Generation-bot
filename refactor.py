import os
import sqlite3
import string
import time
import random
from shutil import copyfile
import cv2
import numpy as np
from PIL import Image, ImageEnhance


def refactoring_func(dial, image_dimensions, remove_audio):
    print("IN REFACTORING FUNCTION")
    def get_random_string(length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str


    cur = sqlite3.connect("settings.db").cursor()
    cur.execute("SELECT * FROM SETTINGS")
    result = cur.fetchone()
    fetch_res = len(result)

    mainPath = result[0]
    imagepath = result[1]
    outputPath = result[2]
    bodyPath = result[3]
    musicPath = result[4]
    fontPath = result[5]
    fontPath = fontPath[:1] + "\\\\" + fontPath[1:]
    check1 = result[6]
    imagecombo = result[7]
    spintaxcombo = result[8]
    #popuppath = result[9]

    for ind, ele in enumerate(os.listdir(mainPath)):
        source = mainPath + "/" + ele
        dest = mainPath + "/" + str(ind) + get_random_string(10) + ".mp4"
        os.rename(source, dest)
        FINAL = mainPath + "/" + str(ind) + get_random_string(10) +  "R.mp4"


        q = f'ffmpeg -i {dest} -vf \"scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1\" {FINAL}'

        os.system(f"""{q}""")
        os.remove(dest)

    if imagepath != "None":
        for ind, ele in enumerate(os.listdir(imagepath)):
            ext = ele.split(".")[1]
            source = imagepath + "/" + ele

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

            dimensions_w, dimensions_h = image_dimensions, image_dimensions
            scaler = 1
            while w < dimensions_w and h < dimensions_h:
                w = width * scaler
                h = height * scaler
                scaler += 0.01
            scaler -= 0.25

            checkx = False
            while w > dimensions_w or h > dimensions_h:
                checkx = True

                if scaler == 0:
                    break

                w = width * scaler
                h = height * scaler
                scaler -= 0.01

            if checkx:
                scaler += 0.25

            print(scaler, w, h)
            rendered_image = "tempimg/" + str(ind) +get_random_string(3)+ "RR.jpg"
            img_scale_up = cv2.resize(enhanced_image, (0, 0), fx=scaler, fy=scaler)
            cv2.imwrite(rendered_image, img_scale_up)
            #os.remove(source)

    if int(check1):
        for ind, ele in enumerate(os.listdir(bodyPath)):
            source = bodyPath + "/" + ele
            dest = bodyPath + "/" + str(ind) +get_random_string(10) +  ".txt"
            os.rename(source, dest)


    if dial != -1:
        dial = dial/100
        print("dial is:", dial)

        '''#TO STRIP AUDIO
        for ele in os.listdir(mainPath):
            filename = ele.split(".")[0]
            input_ele = mainPath + "/" + ele
            output_ele = "only_audio/" + filename + ".mp3"
            q = "ffmpeg.exe -i {} {}".format(input_ele, output_ele)
            print("FOR STRIPPING AUDIO : ",q)
            os.system(f"""{q}""")'''

        #TO REDUCE AUDIO VOLUME
        for ind, ele in enumerate(os.listdir(musicPath)):
            source = musicPath + "/" + ele
            rename_dest = musicPath + "/" + str(ind) + get_random_string(3) + ele
            os.rename(source, rename_dest)
            time.sleep(1)
            print("REDUCING AUDIO FOR : ", ele)

            dest = "tempmusic/" + str(ind) + get_random_string(3) +  "RRR.mp3"
            music = "ffmpeg -i {} -filter:a \"volume={}\" {}".format(rename_dest, dial, dest)
            os.system(f"""{music}""")

        '''#TO MERGE AUDIO STREAMS
        for mainele in os.listdir("only_audio"):
            for musicele in os.listdir("tempmusic"):
                musicfile = "final_audio/" + mainele.split(".")[0] + "___" + musicele.split(".")[0] + ".mp3"
                q = "ffmpeg.exe -i {} -i {} -filter_complex amerge -c:a libmp3lame -q:a 4 {}".format("only_audio/"+mainele, "tempmusic/"+musicele, musicfile)
                print("MERGING AUDIO FOR : ", q)
                os.system(f"""{q}""")'''

    print("refactoring done")
#refactoring_func()
