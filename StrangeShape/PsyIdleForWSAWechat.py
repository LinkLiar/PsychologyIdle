import pyautogui
import cv2
import random
import win32api
import win32con
import win32gui
import time
import numpy
import math
labelName = "com.tencent.mm"
titleName = "WeChat"

def Median(data):
    data = sorted(data)
    size = len(data)
    if size % 2 == 0: # 判断列表长度为偶数
        median = (data[size//2]+data[size//2-1])/2
        data[0] = median
    if size % 2 == 1: # 判断列表长度为奇数
        median = data[(size-1)//2]
        data[0] = median
    return data[0]

def FindMinIndex(set):
    minIndex = -1
    min = 999999
    for i in range(0,len(set)):
        if(len(set[i]) < min):
            minIndex = i
            min = len(set[i])
    return minIndex

def GetWindowRegion():
    handle = win32gui.FindWindow(0, titleName)
    if handle == 0:
        return None
    else:
        x1 = win32gui.GetWindowRect(handle)[0]
        y1 = win32gui.GetWindowRect(handle)[1]
        x2 = win32gui.GetWindowRect(handle)[2]
        y2 = win32gui.GetWindowRect(handle)[3]
        print(win32gui.GetWindowRect(handle))

        if(pyautogui.onScreen((x1, y1)) & pyautogui.onScreen(x2, y2)):
            pyautogui.alert('窗口识别完成，自动点击已部署')
            return win32gui.GetWindowRect(handle)
        else:
            return None


def CheckIsOutOfArea(windowRegion):
    mouseX = pyautogui.position()[0]
    mouseY = pyautogui.position()[1]
    if(mouseX < windowRegion[0] | mouseX > windowRegion[2] | mouseY < windowRegion[1] | mouseY > windowRegion[2]):
        pyautogui.alert('鼠标移出区域，暂停中...')


def WaitUntilShow(imagePath, windowRegion, confidence=1, timeoutThreshold=10):
    tic = time.perf_counter()
    while(True):
        haveFlag = pyautogui.locateAllOnScreen(
            imagePath, region=windowRegion, confidence=confidence)
        if(haveFlag):
            break
    toc = time.perf_counter()
    timeComsume = toc-tic
    if(timeComsume > timeoutThreshold):
        pyautogui.alert('WaitUntilShow Timeout...')
    else:
        print(f"Wait {imagePath} for {timeComsume} second")


def Screenshot(windowRegion, savePath="", convertTo="PIL"):
    if(windowRegion[0] == 0 & windowRegion[1] == 0 & windowRegion[2] == 0 & windowRegion[3] == 0):
        imagePIL = pyautogui.screenshot()
    else:
        imagePIL = pyautogui.screenshot(region=(
            windowRegion[0], windowRegion[1], windowRegion[2]-windowRegion[0], windowRegion[3]-windowRegion[1]))
    if(savePath != ""):
        imagePIL.save(savePath)
    if(convertTo == "OpenCV"):
        imageOpenCV = cv2.cvtColor(numpy.asarray(imagePIL), cv2.COLOR_RGB2BGR)
        return imageOpenCV
    else:
        return imagePIL


def main():
    imageCrossPath = "cross.png"
    imagefailPath = "fail.png"
    imageContinuePath = "continueForWSA.png"
    windowRegion = GetWindowRegion()
    X = windowRegion[0]
    Y = windowRegion[1]
    print(F"X , Y = {X} , {Y} ")
    backgroundColor = (128, 128, 128)
    WHITE = (255, 255, 255)

    continueX, continueY = pyautogui.locateCenterOnScreen(
        imageContinuePath, region=windowRegion, confidence=0.5)
    pyautogui.moveTo(continueX, continueY)
    pyautogui.click(clicks=2)
    image = Screenshot(windowRegion,convertTo="OpenCV")
    height = image.shape[0]
    width = image.shape[1]
    startHeight = 0
    endHeight = 0

    for position in range(100,height):
        color= image[position,int(width/2)]
        if((color == WHITE).all() and startHeight == 0):
            startHeight = position
        if((color != WHITE).any() and startHeight !=0 and endHeight == 0):
            endHeight = position

    startWidth = 0
    endWidth = 0
    for position in range(10,width):
        color = image[int(height/2),position]
        if((color == WHITE).all() and startWidth == 0):
            startWidth = position
        if((color != WHITE).any() and startWidth !=0 and endWidth == 0):
            endWidth = position

    squareRegion = (windowRegion[0]+startWidth,windowRegion[1] + startHeight,windowRegion[2]-width+endWidth,windowRegion[3] - height + endHeight)

    while(windowRegion != None):
        CheckIsOutOfArea(windowRegion)
        time.sleep(0.1)

        failLocation = pyautogui.locateCenterOnScreen(imagefailPath, region=windowRegion, confidence=0.9)
        if(failLocation != None):
            # break
            pass
        continueLocation = pyautogui.locateCenterOnScreen(imageContinuePath, region=windowRegion, confidence=0.9)
        if(continueLocation != None):
                pyautogui.moveTo(continueLocation[0], continueLocation[1])
                pyautogui.click(clicks=2)
        image = Screenshot(squareRegion,convertTo="OpenCV")

        height = image.shape[0]
        width = image.shape[1]
      
        tlArea = image[0:int(height/4),0:int(width/4)]
        trArea = image[0:int(height/4),int(width/2):int(3*width/4)]
        blArea = image[int(height/2):int(3*height/4),0:int(width/4)]
        brArea = image[int(height/2):int(3*height/4),int(width/2):int(3*width/4)]

        tlgray=cv2.cvtColor(tlArea,cv2.COLOR_BGR2GRAY)
        _, tlArea = cv2.threshold(tlgray, 0, 255, cv2.THRESH_OTSU)         
        trgray=cv2.cvtColor(trArea,cv2.COLOR_BGR2GRAY)
        _, trArea = cv2.threshold(trgray, 0, 255, cv2.THRESH_OTSU)         
        blgray=cv2.cvtColor(blArea,cv2.COLOR_BGR2GRAY)
        _, blArea = cv2.threshold(blgray, 0, 255, cv2.THRESH_OTSU) 
        brgray=cv2.cvtColor(brArea,cv2.COLOR_BGR2GRAY)
        _, brArea = cv2.threshold(brgray, 0, 255, cv2.THRESH_OTSU) 

        tlHist = tlArea.ravel()
        trHist = trArea.ravel()
        blHist = blArea.ravel()
        brHist = brArea.ravel()

        tlBlackCount = 0
        trBlackCount = 0
        blBlackCount = 0
        brBlackCount = 0
        for i in tlHist:
            if(i == 0):
                tlBlackCount+=1    # 第二象限
        for i in trHist:
            if(i == 0):
                trBlackCount+=1    # 第一象限
        for i in blHist:
            if(i == 0):
                blBlackCount+=1    # 第三象限
        for i in brHist:
            if(i == 0):
                brBlackCount+=1    # 第四象限

        if(tlBlackCount < 100):
            continue
        print("2 = "+str(tlBlackCount))
        print("1 = "+str(trBlackCount))
        print("3 = "+str(blBlackCount))
        print("4 = "+str(brBlackCount))

        hist = [trBlackCount,tlBlackCount,blBlackCount,brBlackCount]
    
        answerPositon = -1
        median = Median(hist)
        print(F"median = {median}")
        print(max(hist) - min(hist))
        if(max(hist) - min(hist) > 0.05 * median): #max(hist) - min(hist) > 0.05 * median
            if(max(hist) - median >  median - min(hist)):
                answerPositon = hist.index(max(hist))
            else:
                answerPositon = hist.index(min(hist))
        else:
            print("Checking Again in detail...")
            print(F"difer = {max(hist) - min(hist)}")
            cv2.imwrite("tl.png", tlArea) 
            cv2.imwrite("tr.png", trArea) 
            cv2.imwrite("bl.png", blArea) 
            cv2.imwrite("br.png", brArea) 

            tlCntsSet,_ = cv2.findContours(cv2.bitwise_not(tlArea), cv2.RETR_EXTERNAL, cv2.RETR_LIST)
            trCntsSet,_ = cv2.findContours(cv2.bitwise_not(trArea), cv2.RETR_EXTERNAL, cv2.RETR_LIST)
            blCntsSet,_ = cv2.findContours(cv2.bitwise_not(blArea), cv2.RETR_EXTERNAL, cv2.RETR_LIST)
            brCntsSet,_ = cv2.findContours(cv2.bitwise_not(brArea), cv2.RETR_EXTERNAL, cv2.RETR_LIST)

            tlCnts = tlCntsSet[FindMinIndex(tlCntsSet)]
            trCnts = trCntsSet[FindMinIndex(trCntsSet)]
            blCnts = blCntsSet[FindMinIndex(blCntsSet)]
            brCnts = brCntsSet[FindMinIndex(brCntsSet)]

            tlMinRect = cv2.minAreaRect(tlCnts)
            trMinRect = cv2.minAreaRect(trCnts)
            blMinRect = cv2.minAreaRect(blCnts)
            brMinRect = cv2.minAreaRect(brCnts)

            tlMinRectArea = tlMinRect[1][0]*tlMinRect[1][1]
            trMinRectArea = trMinRect[1][0]*trMinRect[1][1]
            blMinRectArea = blMinRect[1][0]*blMinRect[1][1]
            brMinRectArea = brMinRect[1][0]*brMinRect[1][1]
            proportion = [trBlackCount/trMinRectArea,tlBlackCount/tlMinRectArea,blBlackCount/blMinRectArea,brBlackCount/brMinRectArea]
            # proportion = [len(trCnts[0]),len(tlCnts[0]),len(blCnts[0]),len(brCnts[0])]

            print(proportion)
            print(Median(proportion))
            if(max(proportion) - Median(proportion) >  Median(proportion) - min(proportion)):
                answerPositon = proportion.index(max(proportion))
            else:
                answerPositon = proportion.index(min(proportion))


        print("Answer In "+ str(answerPositon+1))

        if(answerPositon == 0):
            pyautogui.moveTo(windowRegion[0] + startWidth + int(3*width/4), windowRegion[1]+startHeight + int(height/4))
            pyautogui.click(clicks=2)
        if(answerPositon == 1):
            pyautogui.moveTo(windowRegion[0] + startWidth + int(width/4), windowRegion[1]+startHeight + int(height/4))
            pyautogui.click(clicks=2)
        if(answerPositon == 2):
            pyautogui.moveTo(windowRegion[0] + startWidth + int(width/4), windowRegion[1]+startHeight + int(3*height/4))
            pyautogui.click(clicks=2)
        if(answerPositon == 3):
            pyautogui.moveTo(windowRegion[0] + startWidth + int(3*width/4), windowRegion[1]+startHeight + int(3*height/4))
            pyautogui.click(clicks=2)       

        CheckIsOutOfArea(windowRegion)

if __name__ == '__main__':
    main()
