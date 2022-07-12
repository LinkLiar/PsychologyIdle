import pyautogui
import cv2
import random
import win32api
import win32con
import win32gui
import time
import numpy
import pandas as pd
import os
import pyperclip
from win32.lib import win32con
import win32api, win32gui, win32print
import math

def GetResolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    width = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    height = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return (width, height)

def GetSpecificWindowRegion(titleName, verbose = True,alert = True):
    width, height = GetResolution()
    if(verbose):
        print(F"Current Screen's Resolution:\t{width} x {height}")
    handle = win32gui.FindWindow(0, titleName)
    if handle == 0:
        return None
    else:
        x1 = win32gui.GetWindowRect(handle)[0]
        y1 = win32gui.GetWindowRect(handle)[1]
        x2 = win32gui.GetWindowRect(handle)[2]
        y2 = win32gui.GetWindowRect(handle)[3]

        x2 = x2 - 1
        y2 = y2 - 1
        if (pyautogui.onScreen((x1, y1)) & pyautogui.onScreen(x2, y2)):
            if(verbose):

            if(alert):
                pyautogui.alert(F'窗口识别完成，自动点击已部署')
            return win32gui.GetWindowRect(handle)
        else:
            return None


def CheckIsOutOfArea(windowRegion):
    mouseX = pyautogui.position()[0]
    mouseY = pyautogui.position()[1]
    if (mouseX < windowRegion[0] | mouseX > windowRegion[2] | mouseY < windowRegion[1] | mouseY > windowRegion[2]):
        pyautogui.alert('鼠标移出区域，暂停中...')


def WaitUntilShow(imagePath, windowRegion, confidence=1, timeoutThreshold=10):
    tic = toc =time.perf_counter()
    timeComsume = 0
    while (True):
        haveFlag = pyautogui.locateCenterOnScreen(imagePath, region=windowRegion, confidence=confidence)
        if (haveFlag != None):
            break
        toc = time.perf_counter()
        timeComsume = toc - tic
        if (timeComsume > timeoutThreshold):
            return True
    print(f"Wait {imagePath} for {timeComsume} second")
    return False


def Screenshot(windowRegion, savePath="", convertTo="OpenCV"):
    print(windowRegion)
    if (windowRegion[0] == 0 and windowRegion[1] == 0 and windowRegion[2] == 0 and windowRegion[3] == 0):
        imagePIL = pyautogui.screenshot()
    else:
        imagePIL = pyautogui.screenshot(region=(
            windowRegion[0], windowRegion[1], windowRegion[2] - windowRegion[0], windowRegion[3] - windowRegion[1]))
    if (savePath != ""):
        imagePIL.save(savePath)
    if (convertTo == "OpenCV"):
        imageOpenCV = cv2.cvtColor(numpy.asarray(imagePIL), cv2.COLOR_RGB2BGR)
        return imageOpenCV
    else:
        return imagePIL

def addName(unseccussfullyName):
    with open("unseccussfulName.txt", "a") as file:
        file.write(str(unseccussfullyName) + "\n")

def saveROI(ROI):
    with open("ROI.txt", "w") as file:
        for i in range(4):
            file.write(str(ROI[i]) + "\n")

def addError(name):
    with open("errorTmp.txt", "a") as file:
        file.write(str(name) + "\n")

def clearError():
    with open("errorTmp.txt", "w") as file:
        file.write("")

backgroundColor = (247, 247, 247)
firstStepImage = "first.png"
secondStepImage = "second.png"
nameImgPath = "name.png"
idImgPath = "id.png"
phoneImgPath = "phone.png"
detailImgPath = "detail.png"
submitImgPath = "submit.png"
sureImgPath = "sure.png"

searchNameImgPath = "searchName.png"
searchImgPath = "search.png"
enterImgPath = "enter.png"
blueBlockImgPath = "blueBlock.png"
returnImgPath = "return.png"

cityImgPath = "city.png"
areaImgPath = "area.png"
greenSureImgPath = "greenSure.png"
guipingImgPath = "guiping.png"

