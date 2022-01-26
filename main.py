import copy
import os
import sqlite3
import traceback
from threading import Thread

import astroid.modutils
import cv2
import pywin32_bootstrap
from PyQt5 import QtWidgets
import sys
from qtpy import uic
import os
import sqlite3
import string
import time
import random
import shutil
import spintax
import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import cv2
import refactor

cur = sqlite3.connect("settings.db").cursor()


class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ImagecontentGen.ui', self)

        db_evincer = False
        for ele in os.getcwd():
            if ele == "settings.db":
                db_evincer = True
                break
        if db_evincer is not True:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS SETTINGS (MAINVID VARCHAR(1000),IMAGE VARCHAR(1000),OUTPUTDIR VARCHAR(1000),BODYTEXT VARCHAR(1000),MUSICDIR VARCHAR(1000),FONTDIR VARCHAR(1000), BOX1 VARCHAR )")

        self.loadData()
        self.mainPartBtn.clicked.connect(self.selectMain)
        self.imageBtn.clicked.connect(self.selectImage)
        self.bodyTextBtn.clicked.connect(self.selectBodyText)
        #self.bodyTextBtn_2.clicked.connect(self.selectPopUpText)
        self.fontsBtn.clicked.connect(self.selectFont)
        self.musicBtn.clicked.connect(self.selectMusic)
        self.outputBtn.clicked.connect(self.selectOutput)
        self.renderButton.clicked.connect(self.renderVid)
        self.saveSettingsBtn.clicked.connect(self.saveSettings)
        self.pushButton.clicked.connect(self.image_button)
        self.pushButton_9.clicked.connect(self.pop_up_button_1)
        self.pushButton_8.clicked.connect(self.pop_up_button_2)
        self.pushButton_7.clicked.connect(self.pop_up_button_3)
        self.pushButton_6.clicked.connect(self.pop_up_button_4)
        self.pushButton_5.clicked.connect(self.pop_up_button_5)
        self.pushButton_3.clicked.connect(self.pop_up_button_6)
        self.show()
        global img3, img, x_axis_array, y_axis_array, preview, temp_img3, pop_up_Texts
        pop_up_Texts = {}
        x_axis_array = {}
        y_axis_array = {}
        preview = -1

    def image_button(self):
        if self.mainPlaceholder.text() != "None" and self.outroPlaceholder.text() != "None":
            global img, preview
            if preview == -1: #POPUP TEXT NOT YET SELECTED
                tempmainpath = self.mainPlaceholder.text()
                tempmainPathFiles = os.listdir(tempmainpath)
                path = tempmainpath + "/" + tempmainPathFiles[0]
                video = cv2.VideoCapture(path)
                length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
                rangee = length // 2
                for i in range(rangee):
                    ret, frame = video.read()
                img = frame
                preview = 1

            global img3
            tempimagepath = self.outroPlaceholder.text()
            tempimagepathfiles = os.listdir(tempimagepath)
            image_paste = tempimagepath + "/" + tempimagepathfiles[0]
            img2 = cv2.imread(image_paste)
            print("Video Image : ", img.shape)
            print("Image from dir : ", img2.shape)
            width, height, channels = img2.shape
            w, h = width, height
            image_size = self.spinBox_2.value()
            dimensions_w, dimensions_h = image_size, image_size
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
            imagecombo = self.comboBox_2.currentText()
            if imagecombo == "Top":
                y_pos = 5
            elif imagecombo == "Center":
                y_pos = 2
            elif imagecombo == "Bottom":
                y_pos = 1.1
            print("SCALED UP IMAGE SIZE : ", img_scale_up.shape)
            print("MAIN IMAGE SIZE : ", img.shape)
            parent_x, parent_y, cawdawd = img.shape
            child_x, child_y, cwassdw = img_scale_up.shape
            x, y = int((parent_y - child_y) / 2), int((parent_x - child_x) / y_pos)
            replace = img.copy()
            replace[y: y + child_x, x: x + child_y] = img_scale_up
            img3 = cv2.resize(replace, (0, 0), fx=0.5, fy=0.5)
            cv2.imshow('image', img3)

    def pop_up_button_1(self):
        pop_up_1 = self.checkBox_3.isChecked()
        global img, img3, preview, temp_img3, pop_up_Texts
        if int(pop_up_1) and self.mainPlaceholder.text() != "None":
            if preview == -1: #IMAGE NOT YET SELECTED
                tempmainpath = self.mainPlaceholder.text()
                tempmainPathFiles = os.listdir(tempmainpath)
                path = tempmainpath + "/" + tempmainPathFiles[0]
                video = cv2.VideoCapture(path)
                length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
                rangee = length // 2
                for i in range(rangee):
                    ret, frame = video.read()
                img = frame
                img3 = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
                temp_img3 = copy.deepcopy(img3)
                preview = 1
            else:
                temp_img3 = copy.deepcopy(img3)

            pop_up_1_text = self.textEdit_2.toPlainText()
            pop_up_Texts[1] = pop_up_1_text

            #pop_up_Texts.append(pop_up_1_text)
            def click_event(event, x, y, flags, params):
                if event == cv2.EVENT_LBUTTONDOWN:
                    global xaxis, yaxis
                    xaxis = x * 2
                    yaxis = y * 2
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    print("**********************************************")
                    print("Coords for pop up text 1 : ", xaxis, yaxis)
                    print("**********************************************")
                    cv2.putText(img3, pop_up_1_text, (x, y), font, 1, (0,128,0), 1)
                    cv2.putText(img3, "pop up 1", (x, y + 30), font, 1, (0, 0, 255), 1)
                    cv2.imshow('image', img3)

            cv2.imshow('image', img3)
            cv2.setMouseCallback('image', click_event)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            global xaxis, yaxis
            global x_axis_array, y_axis_array
            x_axis_array[1] = xaxis
            y_axis_array[1] = yaxis
            print("THE COORD ARRAYS ARE : ")
            print(x_axis_array, y_axis_array)
            self.spinBox_5.setValue((xaxis))
            self.spinBox_6.setValue((yaxis))

            font = cv2.FONT_HERSHEY_SIMPLEX
            img3 = copy.deepcopy(temp_img3)
            for ele in x_axis_array.keys():
                x = x_axis_array[ele]//2
                y = y_axis_array[ele]//2
                text = pop_up_Texts[ele]
                pos = "pop up " + str(ele)
                cv2.putText(img3, text, (x, y), font, 1, (0,128,0), 2)
                cv2.putText(img3, pos, (x, y + 30), font, 1, (0, 0, 255), 2)



    def pop_up_button_2(self):
        pop_up_2 = self.checkBox_6.isChecked()
        global img, img3, preview, temp_img3, pop_up_Texts
        if int(pop_up_2) and self.mainPlaceholder.text() != "None":
            pop_up_2_text = self.textEdit_3.toPlainText()
            pop_up_Texts[2] = pop_up_2_text
            def click_event(event, x, y, flags, params):
                if event == cv2.EVENT_LBUTTONDOWN:
                    global xaxis, yaxis
                    xaxis = x * 2
                    yaxis = y * 2
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    print("**********************************************")
                    print("Coords for pop up text 2 : ", xaxis, yaxis)
                    print("**********************************************")
                    cv2.putText(img3, pop_up_2_text, (x, y), font, 1, (0,128,0), 1)
                    cv2.putText(img3, "pop up 2", (x, y + 30), font, 1, (0, 0, 255), 1)
                    cv2.imshow('image', img3)

            cv2.imshow('image', img3)
            cv2.setMouseCallback('image', click_event)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            global xaxis, yaxis
            global x_axis_array, y_axis_array
            x_axis_array[2] = xaxis
            y_axis_array[2] = yaxis
            print("THE COORD ARRAYS ARE : ")
            print(x_axis_array, y_axis_array)
            self.spinBox_21.setValue((xaxis))
            self.spinBox_22.setValue((yaxis))

            font = cv2.FONT_HERSHEY_SIMPLEX
            img3 = copy.deepcopy(temp_img3)
            for ele in x_axis_array.keys():
                x = x_axis_array[ele]//2
                y = y_axis_array[ele]//2
                text = pop_up_Texts[ele]
                pos = "pop up " + str(ele)
                cv2.putText(img3, text, (x, y), font, 1, (0,128,0), 2)
                cv2.putText(img3, pos, (x, y + 30), font, 1, (0, 0, 255), 2)

    def pop_up_button_3(self):
        pop_up_3 = self.checkBox_7.isChecked()
        global img, img3, preview, temp_img3, pop_up_Texts
        if int(pop_up_3) and self.mainPlaceholder.text() != "None":
            pop_up_3_text = self.textEdit.toPlainText()
            pop_up_Texts[3] = pop_up_3_text
            def click_event(event, x, y, flags, params):
                if event == cv2.EVENT_LBUTTONDOWN:
                    global xaxis, yaxis
                    xaxis = x * 2
                    yaxis = y * 2
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    print("**********************************************")
                    print("Coords for pop up text 3 : ", xaxis, yaxis)
                    print("**********************************************")
                    cv2.putText(img3, pop_up_3_text, (x, y), font, 1, (0,128,0), 1)
                    cv2.putText(img3, "pop up 3", (x, y + 30), font, 1, (255, 0, 0), 1)
                    cv2.imshow('image', img3)

            cv2.imshow('image', img3)
            cv2.setMouseCallback('image', click_event)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            global xaxis, yaxis
            global x_axis_array, y_axis_array
            x_axis_array[3] = xaxis
            y_axis_array[3] = yaxis
            print("THE COORD ARRAYS ARE : ")
            print(x_axis_array, y_axis_array)
            self.spinBox_27.setValue((xaxis))
            self.spinBox_28.setValue((yaxis))

            font = cv2.FONT_HERSHEY_SIMPLEX
            img3 = copy.deepcopy(temp_img3)
            for ele in x_axis_array.keys():
                x = x_axis_array[ele]//2
                y = y_axis_array[ele]//2
                text = pop_up_Texts[ele]
                pos = "pop up " + str(ele)
                cv2.putText(img3, text, (x, y), font, 1, (0,128,0), 2)
                cv2.putText(img3, pos, (x, y + 30), font, 1, (0, 0, 255), 2)

    def pop_up_button_4(self):
        pop_up_4 = self.checkBox_8.isChecked()
        global img, img3, preview, temp_img3, pop_up_Texts
        if int(pop_up_4) and self.mainPlaceholder.text() != "None":
            pop_up_4_text = self.textEdit_4.toPlainText()
            pop_up_Texts[4] = pop_up_4_text
            def click_event(event, x, y, flags, params):
                if event == cv2.EVENT_LBUTTONDOWN:
                    global xaxis, yaxis
                    xaxis = x * 2
                    yaxis = y * 2
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    print("**********************************************")
                    print("Coords for pop up text 4 : ", xaxis, yaxis)
                    print("**********************************************")
                    cv2.putText(img3, pop_up_4_text, (x, y), font, 1, (0,128,0), 1)
                    cv2.putText(img3, "pop up 4", (x, y + 30), font, 1, (255, 0, 0), 1)
                    cv2.imshow('image', img3)

            cv2.imshow('image', img3)
            cv2.setMouseCallback('image', click_event)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            global xaxis, yaxis
            global x_axis_array, y_axis_array
            x_axis_array[4] = xaxis
            y_axis_array[4] = yaxis
            print("THE COORD ARRAYS ARE : ")
            print(x_axis_array, y_axis_array)
            self.spinBox_33.setValue((xaxis))
            self.spinBox_34.setValue((yaxis))

            font = cv2.FONT_HERSHEY_SIMPLEX
            img3 = copy.deepcopy(temp_img3)
            for ele in x_axis_array.keys():
                x = x_axis_array[ele]//2
                y = y_axis_array[ele]//2
                text = pop_up_Texts[ele]
                pos = "pop up " + str(ele)
                cv2.putText(img3, text, (x, y), font, 1, (0,128,0), 2)
                cv2.putText(img3, pos, (x, y + 30), font, 1, (0, 0, 255), 2)

    def pop_up_button_5(self):
        pop_up_5 = self.checkBox_9.isChecked()
        global img, img3, preview, temp_img3, pop_up_Texts
        if int(pop_up_5) and self.mainPlaceholder.text() != "None":
            pop_up_5_text = self.textEdit_5.toPlainText()
            pop_up_Texts[5] = pop_up_5_text
            def click_event(event, x, y, flags, params):
                if event == cv2.EVENT_LBUTTONDOWN:
                    global xaxis, yaxis
                    xaxis = x * 2
                    yaxis = y * 2
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    print("**********************************************")
                    print("Coords for pop up text 5 : ", xaxis, yaxis)
                    print("**********************************************")
                    cv2.putText(img3, pop_up_5_text, (x, y), font, 1, (0,128,0), 1)
                    cv2.putText(img3, "pop up 5", (x, y + 30), font, 1, (255, 0, 0), 1)
                    cv2.imshow('image', img3)

            cv2.imshow('image', img3)
            cv2.setMouseCallback('image', click_event)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            global xaxis, yaxis
            global x_axis_array, y_axis_array
            x_axis_array[5] = xaxis
            y_axis_array[5] = yaxis
            print("THE COORD ARRAYS ARE : ")
            print(x_axis_array, y_axis_array)
            self.spinBox_39.setValue((xaxis))
            self.spinBox_40.setValue((yaxis))

            font = cv2.FONT_HERSHEY_SIMPLEX
            img3 = copy.deepcopy(temp_img3)
            for ele in x_axis_array.keys():
                x = x_axis_array[ele]//2
                y = y_axis_array[ele]//2
                text = pop_up_Texts[ele]
                pos = "pop up " + str(ele)
                cv2.putText(img3, text, (x, y), font, 1, (0,128,0), 2)
                cv2.putText(img3, pos, (x, y + 30), font, 1, (0, 0, 255), 2)

    def pop_up_button_6(self):
        pop_up_6 = self.checkBox_10.isChecked()
        global img, img3, preview, temp_img3, pop_up_Texts
        if int(pop_up_6) and self.mainPlaceholder.text() != "None":
            pop_up_6_text = self.textEdit_6.toPlainText()
            pop_up_Texts[6] = pop_up_6_text
            def click_event(event, x, y, flags, params):
                if event == cv2.EVENT_LBUTTONDOWN:
                    global xaxis, yaxis
                    xaxis = x * 2
                    yaxis = y * 2
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    print("**********************************************")
                    print("Coords for pop up text 6 : ", xaxis, yaxis)
                    print("**********************************************")
                    cv2.putText(img3, pop_up_6_text, (x, y), font, 1, (0,128,0), 1)
                    cv2.putText(img3, "pop up 6", (x, y + 30), font, 1, (255, 0, 0), 1)
                    cv2.imshow('image', img3)

            cv2.imshow('image', img3)
            cv2.setMouseCallback('image', click_event)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            global xaxis, yaxis
            global x_axis_array, y_axis_array
            x_axis_array[6] = xaxis
            y_axis_array[6] = yaxis
            print("THE COORD ARRAYS ARE : ")
            print(x_axis_array, y_axis_array)
            self.spinBox_45.setValue((xaxis))
            self.spinBox_46.setValue((yaxis))

            font = cv2.FONT_HERSHEY_SIMPLEX
            img3 = copy.deepcopy(temp_img3)
            for ele in x_axis_array.keys():
                x = x_axis_array[ele]//2
                y = y_axis_array[ele]//2
                text = pop_up_Texts[ele]
                pos = "pop up " + str(ele)
                cv2.putText(img3, text, (x, y), font, 1, (0,128,0), 2)
                cv2.putText(img3, pos, (x, y + 30), font, 1, (0, 0, 255), 2)

    def loadData(self):
        cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='SETTINGS' ''')

        # if the count is 1, then table exists
        if cur.fetchone()[0] == 1:
            cur.execute("SELECT * FROM SETTINGS")
            result = cur.fetchone()
            fetch_res = len(result)

            print(result)
            print("result value : ", fetch_res)

            self.mainPlaceholder.setText(result[0])
            self.outroPlaceholder.setText(result[1])
            self.outputPlaceholder.setText(result[2])
            self.bodyPlaceholder.setText(result[3])
            self.musicPlaceholder.setText(result[4])
            self.fontsPlaceholder.setText(result[5])
            self.comboBox_2.setCurrentText(result[7])
            self.comboBox.setCurrentText(result[8])
            #self.bodyPlaceholder_2.setText(result[9])

    def renderVid(self):
        t1 = Thread(target=self.operation)
        t1.start()

    def saveSettings(self):
        print("INSIDE SAVE")
        checkbox1 = self.checkBox.isChecked()
        image_combobox = self.comboBox_2.currentText()
        spintax_combobox = self.comboBox.currentText()

        #pop_up_checkbox = self.checkBox_3.isChecked()
        music_checkbox = self.checkBox_2.isChecked()
        spintax_checkbox = self.checkBox.isChecked()
        image_checkbox = self.checkBox_4.isChecked()

        '''if not int(pop_up_checkbox):
            self.bodyPlaceholder_2.setText("None")
            self.len_3.setText("0")'''

        if not int(spintax_checkbox):
            self.bodyPlaceholder.setText("None")
            self.len_3.setText("0")

        if not int(music_checkbox):
            self.musicPlaceholder.setText("None")
            self.len_5.setText("0")

        if not int(image_checkbox):
            self.outroPlaceholder.setText("None")
            self.len_2.setText("0")

        print("inside main")
        cur.execute('DROP TABLE SETTINGS')
        cur.execute(
            "CREATE TABLE IF NOT EXISTS SETTINGS (MAINVID VARCHAR(1000),IMAGE VARCHAR(1000),OUTPUTDIR VARCHAR(1000),BODYTEXT VARCHAR(1000),MUSICDIR VARCHAR(1000),FONTDIR VARCHAR(1000), BOX1 VARCHAR,BOX2 VARCHAR,BOX3 VARCHAR)")
        q = "INSERT INTO SETTINGS VALUES(?,?,?,?,?,?,?,?,?)"
        cur.execute(q, (self.mainPlaceholder.text(), self.outroPlaceholder.text(), self.outputPlaceholder.text(),
                        self.bodyPlaceholder.text(), self.musicPlaceholder.text(), self.fontsPlaceholder.text(),
                        checkbox1, image_combobox, spintax_combobox))
        cur.execute('commit')

        background = len(os.listdir(self.mainPlaceholder.text()))

        if int(image_checkbox):
            image = len(os.listdir(self.outroPlaceholder.text()))
            self.len_2.setText(str(image))

        if int(checkbox1):
            body_text = len(os.listdir(self.bodyPlaceholder.text()))
            self.len_3.setText(str(body_text))

        if int(music_checkbox):
            music = len(os.listdir(self.musicPlaceholder.text()))
            self.len_5.setText(str(music))

        '''if int(pop_up_checkbox):
            print("inside popup spintax")
            popup = len(os.listdir(self.bodyPlaceholder_2.text()))
            self.len_6.setText(str(popup))'''

        self.len.setText(str(background))
        self.renderStatusPlaceholder.setText("Settings Saved")

        cur7 = sqlite3.connect("settings.db").cursor()
        cur7.execute("SELECT * FROM SETTINGS")
        result = cur7.fetchone()
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

        #puts total time of the video
        mainPathFiles = os.listdir(mainPath)
        path_sec = mainPath + "/" + mainPathFiles[0]
        data = cv2.VideoCapture(path_sec)
        frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = int(data.get(cv2.CAP_PROP_FPS))
        ending = int(frames / fps)
        self.len_7.setText(str(ending))

        if int(image_checkbox):
            imagepathfiles = os.listdir(imagepath)

        if int(spintax_checkbox):
            bodyPathFiles = os.listdir(bodyPath)

        if int(music_checkbox):
            musicPathfiles = os.listdir(musicPath)
            dial = self.dial.value()
            self.len_4.setText(str(dial))

        '''if int(pop_up_checkbox):
            popuppathfiles = os.listdir(popuppath)'''

        placeholder_iters = len(mainPathFiles)

        if int(image_checkbox):
            placeholder_iters *= len(imagepathfiles)

        if int(spintax_checkbox):
            placeholder_iters *= len(bodyPathFiles)

        if int(music_checkbox):
            placeholder_iters *= len(musicPathfiles)

        '''if int(pop_up_checkbox):
            placeholder_iters *= len(popuppathfiles)'''

        print("total iters :", placeholder_iters)
        self.totalVidsPlaceholder.setText(str(placeholder_iters))

        #EDITOR FOR REVIEW

        '''pop_up_1 = self.checkBox_3.isChecked()
        pop_up_2 = self.checkBox_6.isChecked()
        pop_up_3 = self.checkBox_7.isChecked()
        pop_up_4 = self.checkBox_8.isChecked()
        pop_up_5 = self.checkBox_9.isChecked()
        pop_up_6 = self.checkBox_10.isChecked()

        total_pop_ups = 0
        if int(pop_up_1):
            total_pop_ups += 1
        if int(pop_up_2):
            total_pop_ups += 1
        if int(pop_up_3):
            total_pop_ups += 1
        if int(pop_up_4):
            total_pop_ups += 1
        if int(pop_up_5):
            total_pop_ups += 1
        if int(pop_up_6):
            total_pop_ups += 1

        global img, img3
        if int(total_pop_ups):
            if img == -1:
                path = mainPath + "/" + mainPathFiles[0]
                video = cv2.VideoCapture(path)
                length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
                rangee = length // 2
                for i in range(rangee):
                    ret, frame = video.read()
                img = frame
                img3 = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

            def click_event(event, x, y, flags, params):
                if event == cv2.EVENT_LBUTTONDOWN:
                    global xaxis, yaxis
                    xaxis = x * 2
                    yaxis = y * 2
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    print("**********************************************")
                    print("Coords : ", xaxis, yaxis)
                    print("**********************************************")
                    cv2.putText(img3, ele, (x, y), font, 0.5, (255, 255, 255), 1)
                    cv2.imshow('image', img3)

            cv2.imshow('image', img3)
            cv2.setMouseCallback('image', click_event)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            global xaxis, yaxis
            #print("Coords : ", xaxis, yaxis)
            #self.spinBox_5.setValue(xaxis)
            #self.spinBox_6.setValue(yaxis)'''


    def selectMain(self):
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderpath == None: folderpath = 'NONE'
        self.mainPlaceholder.setText(folderpath)

    def selectImage(self):
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderpath == None: folderpath = 'NONE'
        self.outroPlaceholder.setText(folderpath)

    def selectBodyText(self):
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderpath == None: folderpath = 'NONE'
        self.bodyPlaceholder.setText(folderpath)

    def selectPopUpText(self):
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderpath == None: folderpath = 'NONE'
        self.bodyPlaceholder_2.setText(folderpath)

    def selectMusic(self):
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderpath == None: folderpath = 'NONE'
        self.musicPlaceholder.setText(folderpath)

    def selectFont(self):
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')
        if filename == None: filename = 'NONE'
        self.fontsPlaceholder.setText(filename)

    def selectOutput(self):
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folderpath == None: folderpath = 'NONE'
        self.outputPlaceholder.setText(folderpath)

    def operation(self):
        cur = sqlite3.connect("settings.db").cursor()
        cur.execute("SELECT * FROM SETTINGS")
        result = cur.fetchone()
        fetch_res = len(result)
        self.renderStatusPlaceholder.setText("Rendering in Progress")

        print(result)

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

        print("MainPath : ", mainPath)
        print("imagepath : ", imagepath)
        print("outputpath : ", outputPath)
        print("bodyPath : ", bodyPath)
        print("musicPath : ", musicPath)
        #print("popuppath : ", popuppath)

        checkbox1 = self.checkBox.isChecked()
        image_combobox = self.comboBox_2.currentText()
        spintax_combobox = self.comboBox.currentText()
        pop_up_checkbox = self.checkBox_3.isChecked()
        music_checkbox = self.checkBox_2.isChecked()
        spintax_checkbox = self.checkBox.isChecked()

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

        curr_dirs = os.listdir()

        if 'mainTemp' in curr_dirs:
            shutil.rmtree("mainTemp")
        if 'merged' in curr_dirs:
            shutil.rmtree("merged")
        if 'tempimg' in curr_dirs:
            shutil.rmtree("tempimg")
        if 'tempmusic' in curr_dirs:
            shutil.rmtree("tempmusic")
        if 'tempoutput' in curr_dirs:
            shutil.rmtree("tempoutput")
        '''if "only_audio" in curr_dirs:
            shutil.rmtree("only_audio")
        if "final_audio" in curr_dirs:
            shutil.rmtree("final_audio")'''

        time.sleep(5)
        os.makedirs('mainTemp')
        os.makedirs('merged')
        os.makedirs('tempimg')
        os.makedirs('tempmusic')
        os.makedirs('tempoutput')
        '''os.makedirs("only_audio")
        os.makedirs("final_audio")'''
        time.sleep(3)

        if int(spintax_checkbox):
            bodyPathFiles = os.listdir(bodyPath)

        if int(music_checkbox):
            musicPathfiles = os.listdir(musicPath)
            dial = self.dial.value()
            self.len_4.setText(str(dial))

        prev = 0
        mainPathFiles = os.listdir(mainPath)
        checkbox2 = self.checkBox_2.isChecked()
        image_check_box = self.checkBox_4.isChecked()

        if int(image_check_box):
            imagepathfiles = os.listdir(imagepath)
            prev += len(imagepathfiles)
            imagepathfiles_iters = len(imagepathfiles)
        else:
            imagepathfiles_iters = 1

        '''if int(pop_up_checkbox):
            popupfiles = os.listdir(popuppath)
            prev += len(popupfiles)
            popupPathfiles_iters = len(popupfiles)
        else:
            popupPathfiles_iters = 1'''

        if int(checkbox2):
            musicPathfiles = os.listdir(musicPath)
            prev += len(musicPathfiles)
            musicPathfiles_iters = len(musicPathfiles)
        else:
            musicPathfiles_iters = 1

        if int(check1):
            bodyPathFiles = len(os.listdir(bodyPath))
            prev += bodyPathFiles
            bodyPathFiles_iters = bodyPathFiles
        else:
            bodyPathFiles_iters = 1

        prev += len(mainPathFiles)

        if int(self.checkBox_5.isChecked()):
            remove_audio = True
        else:
            remove_audio = False

        self.renderStatusPlaceholder.setText("Refactoring in Progress")
        image_dim = -1
        dial = -1
        if int(checkbox2):
            dial = self.dial.value()
            self.len_4.setText(str(dial))

        if int(image_check_box):
            image_dim = self.spinBox_2.value()

        refactor.refactoring_func(dial, image_dim, remove_audio)
        self.renderStatusPlaceholder.setText("Refactoring Completed")

        curr = 0
        i = 1
        while i < 10:
            maincheck = len(mainPathFiles)

            if int(image_check_box):
                imagecheck = len(os.listdir("tempimg"))
                curr += imagecheck

            '''if int(pop_up_checkbox):
                popupcheck = len(os.listdir(popuppath))
                curr += popupcheck'''

            if int(checkbox2):
                musiccheck = len(os.listdir("tempmusic"))
                curr += musiccheck

            if int(check1):
                bodyPathFiles = len(os.listdir(bodyPath))
                curr += bodyPathFiles

            curr += maincheck
            if curr == prev:
                break
            else:
                time.sleep(3)
                curr = 0

        if int(image_check_box):
            if imagecombo == "Top":
                y_pos = 5
            elif imagecombo == "Center":
                y_pos = 2
            elif imagecombo == "Bottom":
                y_pos = 1.1

        # Computing Total iterations
        total_iters = 0
        if int(image_check_box): #image
            total_iters += len(mainPathFiles) * bodyPathFiles_iters * imagepathfiles_iters

        if int(spintax_checkbox): #maintext
            total_iters += len(mainPathFiles) * bodyPathFiles_iters

        if int(checkbox2): #music
            total_iters += len(mainPathFiles) * bodyPathFiles_iters * imagepathfiles_iters * musicPathfiles_iters

        if int(pop_up_checkbox): #popup
            total_iters += len(mainPathFiles) * bodyPathFiles_iters * imagepathfiles_iters * musicPathfiles_iters

        print("TOTAL ITERATIONS ARE :",total_iters)

        curr_iters = 0

        total_videos_rendered = 0
        stop_here = self.spinBox_85.value()

        #For Spintax Only
        if int(check1):
            time_sync = self.comboBox_6.currentText()

            self.renderStatusPlaceholder.setText("Rendering Background Video")
            mainPathFiles = os.listdir(mainPath)
            bodyPathFiles = os.listdir(bodyPath)
            first = (len(mainPathFiles) * len(bodyPathFiles))
            mainspintaxsize = self.spinBox_7.value()
            text_color_spintax = str.lower(self.comboBox_49.currentText())
            stroke_color_spintax = str.lower(self.comboBox_48.currentText())
            back_ground_spintax_color = str.lower(self.comboBox_50.currentText())

            disable_box_color_spintax = False
            disable_stroke_color = False
            if stroke_color_spintax == "disable":
                disable_stroke_color = True

            if back_ground_spintax_color == "disable":
                disable_box_color_spintax = True

            path_sec = mainPath + "/" + mainPathFiles[0]
            data = cv2.VideoCapture(path_sec)
            frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = int(data.get(cv2.CAP_PROP_FPS))
            ending = int(frames / fps)

            start_end_checker = False
            if time_sync == "Full Duration":
                start_end_checker = True
            elif time_sync == "Start - End":
                start = self.spinBox_13.value()
                end = self.spinBox_12.value()
            elif time_sync == "x from end":
                start = ending - self.spinBox_14.value()
                end = ending


            for y in mainPathFiles:
                if total_videos_rendered == stop_here:
                    break
                for x in bodyPathFiles:

                    if spintaxcombo == "Top":
                        line = 200
                    elif spintaxcombo == "Center":
                        line = 800
                    elif spintaxcombo == "Bottom":
                        line = 1400

                    mainPathExactFile = f"{mainPath}/{y}"
                    bodyPathExactFile = f"{bodyPath}/{x}"
                    textfile = open(bodyPathExactFile, "r", encoding="utf8")
                    message = ""
                    for ele in textfile.readline():
                        message += ele
                    spinnedMessage = spintax.spin(message).split(" ")

                    first_file = y.split(".")[0]
                    second_file = x.split(".")[0]
                    filename = first_file + "_" + second_file

                    if not start_end_checker:
                        time_stamp = "'between(t," + str(start) + "," + str(end) + ")'"

                    messagelist = text_formatter(spinnedMessage)

                    q = "ffmpeg -i " + mainPathExactFile + " -vf \"[in]"
                    for ele in messagelist:

                        q += "drawtext=fontsize=" + str(mainspintaxsize) + ":fontcolor=" + text_color_spintax

                        if not disable_box_color_spintax: #enable background box
                            q += ":box=1:boxcolor=" + back_ground_spintax_color + "@1.0:boxborderw=5"

                        if not disable_stroke_color: #enable stroke of text
                            q += ":borderw=4:bordercolor=" + stroke_color_spintax

                        q += ":fontfile= " + str(fontPath) + " :text='" + ele + "':x=(w-text_w)/2:y=" + str(line)

                        if not start_end_checker: #enable time stamp
                            q += ":enable=" + time_stamp + ", "
                        else:
                            q += ", "

                        line += 75
                    q = q[:-2]
                    q += "\""
                    # 
                    q += f" -y mainTemp/{filename}.mp4"
                    try:
                        os.system(f"""{q}""")
                    except:
                        pass
                    curr_iters += 1

                    progress_bar_status = int((curr_iters / total_iters) * 100)
                    self.progressBar.setValue(progress_bar_status)
                    print("% Completed  : {}/100".format(progress_bar_status))

                    if not int(music_checkbox) and not int(image_check_box) and not int(pop_up_checkbox):
                        total_videos_rendered += 1
                        self.renderStatusPlaceholder_3.setText(str(total_videos_rendered))
                        if total_videos_rendered == stop_here:
                            break
        else:
            #moving items from bg vids to mainTemp
            print("COPYING VIDEOS FROM INPUT TO MAINTEMP NO MAIN SPINTAX DETECTED")
            for ele in os.listdir(mainPath):
                if remove_audio:
                    source = mainPath + "/" + ele
                    dest = "mainTemp/" + ele
                    q = f'ffmpeg -i {source} -vf \"scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1\" -an {dest}'
                    print("STRIPPING AUDIO FROM THE VIDEO FILE")
                    try:
                        os.system(f"""{q}""")
                    except:
                        pass
                else:
                    src = mainPath + "/" + ele
                    shutil.copy(src, "mainTemp")

        if int(check1):
            for i in range(10):
                firstcheck = len(os.listdir("mainTemp"))
                if first == firstcheck:
                    break
                else:
                    time.sleep(3)

        #For Image Only
        if int(image_check_box):
            time_sync = self.comboBox_7.currentText()
            self.renderStatusPlaceholder.setText("Interlacing Image")
            # image interlacing
            mainTempPathFiles = os.listdir("mainTemp")
            imagePathFiles = os.listdir('tempimg')
            fourth = len(mainTempPathFiles) * len(imagePathFiles)

            path_sec = "mainTemp/" + mainTempPathFiles[0]
            data = cv2.VideoCapture(path_sec)
            frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = int(data.get(cv2.CAP_PROP_FPS))
            ending = int(frames / fps)

            start_end_checker_image = False
            if time_sync == "Full Duration":
                start_end_checker_image = True
            elif time_sync == "Start - End":
                start = self.spinBox_10.value()
                end = self.spinBox_9.value()
            elif time_sync == "x from end":
                start = ending - self.spinBox_11.value()
                end = ending

            #comeback
            for y in mainTempPathFiles:
                if total_videos_rendered == stop_here:
                    break
                for x in imagePathFiles:
                    mainTempExactFile = f"mainTemp/{y}"
                    imagePathExactFile = f"tempimg/{x}"

                    first_file = y.split(".")[0]
                    second_file = x.split(".")[0]
                    filename = first_file + "_" + second_file + ".mp4"
                    filename_f = "merged/" + filename

                    if not start_end_checker_image:
                        time_stamp_image = "'between(t," + str(start) + "," + str(end) + ")'"

                        q = "ffmpeg -i {} -i {} -filter_complex \"[0:v][1:v] overlay=(W-w)/2:(H-h)/{}:enable={}\" -pix_fmt yuv420p -c:a copy {}".format(
                            mainTempExactFile, imagePathExactFile, y_pos, time_stamp_image, filename_f)
                    else:
                        q = "ffmpeg -i {} -i {} -filter_complex \"[0:v][1:v] overlay=(W-w)/2:(H-h)/{}\" -pix_fmt yuv420p -c:a copy {}".format(
                            mainTempExactFile, imagePathExactFile, y_pos, filename_f)

                    try:
                        pass
                        os.system(f"""{q}""")
                    except:
                        pass

                    curr_iters += 1
                    progress_bar_status = int((curr_iters / total_iters) * 100)
                    self.progressBar.setValue(progress_bar_status)
                    print("% Completed  : {}/100".format(progress_bar_status))

                    if not int(music_checkbox)  and not int(pop_up_checkbox):
                        total_videos_rendered += 1
                        self.renderStatusPlaceholder_3.setText(str(total_videos_rendered))
                        if total_videos_rendered == stop_here:
                            break
        else:
            #MOVING FILES FROM MAINTEMP TO MERGED
            print("MOVING FILES FROM MAINTEMP TO MERGED no image applied")
            for ele in os.listdir("mainTemp"):
                src = "mainTemp/" + ele
                shutil.copy(src, "merged")

        if int(image_check_box):
            for i in range(15):
                if int(checkbox2):
                    fourthcheck = len(os.listdir("merged"))
                else:
                    fourthcheck = len(os.listdir(outputPath))
                if fourth == fourthcheck:
                    break
                else:
                    time.sleep(1)

        #POP UP METADATA STARTS HERE
        pop_up_1 = self.checkBox_3.isChecked()
        pop_up_2 = self.checkBox_6.isChecked()
        pop_up_3 = self.checkBox_7.isChecked()
        pop_up_4 = self.checkBox_8.isChecked()
        pop_up_5 = self.checkBox_9.isChecked()
        pop_up_6 = self.checkBox_10.isChecked()
        text_size = {}
        box_color = {}
        text_color = {}
        stroke_color = {}
        spintax_time_type = {}
        randomizer = {}
        global x_axis_array, y_axis_array, pop_up_Texts
        total_length_pop = len(x_axis_array)

        num = 0
        if int(pop_up_1):
            text_size[1] = self.spinBox_8.value()
            spintax_time_type[1] = self.comboBox_5.currentText()
            if spintax_time_type[1] == "Start - End":
                start_1 = self.spinBox_16.value()
                end_1 = self.spinBox_15.value()
                spintax_time_type[1] = [spintax_time_type[1], start_1, end_1]
            elif spintax_time_type[1] == "x from end":
                sec_1 = self.spinBox_17.value()
                spintax_time_type[1] = [spintax_time_type[1], sec_1]
            else:
                spintax_time_type[1] = ["Full Duration"]
            text_color[1] = self.comboBox_4.currentText()
            box_color[1] = self.comboBox_3.currentText()
            stroke_color[1] = self.comboBox_23.currentText()
            randomizer[1] = self.spinBox_84.value()
            num += 1

        if int(pop_up_2):
            text_size[2] = self.spinBox_20.value()
            spintax_time_type[2] = self.comboBox_9.currentText()
            if spintax_time_type[2] == "Start - End":
                start_1 = self.spinBox_19.value()
                end_1 = self.spinBox_18.value()
                spintax_time_type[2] = [spintax_time_type[2], start_1, end_1]
            elif spintax_time_type[2] == "x from end":
                sec_1 = self.spinBox_23.value()
                spintax_time_type[2] = [spintax_time_type[2], sec_1]
            else:
                spintax_time_type[2] = ["Full Duration"]
            text_color[2] = self.comboBox_34.currentText()
            box_color[2] = self.comboBox_33.currentText()
            stroke_color[2] = self.comboBox_35.currentText()
            randomizer[2] = self.spinBox_86.value()
            num += 1

        if int(pop_up_3):
            text_size[3] = self.spinBox_26.value()
            spintax_time_type[3] = self.comboBox_12.currentText()
            if spintax_time_type[3] == "Start - End":
                start_1 = self.spinBox_25.value()
                end_1 = self.spinBox_24.value()
                spintax_time_type[3] = [spintax_time_type[3], start_1, end_1]
            elif spintax_time_type[3] == "x from end":
                sec_1 = self.spinBox_29.value()
                spintax_time_type[3] = [spintax_time_type[3], sec_1]
            else:
                spintax_time_type[3] = ["Full Duration"]
            text_color[3] = self.comboBox_37.currentText()
            box_color[3] = self.comboBox_36.currentText()
            stroke_color[3] = self.comboBox_38.currentText()
            randomizer[3] = self.spinBox_87.value()
            num += 1

        if int(pop_up_4):
            text_size[4] = self.spinBox_32.value()
            spintax_time_type[4] = self.comboBox_15.currentText()
            if spintax_time_type[4] == "Start - End":
                start_1 = self.spinBox_31.value()
                end_1 = self.spinBox_30.value()
                spintax_time_type[4] = [spintax_time_type[4], start_1, end_1]
            elif spintax_time_type[4] == "x from end":
                sec_1 = self.spinBox_35.value()
                spintax_time_type[4] = [spintax_time_type[4], sec_1]
            else:
                spintax_time_type[4] = ["Full Duration"]
            text_color[4] = self.comboBox_40.currentText()
            box_color[4] = self.comboBox_39.currentText()
            stroke_color[4] = self.comboBox_41.currentText()
            randomizer[4] = self.spinBox_88.value()
            num += 1

        if int(pop_up_5):
            text_size[5] = self.spinBox_38.value()
            spintax_time_type[5] = self.comboBox_18.currentText()
            if spintax_time_type[5] == "Start - End":
                start_1 = self.spinBox_37.value()
                end_1 = self.spinBox_36.value()
                spintax_time_type[5] = [spintax_time_type[5], start_1, end_1]
            elif spintax_time_type[5] == "x from end":
                sec_1 = self.spinBox_41.value()
                spintax_time_type[5] = [spintax_time_type[5], sec_1]
            else:
                spintax_time_type[5] = ["Full Duration"]
            text_color[5] = self.comboBox_43.currentText()
            box_color[5] = self.comboBox_42.currentText()
            stroke_color[5] = self.comboBox_44.currentText()
            randomizer[5] = self.spinBox_89.value()
            num += 1

        if int(pop_up_6):
            text_size[6] = self.spinBox_44.value()
            spintax_time_type[6] = self.comboBox_21.currentText()
            if spintax_time_type[6] == "Start - End":
                start_1 = self.spinBox_43.value()
                end_1 = self.spinBox_42.value()
                spintax_time_type[6] = [spintax_time_type[6], start_1, end_1]
            elif spintax_time_type[6] == "x from end":
                sec_1 = self.spinBox_47.value()
                spintax_time_type[6] = [spintax_time_type[6], sec_1]
            else:
                spintax_time_type[6] = ["Full Duration"]
            text_color[6] = self.comboBox_46.currentText()
            box_color[6] = self.comboBox_45.currentText()
            stroke_color[6] = self.comboBox_47.currentText()
            randomizer[6] = self.spinBox_90.value()
            num += 1

        #For PopUp Only
        print("Text Size Dictionary : ", text_size)
        print("Text color Dictionary : ", text_color)
        print("box color Dictionary : ", box_color)
        print("stroke color Dictionary : ", stroke_color)
        print("spintax_time_type Dictionary : ", spintax_time_type)
        print("Text Size Dictionary : ", text_size)
        print("X AXIS : ", x_axis_array)
        print("Y AXIS : ", y_axis_array)
        print("the pop up texts are  : ", pop_up_Texts)
        print("TOTAL VALUES TO UNPACK : ", total_length_pop)

        if int(pop_up_1):
            # x=1080 y=1920
            self.renderStatusPlaceholder.setText("Adding Pop Up Text")

            tempoutputfiles = os.listdir("merged") #for only spintax functionality required
            if len(tempoutputfiles) == 0:
                print("Copying Background videos")
                for ele in os.listdir(mainPath):
                    src = mainPath + "/" + ele
                    print(src, "merged")
                    shutil.copy(src, "merged")
            time.sleep(5)

            def text_formatter_for_pop_up(message):
                messagelist = []
                temp = ""
                line_size = 0
                letter_count = 0
                for word in message:
                    letter_count += 1
                    for ele in word:
                        letter_count += 1
                    if letter_count <= 30:
                        temp += word + " "
                    else:
                        temp = temp[:-1]
                        messagelist.append(temp)
                        temp = word + " "
                        letter_count = 0
                if temp:
                    messagelist.append(temp[:-1])
                return messagelist

            #popupfiles linear function
            for y in tempoutputfiles:
                tempoutputPathExactFile = f"merged/{y}"
                first_file = y.split(".")[0]
                filename = first_file + "_" + "pop_up_" + str(num)

                q = "ffmpeg -i " + tempoutputPathExactFile + " -vf \"[in]"

                for index in range(1, total_length_pop + 1):
                    textsize = text_size[index]
                    boxcolor = box_color[index]
                    textcolor = text_color[index]
                    strokecolor = stroke_color[index]
                    spintaxtimetype = spintax_time_type[index]

                    textcolor = str.lower(textcolor)
                    strokecolor = str.lower(strokecolor)
                    boxcolor = str.lower(boxcolor)

                    disablestroke = False
                    disablebox = False
                    if strokecolor == "disable":
                        disablestroke = True
                    if boxcolor == "disable":
                        disablebox = True

                    print(" stroke : ", strokecolor)
                    print(" box : ", boxcolor)

                    path_sec = tempoutputPathExactFile
                    data = cv2.VideoCapture(path_sec)
                    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
                    fps = int(data.get(cv2.CAP_PROP_FPS))
                    ending = int(frames / fps)

                    if spintaxtimetype[0] == "Full Duration":
                        start = 0
                        end = ending
                    elif spintaxtimetype[0] == "Start - End":
                        start = spintaxtimetype[1]
                        end = spintaxtimetype[2]
                    elif spintaxtimetype[0] == "x from end":
                        start = ending - int(spintaxtimetype[1])
                        end = ending
                    print("Start and end time : ", start, end, spintaxtimetype[0])
                    time_stamp = "'between(t," + str(start) + "," + str(end) + ")'"

                    x_pop_up = x_axis_array[index]
                    y_pop_up = y_axis_array[index]
                    random_offset = randomizer[index]
                    text = pop_up_Texts[index]
                    spinnedMessage = spintax.spin(text).split(" ")


                    add_xaxis = bool(random.getrandbits(1))
                    add_yaxis = bool(random.getrandbits(1))

                    if add_xaxis:
                        x_pop_up += random.randint(0,random_offset)
                    else:
                        x_pop_up -= random.randint(0,random_offset)

                    if add_yaxis:
                        y_pop_up += random.randint(0,random_offset)
                    else:
                        y_pop_up -= random.randint(0,random_offset)

                    messagelist = text_formatter_for_pop_up(spinnedMessage)
                    print("The messagelist is : ", messagelist)
                    y_axis = y_pop_up
                    for ele in messagelist:
                        q += "drawtext=fontsize="+str(textsize)+":fontcolor="+textcolor

                        if not disablebox:  # enable background box
                            q += ":box=1:boxcolor="+boxcolor+"@0.6: boxborderw=5"

                        if not disablestroke:  # enable stroke of text
                            q += ":borderw=4:bordercolor="+strokecolor

                        q += ":fontfile= " + str(fontPath) + " :text='" + ele + "':x=" + str(x_pop_up) + ":y=" + str(y_axis)
                        q += ":enable=" + time_stamp + ", "


                        y_axis += textsize

                q = q[:-2]
                q += "\""
                q += f" -y tempoutput/{filename}.mp4"
                print(q)

                try:
                    os.system(f"""{q}""")
                except:
                    pass

                curr_iters += 1
                progress_bar_status = int((curr_iters / total_iters) * 100)
                self.progressBar.setValue(progress_bar_status)
                print("% Completed  : {}/100".format(progress_bar_status))
                total_videos_rendered += 1

                if not int(music_checkbox):
                    self.renderStatusPlaceholder_3.setText(str(total_videos_rendered))
                    if total_videos_rendered == stop_here:
                        break

        else:
            # Adding PopUp to the directories
            print("Adding PopUp to the directories no pop UP APPLIED")
            for ele in os.listdir("merged"):
                src = "merged/" + ele
                shutil.copy(src, "tempoutput")

        # For music Only
        if int(checkbox2):
            self.renderStatusPlaceholder.setText("Merging Audio")
            # combining music to video
            m2 = os.listdir('tempoutput')
            musicPathFiles = os.listdir("tempmusic")

            '''audio_array = []
            for ele in os.listdir("final_audio"):
                audio_array.append(ele)

            print("THE AUDIO ARRAY IS : ", audio_array)

            for videofile in os.listdir("tempoutput"):
                videoname = videofile.split("_")[0]
                for audiofile in musicPathFiles:
                    videopart = audiofile.split("___")[0]
                    audiopart = audiofile.split("___")[1]

                    if videoname != videopart:
                        continue
                    else:
                        video = "tempoutput/" + videofile
                        audio = "final_audio/" + audiofile
                        output = outputPath + "/" + videofile.split(".")[0] + "___" + audiopart + ".mp4"
                        q = "ffmpeg.exe -i {} -i {} -map 0:v -map 1:a -c copy -y {}".format(video,audio,output)

                        try:
                            os.system(f"""{q}""")
                        except:
                            pass'''

            for x in musicPathFiles:
                if total_videos_rendered == stop_here:
                    break
                for y in m2:
                    x1 = f"tempmusic\{x}"
                    y1 = f"tempoutput\{y}"

                    first_file = y.split(".")[0]
                    second_file = x.split(".")[0]
                    fname = first_file + "_" + second_file

                    if remove_audio:
                        try:
                            os.system(f"""ffmpeg -i {y1} -i {x1} -map 0:v -map 1:a -c:v copy -shortest {outputPath}/{fname}.mp4""")
                        except:
                            pass
                    else:
                        try:
                            os.system(f"""ffmpeg -i {y1} -i {x1} -filter_complex amix -map 0:v -map 0:a -map 1:a -shortest {outputPath}/{fname}.mp4""")
                        except:
                            pass

                    curr_iters += 1

                    progress_bar_status = int((curr_iters / total_iters) * 100)
                    self.progressBar.setValue(progress_bar_status)
                    print("% Completed  : {}/100".format(progress_bar_status))

                    total_videos_rendered += 1
                    self.renderStatusPlaceholder_3.setText(str(total_videos_rendered))
                    if total_videos_rendered == stop_here:
                        break
        else:
            # MOVING FILES FROM tempoutput to outputpath
            print("MOVING FILES FROM tempoutput to outputpath NO MUSIC APPLIED")
            for ele in os.listdir("tempoutput"):
                src = "tempoutput/" + ele
                shutil.copy(src, outputPath)

        print("Current iter number : ", curr_iters)
        self.renderStatusPlaceholder.setText("Rendering completed")
        time.sleep(5)
        self.renderStatusPlaceholder.setText("Task Completed Successfully")
        exit(0)

