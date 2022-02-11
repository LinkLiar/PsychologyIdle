from turtle import color
import pyautogui
import cv2
import random
import win32api
import win32con
import win32gui
import time
import numpy
import math
labelName = "SDL_app"
titleName = "SM-G9910"


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


# topLeftX, topLeftY, bottomRightX, bottomRightY = win32gui.GetWindowRect(328656)

# targetX = 1
# targetY = 1

# random.randint(5, 40)
# pyautogui.moveTo(targetX, targetY, duration=random.randint(5, 40)/10)
# pyautogui.leftClick(x=targetX, y=targetY)
# pyautogui.PAUSE = 2.5  # second
# pyautogui.position()  # 当前鼠标的坐标


def main():
    imageCrossPath = "cross.png"
    imageContinuePath = "continue.png"
    windowRegion = GetWindowRegion()
    X = windowRegion[0]
    Y = windowRegion[1]
    print(F"X , Y = {X} , {Y} ")
    backgroundColor = (128, 128, 128)
    WHITE = (255, 255, 255)

    continueX, continueY = pyautogui.locateCenterOnScreen(
        imageContinuePath, region=windowRegion, confidence=0.9)
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
        time.sleep(0.4)#random.randint(2, 5)/10
        continueLocation = pyautogui.locateCenterOnScreen(imageContinuePath, region=windowRegion, confidence=0.9)
        if(continueLocation != None):
                pyautogui.moveTo(continueLocation[0], continueLocation[1])
                pyautogui.click(clicks=2)
        image = Screenshot(squareRegion,convertTo="OpenCV")
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        _, imageBinary = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU) 

        height = image.shape[0]
        width = image.shape[1]

        tlArea = imageBinary[0:int(height/4),0:int(width/4)]
        trArea = imageBinary[0:int(height/4),int(width/2):int(3*width/4)]
        blArea = imageBinary[int(height/2):int(3*height/4),0:int(width/4)]
        brArea = imageBinary[int(height/2):int(3*height/4),int(width/2):int(3*width/4)]

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

        hist = []
        hist.append(trBlackCount)
        hist.append(tlBlackCount)
        hist.append(blBlackCount)
        hist.append(brBlackCount)
        
        answerPositon = -1
        for number in range(0,4):
            if(number != hist.index(max(hist)) and number !=hist.index(min(hist))):
                if(max(hist) - hist[number] >  hist[number]-min(hist)):
                    answerPositon = hist.index(max(hist))
                else:
                    answerPositon = hist.index(min(hist))

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













#     bias = 50
#     colorCircleRadius = 0
#     squareRadius = 20
#     continueX, continueY = pyautogui.locateCenterOnScreen(
#         imageContinuePath, region=windowRegion, confidence=0.9)
#     hasSquareRadius = 0
#     pyautogui.moveTo(continueX, continueY)
#     pyautogui.click(clicks=2)
#     while(windowRegion != None):
#         time.sleep(0.5)
#         continueLocation = pyautogui.locateCenterOnScreen(imageContinuePath, region=windowRegion, confidence=0.9)
#         if(continueLocation!=None):
#                 pyautogui.moveTo(continueLocation[0], continueLocation[1])
#                 pyautogui.click(clicks=2)
#         WaitUntilShow(imageCrossPath, windowRegion,
#                       confidence=0.9, timeoutThreshold=10)
#         CheckIsOutOfArea(windowRegion)
#         crossX = 0
#         crossY = 0
#         while(True):
#             crossLocation = pyautogui.locateCenterOnScreen(
#                 imageCrossPath, region=windowRegion, confidence=0.9)
#             if(crossLocation==None):
#                 continue
#             crossX = crossLocation[0]
#             crossY = crossLocation[1]
#             pyautogui.moveTo(crossX, crossY+200)
#             break
#         print(f"Located cross...in ({crossX} ,{crossY} )")
#         # crossLocation = pyautogui.locateAllOnScreen(imagePath,region=windowRegion,confidence=0.9)
#         # crossX ,crossY =pyautogui.center(crossLocation)

#         colors = [(), (), (), ()]
#         while(True):
            
