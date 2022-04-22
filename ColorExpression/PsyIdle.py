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
        print(x1)
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
    imageContinuePath = "continue.png"
    windowRegion = GetWindowRegion()
    X = windowRegion[0]
    Y = windowRegion[1]
    print(F"X , Y = {X} , {Y} ")
    backgroundColor = (128, 128, 128)
    WHITE = (255, 255, 255)
    bias = 50
    colorCircleRadius = 0
    squareRadius = 20
    continueX, continueY = pyautogui.locateCenterOnScreen(
        imageContinuePath, region=windowRegion, confidence=0.9)
    hasSquareRadius = 0
    pyautogui.moveTo(continueX, continueY)
    pyautogui.click(clicks=2)
    while(windowRegion != None):
        time.sleep(0.5)
        continueLocation = pyautogui.locateCenterOnScreen(
            imageContinuePath, region=windowRegion, confidence=0.9)
        if(continueLocation != None):
            pyautogui.moveTo(continueLocation[0], continueLocation[1])
            pyautogui.click(clicks=2)
        WaitUntilShow(imageCrossPath, windowRegion,
                      confidence=0.9, timeoutThreshold=10)
        CheckIsOutOfArea(windowRegion)
        crossX = 0
        crossY = 0
        while(True):
            crossLocation = pyautogui.locateCenterOnScreen(
                imageCrossPath, region=windowRegion, confidence=0.9)
            if(crossLocation == None):
                continue
            crossX = crossLocation[0]
            crossY = crossLocation[1]
            pyautogui.moveTo(crossX, crossY+200)
            break
        print(f"Located cross...in ({crossX} ,{crossY} )")

        colors = [(), (), (), ()]
        while(True):

            if(pyautogui.pixel(int(crossX-squareRadius), int(crossY-squareRadius)) != backgroundColor):
                colors[0] = pyautogui.pixel(
                    int(crossX-squareRadius), int(crossY-squareRadius))
                pyautogui.moveTo(crossX-squareRadius,
                                 crossY-squareRadius)
                print(f"pyautogui.pixel = {colors[0]}")
            else:
                if(not hasSquareRadius):
                    squareRadius += 1
            if(pyautogui.pixel(int(crossX+squareRadius), int(crossY-squareRadius)) != backgroundColor):
                colors[1] = pyautogui.pixel(
                    int(crossX+squareRadius), int(crossY-squareRadius))
                pyautogui.moveTo(crossX+squareRadius,
                                 crossY-squareRadius)
                print(f"pyautogui.pixel = {colors[1]}")
            else:
                if(not hasSquareRadius):
                    squareRadius += 1
            if(pyautogui.pixel(int(crossX-squareRadius), int(crossY+squareRadius)) != backgroundColor):
                colors[2] = pyautogui.pixel(
                    int(crossX-squareRadius), int(crossY+squareRadius))
                pyautogui.moveTo(crossX-squareRadius,
                                 crossY+squareRadius)
                print(f"pyautogui.pixel = {colors[2]}")
            else:
                if(not hasSquareRadius):
                    squareRadius += 1
            if(pyautogui.pixel(int(crossX+squareRadius), int(crossY+squareRadius)) != backgroundColor):
                colors[3] = pyautogui.pixel(
                    int(crossX+squareRadius), int(crossY+squareRadius))
                pyautogui.moveTo(crossX+squareRadius,
                                 crossY+squareRadius)
                print(f"pyautogui.pixel = {colors[3]}")
            else:
                if(not hasSquareRadius):
                    squareRadius += 1
            if((colors[0] != backgroundColor) and (colors[0] != ()) and (colors[1] != backgroundColor) and (colors[1] != ()) and (colors[2] != backgroundColor) and (colors[2] != ()) and (colors[3] != backgroundColor) and (colors[3] != ())):
                print("Colors All Have Shown...")
                print(f"squareRadius = {squareRadius}")
                hasSquareRadius = True
                break

        while(True):
            c0 = pyautogui.pixel(int(crossX-squareRadius),
                                 int(crossY-squareRadius))
            c1 = pyautogui.pixel(int(crossX+squareRadius),
                                 int(crossY-squareRadius))
            c2 = pyautogui.pixel(int(crossX-squareRadius),
                                 int(crossY+squareRadius))
            c3 = pyautogui.pixel(int(crossX+squareRadius),
                                 int(crossY+squareRadius))
            if((colors[0] != backgroundColor) and (colors[1] != backgroundColor) and (colors[2] != backgroundColor) and (colors[3] != backgroundColor)):
                print(f"Searching WHITE...")
                while(True):
                    c0 = pyautogui.pixel(int(crossX-squareRadius),
                                         int(crossY-squareRadius))
                    c1 = pyautogui.pixel(int(crossX+squareRadius),
                                         int(crossY-squareRadius))
                    c2 = pyautogui.pixel(int(crossX-squareRadius),
                                         int(crossY+squareRadius))
                    c3 = pyautogui.pixel(int(crossX+squareRadius),
                                         int(crossY+squareRadius))
                    # print(c0,c1,c2,c3)
                    if((c0 == WHITE) and (c1 == WHITE) and (c2 == WHITE) and (c3 == WHITE)):
                        print("Starting Find Colors in ColorCircle...")
                        break
                break

        if(colorCircleRadius == 0):
            colorCircleRadius = squareRadius
            startX = 0
            endX = 0
            pyautogui.moveTo(crossX-squareRadius, crossY-squareRadius)
            pyautogui.click(clicks=2)
            while(True):
                if(pyautogui.pixel(int(crossX-colorCircleRadius), int(crossY)) == backgroundColor):
                    colorCircleRadius += 1
                    # print(pyautogui.pixel(int(crossX-colorCircleRadius), int(crossY)))
                else:
                    startX = colorCircleRadius
                    while(True):
                        # print(pyautogui.pixel(int(crossX-colorCircleRadius), int(crossY)))
                        if(pyautogui.pixel(int(crossX-colorCircleRadius), int(crossY)) != backgroundColor):
                            colorCircleRadius += 1
                        else:
                            endX = colorCircleRadius
                            break
                    break
            colorCircleRadius = int((startX+endX)/2)
            print(f"colorCircleRadius = {colorCircleRadius}")