app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()

'''
        else:
            # only image
            curr_iters = 0
            total_iters = (len(mainPathFiles) * len(imagepathfiles))

            if int(checkbox2):
                total_iters += (len(mainPathFiles) * len(imagepathfiles) * len(musicPathfiles))

            print(total_iters)
            if image_check_box:
                self.renderStatusPlaceholder.setText("Interlacing Image")
                mainPathFiles = os.listdir(mainPath)
                imagePathFiles = os.listdir('tempimg')
                for y in mainPathFiles:
                    for x in imagePathFiles:
                        mainPathExactFile = f"{mainPath}/{y}"
                        imagePathExactFile = f"tempimg/{x}"
                        first_file = y.split(".")[0]
                        second_file = x.split(".")[0]
                        filename = first_file + "_" + second_file

                        if int(checkbox2):
                            filename_f = "merged/" + filename + ".mp4"
                        else:
                            filename_f = outputPath + filename + ".mp4"

                        q = "ffmpeg -i {} -i {} -filter_complex \"[0:v][1:v] overlay=(W-w)/2:(H-h)/{}\" -pix_fmt yuv420p -c:a copy {} ".format(
                            mainPathExactFile, imagePathExactFile, y_pos, filename_f)

                        try:
                            pass
                            os.system(f"""{q}""")
                        except:
                            pass

                        curr_iters += 1
                        progress_bar_status = int((curr_iters / total_iters) * 100)
                        self.progressBar.setValue(progress_bar_status)
                        print("% Completed  : {}/100".format(progress_bar_status))

            if int(checkbox2):
                m2 = os.listdir('merged')
                musicPathFiles = os.listdir("tempmusic")
                self.renderStatusPlaceholder.setText("Merging Music")
                for x in musicPathFiles:
                    for y in m2:
                        x1 = f"tempmusic\{x}"
                        y1 = f" merged\{y}"
                        # fname = get_random_string(10)

                        first_file = y.split(".")[0]
                        second_file = x.split(".")[0]
                        fname = first_file + "_" + second_file

                        try:
                            os.system(
                                f"""ffmpeg -i {y1} -i {x1} -map 0:v -map 1:a -c:v copy -shortest tempoutput/{fname}.mp4 """)
                        except:
                            pass

                        curr_iters += 1
                        progress_bar_status = int((curr_iters / total_iters) * 100)
                        self.progressBar.setValue(progress_bar_status)
                        print("% Completed  : {}/100".format(progress_bar_status))'''