#             if(pyautogui.pixel(int(crossX-squareRadius), int(crossY-squareRadius)) != backgroundColor):
#                 colors[0] = pyautogui.pixel(
#                     int(crossX-squareRadius), int(crossY-squareRadius))
#                 pyautogui.moveTo(crossX-squareRadius,
#                                  crossY-squareRadius)
#                 print(f"pyautogui.pixel = {colors[0]}")   
#             else:
#                 if(not hasSquareRadius):
#                     squareRadius += 1
#             if(pyautogui.pixel(int(crossX+squareRadius), int(crossY-squareRadius)) != backgroundColor):
#                 colors[1] = pyautogui.pixel(
#                     int(crossX+squareRadius), int(crossY-squareRadius))
#                 pyautogui.moveTo(crossX+squareRadius,
#                                  crossY-squareRadius)
#                 print(f"pyautogui.pixel = {colors[1]}")
#             else:
#                 if(not hasSquareRadius):
#                     squareRadius += 1
#             if(pyautogui.pixel(int(crossX-squareRadius), int(crossY+squareRadius)) != backgroundColor):
#                 colors[2] = pyautogui.pixel(
#                     int(crossX-squareRadius), int(crossY+squareRadius))
#                 pyautogui.moveTo(crossX-squareRadius,
#                                  crossY+squareRadius)
#                 print(f"pyautogui.pixel = {colors[2]}")           
#             else:
#                 if(not hasSquareRadius):
#                     squareRadius += 1
#             if(pyautogui.pixel(int(crossX+squareRadius), int(crossY+squareRadius)) != backgroundColor):
#                 colors[3] = pyautogui.pixel(
#                     int(crossX+squareRadius), int(crossY+squareRadius))
#                 pyautogui.moveTo(crossX+squareRadius,
#                                  crossY+squareRadius)
#                 print(f"pyautogui.pixel = {colors[3]}")              
#             else:
#                 if(not hasSquareRadius):
#                     squareRadius += 1
#             if((colors[0] != backgroundColor)and (colors[0] != ()) and (colors[1] != backgroundColor) and(colors[1] != ()) and (colors[2] != backgroundColor) and(colors[2] != ()) and (colors[3] != backgroundColor)and (colors[3] != ()) ):
#                 print("Colors All Have Shown...")
#                 print(f"squareRadius = {squareRadius}")
#                 hasSquareRadius = True
#                 break

#         while(True):
#             c0 = pyautogui.pixel(int(crossX-squareRadius),
#                                  int(crossY-squareRadius))
#             c1 = pyautogui.pixel(int(crossX+squareRadius),
#                                  int(crossY-squareRadius))
#             c2 = pyautogui.pixel(int(crossX-squareRadius),
#                                  int(crossY+squareRadius))
#             c3 = pyautogui.pixel(int(crossX+squareRadius),
#                                  int(crossY+squareRadius))
#             if((colors[0] != backgroundColor) and (colors[1] != backgroundColor) and (colors[2] != backgroundColor) and (colors[3] != backgroundColor)):
#                 print(f"Searching WHITE...")
#                 while(True):
#                     c0 = pyautogui.pixel(int(crossX-squareRadius),
#                                          int(crossY-squareRadius))
#                     c1 = pyautogui.pixel(int(crossX+squareRadius),
#                                          int(crossY-squareRadius))
#                     c2 = pyautogui.pixel(int(crossX-squareRadius),
#                                          int(crossY+squareRadius))
#                     c3 = pyautogui.pixel(int(crossX+squareRadius),
#                                          int(crossY+squareRadius))
#                     # print(c0,c1,c2,c3)
#                     if((c0 == WHITE) and (c1 == WHITE) and (c2 == WHITE) and (c3 == WHITE)):
#                         print("Starting Find Colors in ColorCircle...")
#                         break
#                 break

#         if(colorCircleRadius == 0):
#             colorCircleRadius = squareRadius
#             startX = 0
#             endX = 0
#             pyautogui.moveTo(crossX-squareRadius, crossY-squareRadius)
#             pyautogui.click(clicks=2)
#             while(True):
#                 if(pyautogui.pixel(int(crossX-colorCircleRadius), int(crossY)) == backgroundColor):
#                     colorCircleRadius += 1
#                     # print(pyautogui.pixel(int(crossX-colorCircleRadius), int(crossY)))
#                 else:
#                     startX = colorCircleRadius
#                     while(True):
#                         # print(pyautogui.pixel(int(crossX-colorCircleRadius), int(crossY)))
#                         if(pyautogui.pixel(int(crossX-colorCircleRadius), int(crossY)) != backgroundColor):
#                             colorCircleRadius += 1
#                         else:
#                             endX = colorCircleRadius
#                             break
#                     break
#             colorCircleRadius = int((startX+endX)/2)
#             print(f"colorCircleRadius = {colorCircleRadius}")