deleteImgPath = "delete.png"
rebootImgPath = "reboot.png"
def main():
    windowRegion = GetWindowRegion()
    tendToLocateROI = Screenshot(windowRegion)
    leftStartX = leftEndX = windowRegion[0] + 500
    rightStartX = rightEndX = windowRegion[2] - 500
    upStartY = upEndY = windowRegion[1]
    downStartY = downEndY = windowRegion[3] - 2
    validFlags = [False, False, False, False]
    while (True):
        if (pyautogui.pixel(leftEndX + 1, upStartY + 100) == backgroundColor):
            leftEndX += 1
        else:
            validFlags[0] = True
        if (pyautogui.pixel(rightEndX - 1, upStartY + 100) == backgroundColor):
            rightEndX -= 1
        else:
            validFlags[2] = True
        if (pyautogui.pixel(int((leftStartX + rightStartX) / 2), upEndY) == backgroundColor):
            upEndY += 1
        else:
            validFlags[1] = True
        if (pyautogui.pixel(int((leftStartX + rightStartX) / 2), downEndY) == backgroundColor):
            downEndY -= 1
        else:
            validFlags[3] = True

        breakFlag = True
        for i in range(4):
            if not validFlags[i]:
                breakFlag = False
        if breakFlag:
            break
    print("LeftBoundary:\t" + str(leftEndX))
    print("RightBoundary:\t" + str(rightEndX))
    print("UpBoundary:\t" + str(upEndY))
    print("DownBoundary:\t" + str(downEndY))
    excelPaths = ".//now"
    excels = os.listdir(excelPaths)
    for excel in excels:
        excelPath = excelPaths + '//' + excel
        df = pd.read_excel(excelPath)
        print("total: " + str(df.shape[0]))
        statusPath = ""
        QRCodeFilesPath = ".\\QRCodeFiles"
        if not os.path.exists(QRCodeFilesPath):
            os.makedirs(QRCodeFilesPath)
        generatedInfos = os.listdir(QRCodeFilesPath)
        generatedIds = []
        for info in generatedInfos:
            fileName = os.path.splitext(info)[0]
            print(fileName.split('_'))
            id = fileName.split('_')[2]
            generatedIds.append(id)
        print(F"Loaded {len(generatedIds)} Generated Infos Successfully... ")
        print("---------------------------------------")
        print("Starting Generate...")
        loadFinishedFlag = False
        startIndex = 0

        ROI = (leftEndX, upEndY, rightEndX, downEndY)
        saveROI(ROI)
        WaitUntilShow(firstStepImage, ROI, confidence=0.9, timeoutThreshold=20)
        crossLocation = pyautogui.locateCenterOnScreen(firstStepImage, region=ROI, confidence=0.9)
        pyautogui.moveTo(crossLocation[0], crossLocation[1])
        pyautogui.click(clicks=2)
        time.sleep(2)
        for i in range(df.shape[0]):
            row = df.iloc[i]
            if (str(row['身份证']) in generatedIds):
                continue
            else:
                startIndex = i
                break

        unseccussfullyNamePath = os.path.expanduser('./unseccussfulName.txt')
        with open(unseccussfullyNamePath,'r') as f:
            unseccussfullyNames = f.readlines()
        unseccussfullyNames = [c.strip() for c in unseccussfullyNames]

        for i in range(startIndex, df.shape[0]):
            print(F"Todo: {i}/{df.shape[0]-1}")
            if (str(df.iloc[i]['姓名']) in unseccussfullyNames):
                continue
            if (math.isnan(int(df.iloc[i]['电话'])) or len(str(df.iloc[i]['电话'])) != 11):
                addName(df.iloc[i]['姓名'])
                continue    
            if (str(df.iloc[i]['身份证']) in generatedIds):
                continue

            addError(df.iloc[i]['姓名'])

            WaitUntilShow(secondStepImage, ROI, confidence=0.9, timeoutThreshold=20)
            crossLocation = pyautogui.locateCenterOnScreen(secondStepImage, region=ROI, confidence=0.9)
            pyautogui.moveTo(crossLocation[0], crossLocation[1])
            pyautogui.click(clicks=2)
            time.sleep(0.1)
            WaitUntilShow(nameImgPath, ROI, confidence=0.9, timeoutThreshold=20)
            time.sleep(0.1)
            crossLocation = pyautogui.locateCenterOnScreen(nameImgPath, region=ROI, confidence=0.9)
            pyautogui.moveTo(crossLocation[0], crossLocation[1])
            pyautogui.click(clicks=1)
            pyautogui.moveTo(crossLocation[0]+5, crossLocation[1])
            pyautogui.click(clicks=1)
            time.sleep(0.1)
            pyperclip.copy(df.iloc[i]['姓名'])
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            WaitUntilShow(idImgPath, ROI, confidence=0.9, timeoutThreshold=10)
            crossLocation = pyautogui.locateCenterOnScreen(idImgPath, region=ROI, confidence=0.9)
            pyautogui.moveTo(crossLocation[0], crossLocation[1])
            pyautogui.click(clicks=2)
            time.sleep(0.1)
            pyperclip.copy(str(df.iloc[i]['身份证']))
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            WaitUntilShow(phoneImgPath, ROI, confidence=0.9, timeoutThreshold=10)
            crossLocation = pyautogui.locateCenterOnScreen(phoneImgPath, region=ROI, confidence=0.9)
            pyautogui.moveTo(crossLocation[0], crossLocation[1])
            pyautogui.click(clicks=2)
            time.sleep(0.1)
            pyperclip.copy(str(df.iloc[i]['电话']))
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)

            WaitUntilShow(cityImgPath, ROI, confidence=0.9, timeoutThreshold=10)
            crossLocation = pyautogui.locateCenterOnScreen(cityImgPath, region=ROI, confidence=0.9)
            pyautogui.moveTo(crossLocation[0], crossLocation[1])
            pyautogui.click(clicks=1)

            WaitUntilShow(greenSureImgPath, ROI, confidence=0.9, timeoutThreshold=10)
            greenSurecrossLocation = pyautogui.locateCenterOnScreen(greenSureImgPath, region=ROI, confidence=0.9)
            pyautogui.moveTo(greenSurecrossLocation[0]-200, greenSurecrossLocation[1]-100)
            time.sleep(0.1)
            pyautogui.scroll(-10)
            time.sleep(0.8)
            pyautogui.scroll(-10)
            time.sleep(0.8)
            WaitUntilShow("guigang.png", windowRegion, confidence=0.7, timeoutThreshold=10)
            crossLocation = pyautogui.locateCenterOnScreen("guigang.png", region=windowRegion, confidence=0.9)
            pyautogui.moveTo(crossLocation[0], crossLocation[1])
            pyautogui.click(clicks=1)
            time.sleep(0.5)
            pyautogui.moveTo(greenSurecrossLocation[0]+100, greenSurecrossLocation[1]-100)
            pyautogui.scroll(-10)
            time.sleep(0.1)
            WaitUntilShow(guipingImgPath, ROI, confidence=0.9, timeoutThreshold=10)
            crossLocation = pyautogui.locateCenterOnScreen(guipingImgPath, region=windowRegion, confidence=0.9)
            pyautogui.moveTo(crossLocation[0], crossLocation[1])
            pyautogui.click(clicks=1)
            time.sleep(0.1)
            pyautogui.moveTo(greenSurecrossLocation[0], greenSurecrossLocation[1])
            pyautogui.click(clicks=1)
            time.sleep(0.5)
            WaitUntilShow(areaImgPath, ROI, confidence=0.9, timeoutThreshold=10)
            crossLocation = pyautogui.locateCenterOnScreen(areaImgPath, region=ROI, confidence=0.9)
            pyautogui.moveTo(crossLocation[0], crossLocation[1])
            pyautogui.click(clicks=1)
            time.sleep(0.8)
            pyautogui.moveTo(greenSurecrossLocation[0]-200, greenSurecrossLocation[1]-100)
            time.sleep(0.1)
            pyautogui.scroll(-10)
            time.sleep(0.8)
            pyautogui.scroll(-10)
            time.sleep(0.8)
            pyautogui.scroll(-10)
            time.sleep(0.8)
            pyautogui.scroll(-10)
            time.sleep(0.8)
            pyautogui.scroll(-10)
            time.sleep(0.8)
            pyautogui.scroll(-10)
            time.sleep(0.8)

            WaitUntilShow("jintian.png", windowRegion, confidence=0.7, timeoutThreshold=10)
            crossLocation = pyautogui.locateCenterOnScreen("jintian.png", region=windowRegion, confidence=0.9)
            pyautogui.moveTo(crossLocation[0], crossLocation[1])
            pyautogui.click(clicks=1)
            time.sleep(0.5)
            pyautogui.moveTo(greenSurecrossLocation[0], greenSurecrossLocation[1])
            pyautogui.click(clicks=1)

            time.sleep(0.5)
            WaitUntilShow(detailImgPath, ROI, confidence=0.9, timeoutThreshold=10)
            crossLocation = pyautogui.locateCenterOnScreen(detailImgPath, region=ROI, confidence=0.9)
            pyautogui.moveTo(crossLocation[0], crossLocation[1])
            pyautogui.click(clicks=2)
            time.sleep(0.1)
            pyperclip.copy(str(df.iloc[i]['地址']))
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)


            WaitUntilShow(submitImgPath, ROI, confidence=0.9, timeoutThreshold=10)
            crossLocation = pyautogui.locateCenterOnScreen(submitImgPath, region=ROI, confidence=0.9)
            pyautogui.moveTo(crossLocation[0], crossLocation[1])
            pyautogui.click(clicks=2)
            time.sleep(0.1)

            WaitUntilShow(sureImgPath, ROI, confidence=0.9, timeoutThreshold=10)
            crossLocation = pyautogui.locateCenterOnScreen(sureImgPath, region=ROI, confidence=0.9)
            pyautogui.moveTo(crossLocation[0], crossLocation[1])
            pyautogui.click(clicks=2)
            time.sleep(0.1)

            while(True):
                haveFlag = pyautogui.locateCenterOnScreen(nameImgPath, region=ROI, confidence=0.9)
                if (haveFlag != None): 
                    WaitUntilShow(returnImgPath, ROI, confidence=0.9, timeoutThreshold=10)
                    crossLocation = pyautogui.locateCenterOnScreen(returnImgPath, region=ROI, confidence=0.9)
                    pyautogui.moveTo(crossLocation[0], crossLocation[1])
                    pyautogui.click(clicks=2)
                    time.sleep(0.1)
                breakFlag = pyautogui.locateCenterOnScreen(searchNameImgPath, region=ROI, confidence=0.9)
                if (breakFlag != None): 
                    break


            WaitUntilShow(searchNameImgPath, ROI, confidence=0.9, timeoutThreshold=10)
            crossLocationSearch = pyautogui.locateCenterOnScreen(searchNameImgPath, region=ROI, confidence=0.9)

            while(True):
                pyautogui.moveTo(crossLocationSearch[0]+20, crossLocationSearch[1])
                pyautogui.click(clicks=1)
                time.sleep(0.1)
                pyperclip.copy(str(df.iloc[i]['姓名']))
                pyautogui.hotkey('ctrl', 'v')

                crossLocation = pyautogui.locateCenterOnScreen(deleteImgPath, region=ROI, confidence=0.9)
                if(crossLocation != None):
                    pyautogui.moveTo(crossLocation[0], crossLocation[1])
                    pyautogui.click(clicks=1)
                    pyautogui.moveTo(crossLocation[0]+3, crossLocation[1])
                    pyautogui.click(clicks=1)
                    time.sleep(0.1)
                    break

            pyautogui.moveTo(crossLocationSearch[0]+20, crossLocationSearch[1])
            pyautogui.click(clicks=1)
            pyautogui.moveTo(crossLocationSearch[0]+30, crossLocationSearch[1])
            pyautogui.click(clicks=1)
            time.sleep(0.1)
            pyperclip.copy(str(df.iloc[i]['姓名']))
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            WaitUntilShow(searchImgPath, ROI, confidence=0.9, timeoutThreshold=10)
            crossLocation = pyautogui.locateCenterOnScreen(searchImgPath, region=ROI, confidence=0.9)
            pyautogui.moveTo(crossLocation[0], crossLocation[1])
            pyautogui.click(clicks=2)
            time.sleep(0.1)

            unseccussfullyFlag = True

            for _ in range(5):
                crossLocation = pyautogui.locateCenterOnScreen(enterImgPath, region=ROI, confidence=0.9)
                if(crossLocation != None):
                    unseccussfullyFlag = False
                    break
                time.sleep(1)
            if(unseccussfullyFlag): 
                addName(df.iloc[i]['姓名'])
                continue

            WaitUntilShow(enterImgPath, ROI, confidence=0.9, timeoutThreshold=10)
            crossLocation = pyautogui.locateCenterOnScreen(enterImgPath, region=ROI, confidence=0.9)
            pyautogui.moveTo(crossLocation[0], crossLocation[1])
            pyautogui.click(clicks=2)
            time.sleep(0.1)
            pyautogui.moveTo(crossLocation[0]-5, crossLocation[1])
            pyautogui.click(clicks=1)
            time.sleep(1)
            WaitUntilShow(blueBlockImgPath, ROI, confidence=0.9, timeoutThreshold=30)
            crossLocation = pyautogui.locateCenterOnScreen(blueBlockImgPath, region=ROI, confidence=0.9)

            accurateROI = (ROI[0],ROI[1]+100,ROI[2],ROI[3]-25)
            time.sleep(1)
            pyautogui.moveTo(crossLocation[0], crossLocation[1])
            pyautogui.dragRel(0, -85, 1)
            time.sleep(0.5)
            Screenshot(accurateROI, savePath = QRCodeFilesPath +'\\'+ str(df.iloc[i]['村镇名']) + '_' + str(df.iloc[i]['姓名']) + '_' + str(df.iloc[i]['身份证']) + '.png')
            time.sleep(0.1)
            clearError()
            
            WaitUntilShow(returnImgPath, ROI, confidence=0.9, timeoutThreshold=10)
            crossLocation = pyautogui.locateCenterOnScreen(returnImgPath, region=ROI, confidence=0.9)
            pyautogui.moveTo(crossLocation[0], crossLocation[1])
            pyautogui.click(clicks=1)
            pyautogui.moveTo(crossLocation[0]+3, crossLocation[1])
            pyautogui.click(clicks=1)
            time.sleep(0.1)

