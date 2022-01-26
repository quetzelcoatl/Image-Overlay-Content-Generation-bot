import subprocess
import time
import spintax
import os
import sqlite3
import pathlib, string, random
import moviepy.editor
from moviepy.editor import *
#import refactor
import shutil
import refactor

class renderr():
    def __init__(self):
        cur = sqlite3.connect("settings.db").cursor()
        cur.execute("SELECT * FROM SETTINGS")
        result = cur.fetchone()
        fetch_res = len(result)

        if fetch_res == 9:
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

        elif fetch_res == 7:
            mainPath = result[0]
            imagepath = result[1]
            outputPath = result[2]
            musicPath = result[3]
            fontPath = result[4]
            fontPath = fontPath[:1] + "\\\\" + fontPath[1:]
            check1 = result[5]
            imagecombo = result[6]

        def get_random_string(length):
            # choose from all lowercase letter
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(length))
            return result_str

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

        os.makedirs('mainTemp')
        os.makedirs('merged')
        os.makedirs('tempimg')
        os.makedirs('tempmusic')
        time.sleep(3)

        prev = 0
        mainPathFiles = os.listdir(mainPath)
        imagepathfiles = os.listdir(imagepath)
        musicPathfiles = os.listdir(musicPath)

        if int(check1):
            bodyPathFiles = len(os.listdir(bodyPath))
            prev = bodyPathFiles

        prev += len(mainPathFiles) + len(imagepathfiles) + len(musicPathfiles)

        refactor.refactoring_func()
        curr = 0
        i = 1
        while i < 10:
            maincheck = len(mainPathFiles)
            image_check_box = len(os.listdir("tempimg"))
            musiccheck = len(os.listdir("tempmusic"))

            if int(check1):
                bodyPathFiles = len(os.listdir(bodyPath))
                curr += bodyPathFiles

            curr += maincheck + image_check_box + musiccheck
            if curr == prev:
                break
            else:
                time.sleep(3)
                curr = 0

        if imagecombo == "Top":
            y_pos = 10
        elif imagecombo == "Center":
            y_pos = 5
        elif imagecombo == "Bottom":
            y_pos = 2

        if int(check1):
            #spintax
            mainPathFiles = os.listdir(mainPath)
            bodyPathFiles = os.listdir(bodyPath)
            first = (len(mainPathFiles) * len(bodyPathFiles))

            for y in mainPathFiles:

                if spintaxcombo == "Top":
                    line = 200
                elif spintaxcombo == "Center":
                    line = 700
                elif spintaxcombo == "Bottom":
                    line = 1400
                print(line)
                for x in bodyPathFiles:

                    mainPathExactFile = f"{mainPath}/{y}"
                    bodyPathExactFile = f"{bodyPath}/{x}"
                    textfile = open(bodyPathExactFile, "r", encoding="utf8")
                    message = ""
                    for ele in textfile.readline():
                        message += ele
                    spinnedMessage = spintax.spin(message).split(" ")
                    filename = get_random_string(10)

                    messagelist = text_formatter(spinnedMessage)
                    #line = 1400
                    line_offset = 0
                    q = "ffmpeg -i " + mainPathExactFile + " -vf \"[in]"
                    for ele in messagelist:
                        q += "drawtext=fontsize=60:fontcolor=White:borderw=4:bordercolor=black:fontfile= " + str(
                            fontPath) + " :text='" + ele + "':x=(w-text_w)/2:y=" + str(line) + ", "
                        line += 75
                    q = q[:-2]
                    q += "\""
                    #
                    q += f" -y mainTemp/{filename}.mp4"
                    try:
                        os.system(f"""{q}""")
                    except:
                        pass

            for i in range(10):
                firstcheck = len(os.listdir("mainTemp"))
                if first == firstcheck:
                    break
                else:
                    time.sleep(3)

            #image interlacing
            mainTempPathFiles = os.listdir("mainTemp")
            imagePathFiles = os.listdir('tempimg')
            fourth = len(mainTempPathFiles) * len(imagePathFiles)
            for y in mainTempPathFiles:
                for x in imagePathFiles:
                    mainTempExactFile = f"mainTemp/{y}"
                    imagePathExactFile = f"tempimg/{x}"
                    filename = get_random_string(10)
                    q = "ffmpeg -i {} -i {} -filter_complex \"[0:v][1:v] overlay=(W-w)/2:(H-h)/{}\" -pix_fmt yuv420p -c:a copy merged/{}".format(mainTempExactFile, imagePathExactFile, y_pos,filename)

                    try:
                        pass
                        os.system(f"""{q}""")
                    except:
                        pass

            for i in range(15):
                fourthcheck = len(os.listdir("merged"))
                if fourth == fourthcheck:
                    break
                else:
                    time.sleep(1)

            #combining music to video
            m2 = os.listdir('merged')
            musicPathFiles = os.listdir("tempmusic")

            for x in musicPathFiles:
                for y in m2:
                    x1 = f"tempmusic\{x}"
                    y1 = f" merged\{y}"
                    fname = get_random_string(10)
                    try:
                        os.system(
                            f"""ffmpeg -i {y1} -i {x1} -map 0:v -map 1:a -c:v copy -shortest {outputPath}/{fname}.mp4 """)
                    except:
                        pass

        else:
            #only image
            mainPathFiles = os.listdir(mainPath)
            imagePathFiles = os.listdir('tempimg')
            for y in mainPathFiles:
                for x in imagePathFiles:
                    mainPathExactFile = f"{mainPath}/{y}"
                    imagePathExactFile = f"tempimg/{x}"
                    filename = get_random_string(10)
                    q = "ffmpeg -i {} -i {} -filter_complex \"[0:v][1:v] overlay=(W-w)/2:(H-h)/{}\" -pix_fmt yuv420p -c:a copy merged/{}.mp4 ".format(
                        mainPathExactFile, imagePathExactFile, y_pos,filename)

                    try:
                        pass
                        os.system(f"""{q}""")
                    except:
                        pass

            m2 = os.listdir('merged')
            musicPathFiles = os.listdir("tempmusic")

            for x in musicPathFiles:
                for y in m2:
                    x1 = f"tempmusic\{x}"
                    y1 = f" merged\{y}"
                    fname = get_random_string(10)
                    try:
                        os.system(
                            f"""ffmpeg -i {y1} -i {x1} -map 0:v -map 1:a -c:v copy -shortest {outputPath}/{fname}.mp4 """)
                    except:
                        pass

        time.sleep(10)
        shutil.rmtree("merged")
        shutil.rmtree("mainTemp")
        shutil.rmtree("tempmusic")
        shutil.rmtree("tempimg")
        exit(0)