# # ===================================================================================
# # One
#         tic = time.perf_counter()
#         pyautogui.moveTo(crossX-squareRadius, crossY-squareRadius)
#         pyautogui.click(clicks=2)
#         theta = random.randint(0, 31) / 10
#         while(True):
#             theta += 0.1
#             time.sleep(0.02)
#             checkX = int(crossX + colorCircleRadius*math.cos(theta))
#             checkY = int(crossY + colorCircleRadius*math.sin(theta))
#             if(pyautogui.pixelMatchesColor(checkX, checkY, colors[0], tolerance=30)):
#                 pyautogui.moveTo(checkX, checkY)
#                 pyautogui.dragRel(0, 200,
#                                   duration=random.randint(5, 25) / 10)
#                 break
#             else:
#                 showX = crossX + \
#                     (squareRadius)*math.cos(theta)
#                 showY = crossY + \
#                     (squareRadius)*math.cos(theta)
#                 # pyautogui.moveTo(showX, showY)
#         toc = time.perf_counter()
#         timeComsume = toc-tic
#         print(f"Stage One for {timeComsume} second")

# # ===================================================================================
# # Two
#         tic = time.perf_counter()
#         pyautogui.moveTo(crossX+squareRadius, crossY-squareRadius)
#         pyautogui.click(clicks=2)
#         theta = random.randint(0, 31) / 10
#         while(True):

#             theta += 0.1
#             time.sleep(0.02)
#             checkX = int(crossX + colorCircleRadius*math.cos(theta))
#             checkY = int(crossY + colorCircleRadius*math.sin(theta))
#             if(pyautogui.pixelMatchesColor(checkX, checkY, colors[1], tolerance=30)):
#                 pyautogui.moveTo(checkX, checkY)
#                 pyautogui.dragRel(0, 200,
#                                   duration=random.randint(5, 25) / 10)
#                 break
#             else:
#                 showX = crossX + \
#                     (squareRadius)*math.cos(theta)
#                 showY = crossY + \
#                     (squareRadius)*math.cos(theta)
#                 # pyautogui.moveTo(showX, showY)
#         toc = time.perf_counter()
#         timeComsume = toc-tic
#         print(f"Stage Two for {timeComsume} second")
# # ===================================================================================
# # Three
#         tic = time.perf_counter()
#         pyautogui.moveTo(crossX-squareRadius, crossY+squareRadius)
#         pyautogui.click(clicks=2)
#         theta = random.randint(0, 31) / 10
#         while(True):

#             theta += 0.1
#             time.sleep(0.02)
#             checkX = int(crossX + colorCircleRadius*math.cos(theta))
#             checkY = int(crossY + colorCircleRadius*math.sin(theta))
#             if(pyautogui.pixelMatchesColor(checkX, checkY, colors[2], tolerance=30)):
#                 pyautogui.moveTo(checkX, checkY)
#                 pyautogui.dragRel(0, 200,
#                                   duration=random.randint(5, 25) / 10)
#                 break
#             else:
#                 showX = crossX + \
#                     (squareRadius)*math.cos(theta)
#                 showY = crossY + \
#                     (squareRadius)*math.cos(theta)
#                 # pyautogui.moveTo(showX, showY)
#         toc = time.perf_counter()
#         timeComsume = toc-tic
#         print(f"Stage Three for {timeComsume} second")

# # ===================================================================================
# # Four
#         tic = time.perf_counter()
#         pyautogui.moveTo(crossX+squareRadius, crossY+squareRadius)
#         pyautogui.click(clicks=2)
#         theta = random.randint(0, 31) / 10
#         while(True):

#             theta += 0.1
#             time.sleep(0.02)
#             checkX = int(crossX + colorCircleRadius*math.cos(theta))
#             checkY = int(crossY + colorCircleRadius*math.sin(theta))
#             if(pyautogui.pixelMatchesColor(checkX, checkY, colors[3], tolerance=30)):
#                 pyautogui.moveTo(checkX, checkY)
#                 pyautogui.dragRel(0, 200,
#                                   duration=random.randint(5, 25) / 10)
#                 break
#             else:
#                 showX = crossX + \
#                     (squareRadius)*math.cos(theta)
#                 showY = crossY + \
#                     (squareRadius)*math.cos(theta)
#                 # pyautogui.moveTo(showX, showY)
#         toc = time.perf_counter()
#         timeComsume = toc-tic
#         print(f"Stage Four for {timeComsume} second")


if __name__ == '__main__':
    main()