# ===================================================================================
# One
        tic = time.perf_counter()
        pyautogui.moveTo(crossX-squareRadius, crossY-squareRadius)
        pyautogui.click(clicks=2)
        theta = random.randint(0, 31) / 10
        while(True):
            theta += 0.1
            time.sleep(0.02)
            checkX = int(crossX + colorCircleRadius*math.cos(theta))
            checkY = int(crossY + colorCircleRadius*math.sin(theta))
            if(pyautogui.pixelMatchesColor(checkX, checkY, colors[0], tolerance=30)):
                pyautogui.moveTo(checkX, checkY)
                pyautogui.dragRel(0, 200,
                                  duration=random.randint(5, 25) / 10)
                break
            else:
                showX = crossX + \
                    (squareRadius)*math.cos(theta)
                showY = crossY + \
                    (squareRadius)*math.cos(theta)
                # pyautogui.moveTo(showX, showY)
        toc = time.perf_counter()
        timeComsume = toc-tic
        print(f"Stage One for {timeComsume} second")

# ===================================================================================
# Two
        tic = time.perf_counter()
        pyautogui.moveTo(crossX+squareRadius, crossY-squareRadius)
        pyautogui.click(clicks=2)
        theta = random.randint(0, 31) / 10
        while(True):

            theta += 0.1
            time.sleep(0.02)
            checkX = int(crossX + colorCircleRadius*math.cos(theta))
            checkY = int(crossY + colorCircleRadius*math.sin(theta))
            if(pyautogui.pixelMatchesColor(checkX, checkY, colors[1], tolerance=30)):
                pyautogui.moveTo(checkX, checkY)
                pyautogui.dragRel(0, 200,
                                  duration=random.randint(5, 25) / 10)
                break
            else:
                showX = crossX + \
                    (squareRadius)*math.cos(theta)
                showY = crossY + \
                    (squareRadius)*math.cos(theta)
                # pyautogui.moveTo(showX, showY)
        toc = time.perf_counter()
        timeComsume = toc-tic
        print(f"Stage Two for {timeComsume} second")
# ===================================================================================
# Three
        tic = time.perf_counter()
        pyautogui.moveTo(crossX-squareRadius, crossY+squareRadius)
        pyautogui.click(clicks=2)
        theta = random.randint(0, 31) / 10
        while(True):

            theta += 0.1
            time.sleep(0.02)
            checkX = int(crossX + colorCircleRadius*math.cos(theta))
            checkY = int(crossY + colorCircleRadius*math.sin(theta))
            if(pyautogui.pixelMatchesColor(checkX, checkY, colors[2], tolerance=30)):
                pyautogui.moveTo(checkX, checkY)
                pyautogui.dragRel(0, 200,
                                  duration=random.randint(5, 25) / 10)
                break
            else:
                showX = crossX + \
                    (squareRadius)*math.cos(theta)
                showY = crossY + \
                    (squareRadius)*math.cos(theta)
                # pyautogui.moveTo(showX, showY)
        toc = time.perf_counter()
        timeComsume = toc-tic
        print(f"Stage Three for {timeComsume} second")

# ===================================================================================
# Four
        tic = time.perf_counter()
        pyautogui.moveTo(crossX+squareRadius, crossY+squareRadius)
        pyautogui.click(clicks=2)
        theta = random.randint(0, 31) / 10
        while(True):

            theta += 0.1
            time.sleep(0.02)
            checkX = int(crossX + colorCircleRadius*math.cos(theta))
            checkY = int(crossY + colorCircleRadius*math.sin(theta))
            if(pyautogui.pixelMatchesColor(checkX, checkY, colors[3], tolerance=30)):
                pyautogui.moveTo(checkX, checkY)
                pyautogui.dragRel(0, 200,
                                  duration=random.randint(5, 25) / 10)
                break
            else:
                showX = crossX + \
                    (squareRadius)*math.cos(theta)
                showY = crossY + \
                    (squareRadius)*math.cos(theta)
                # pyautogui.moveTo(showX, showY)
        toc = time.perf_counter()
        timeComsume = toc-tic
        print(f"Stage Four for {timeComsume} second")


if __name__ == '__main__':
    main()