if __name__ == '__main__':

    while(True):
        try:
            main()
        except:
            print("An exception occurred...Rebooting")
            roiTXTPath = os.path.expanduser('./ROI.txt')
            with open(roiTXTPath,'r') as f:
                roiList = f.readlines()
            roiList = [c.strip() for c in roiList]
            ROI =(int(roiList[0]),int(roiList[1]),int(roiList[2]),int(roiList[3]))
            print(ROI)

            errorTXTPath = os.path.expanduser('./errorTmp.txt')
            with open(errorTXTPath,'r') as f:
                errorList = f.readlines()
            errorList = [c.strip() for c in errorList]
            if(len(errorList) > 2):
                addName(errorList[0])
                clearError()
            
            while(True):
                crossLocation = pyautogui.locateCenterOnScreen(returnImgPath, region=ROI, confidence=0.9)
                if(crossLocation != None):
                    pyautogui.moveTo(crossLocation[0], crossLocation[1])
                    pyautogui.click(clicks=1)
                    pyautogui.moveTo(crossLocation[0]+3, crossLocation[1])
                    pyautogui.click(clicks=1)
                greenSurecrossLocation = pyautogui.locateCenterOnScreen(greenSureImgPath, region=ROI, confidence=0.9)
                if(greenSurecrossLocation != None):
                    pyautogui.moveTo(greenSurecrossLocation[0], greenSurecrossLocation[1])
                    pyautogui.click(clicks=1)
                    pyautogui.moveTo(greenSurecrossLocation[0]+5, greenSurecrossLocation[1])
                    pyautogui.click(clicks=1)
                breakFlag = pyautogui.locateCenterOnScreen(rebootImgPath, region=ROI, confidence=0.9)
                if (breakFlag != None): 
                    break