import pathlib
from os import path
from sys import setrecursionlimit
from datetime import date
from datetime import datetime
import csv
import shutil
from PIL import Image
from math import ceil
import random
import pandas as pd
import numpy as np

# Global variables:
BASEPATH = str(pathlib.Path(__file__).parent.resolve()) + '\\' # directory of the main.py
BASEDIRS = ('logs', 'backups\\images') # main directories used throughout the program
IMAGESPATH = 'backups\\images\\' # path to where the images inputted by the user are copied to
CONFIGFILE = '.\\config.properties' # config file
LOGCONFIG = '.\\logs_config.csv' # config file of the logging system: msgType, msgId, msgContent, addition
SUPPORTED = ('png', 'jpg', 'jpeg') # supported file extensions
MAXPIXELS = 8294400 # maximum amount of pixels supported, 8294400 is equal to 4k, 33177600 is equal to 8k
LOGFILE = 'logs\\logs_' # directory/name of a log file
CURRENTDATE = str(date.today().strftime('%Y_%m_%d')) # date at which the script is run
LOGTODAY = BASEPATH + LOGFILE + CURRENTDATE + '.txt' # defining today's log path
INITMESSAGE = 'Welcome to the program!\n'+'It is handle your input, divide the image into N (provided by the user) YxY path.\n' + 'Do not worry, just input any number and the program will tell you if the number is incorrect.\n' + 'Once the number is correct, the program will calculate each part\'s mean color.\n' + 'Then, N number of YxY blocks with random colors will be generated.\n' + 'At last they will be assigned to images\' parts to match the original image in the most accurate way.' 
BLOCKSBOUNDARY = 15
EXT = '.png' # deprecated
BLOCKSDIR = 'blocks'
BLOCKFILENAME = 'blocksData.csv'
IMAGEFILENAME = 'imageData.csv'
# Check what directories are present, needed and then create them
def checkDirs(base: str, dirs: list().__class__ == str):
    presentDirs = []
    # check what directories are present
    if base == BASEPATH:
        for x in pathlib.Path(base).rglob('*'): # check what directories are present within base recursively
            if x.is_dir():
                presentDirs.append(str(x)[len(BASEPATH):])
    neededDirs = []
    # check what directories are needed
    for x in dirs:
        if x in presentDirs:
            logMessage('presentDir', x)
        elif not x in presentDirs:
            neededDirs.append(x)
    #create necessary paths that are not present
    if neededDirs:
        createPaths(base, neededDirs)
    logMessage('dirsPresent', True)
    return True

# Check whether the file is supported
def fileChecker(file: str, imWidth: int, imHeight: int):
    fileMod = file.split('.')
    if len(fileMod) <= 1:
        logMessage('noFileExt', fileMod)
        printSupported()
        return False
    else:
        fileExt = file.split('.')[-1].lower()
        if fileExt in SUPPORTED and imWidth*imHeight <= MAXPIXELS:
            logMessage('correctFile', fileExt)
            return True
        elif fileExt in SUPPORTED and imWidth*imHeight > MAXPIXELS:
            logMessage('tooBigRes', file)
            printSupported()
            return False
        else:
            logMessage('wrongFileExt', fileExt)
            printSupported()
            return False

# Read message config from the LOGCONFIG based on msgId, then go to writeMessage
def logMessage(msgId: str, extras: str):
    #return True # not logging in messages into logs & terminal for the sake of small tests
    currentTime = str(datetime.now().strftime('%H_%M_%S_%f')[:-3])

    with open(LOGCONFIG, 'r') as singleRow:
        singleRow = csv.reader(singleRow) # read a single row
        for col in singleRow: # col[0] = msgType, col[1] = msgId, col[2] = msgContent, col[3] = extras(optional)
            if msgId == col[1]:
                if col[3] == '':
                    msg = f'{currentTime} [{col[0]}] {col[2]}\n'
                    writeMessage(msg, LOGTODAY)
                elif col[3] == 'extras':
                    msg = f'{currentTime} [{col[0]}] {col[2]} {extras}\n' 
                    writeMessage(msg, LOGTODAY)

# Print the message and log it into LOGTODAY
def writeMessage(msg: str, logPath: str):
    print(msg[13:len(msg) - 1]) # print msg without the date at the start and without a newline at the end
    #log msg into LOGTODAY
    if path.isfile(pathlib.Path(logPath)):
        ff = open(logPath, 'a')
        ff.write(msg)
        ff.close()
    elif not path.isfile(pathlib.Path(logPath)):
        ff = open(logPath, 'x')
        ff.write(msg)
        ff.close()

# Create paths
def createPaths(base: str, dirs: list or str):
    if type(dirs) == list:
        for x in dirs:
            pathlib.Path(base + x).mkdir(parents = True, exist_ok = True)
            logMessage('newDir', x)
    elif type(dirs) == str:
        pathlib.Path(base + dirs).mkdir(parents = True, exist_ok = True)
        logMessage('newDir', dirs)

# print a list of supported file extensions
def printSupported():
    print('\nSupported file extensions are: ', end='')
    for ext in SUPPORTED:
        print(ext, end='')
        if ext != SUPPORTED[-1]:
            print(',', end=' ')
    print(f'\nAnd the greatest number of pixels can be: {MAXPIXELS}, which is equal to 3840x2160 - 4k')

# return file name and delimiter the user used to enter a directory
def copyToDatePath(filePath: str):
    splitPath = filePath.split('\\') # split path on '\\', since all the directories are processed as with double backslashes
    delimPlace = len(str(splitPath[-1])) + 1
    file = filePath[len(filePath) - delimPlace + 1:]
    if filePath[-delimPlace] == '\\':
        delim = '\\'
        newDir = str(datetime.now().strftime('%Y%m%d_%H%M%S%f')[2:-4]) # define a directory, e.g. 211210_13241078
        image = Image.open(filePath)
        imWidth, imHeight = int(image.size[0]), int(image.size[1])
        image.close()
        logMessage('loadedFile', file)
        if fileChecker(splitPath[-1], imWidth, imHeight): # check whether the file extension is supported and the image resolutions are correct
            createPaths(BASEPATH + IMAGESPATH, newDir) # create new directory for the file
            datePath = BASEPATH + IMAGESPATH + newDir
            finalPath = datePath + delim + splitPath[-1]
            shutil.copyfile(filePath, finalPath)
            return finalPath, datePath
        else:
            exit()

# Handling user input
def fileInput():
    printSupported()
    print(INITMESSAGE)
    logMessage('waitInput', False)
    filePath = input('Please put in an absolute path to an image you would like to have replicated:\n')
    #filePath = 'C:\\Users\\longw\\Desktop\\G Drive\\Praca_inżynierska\\Engineering_Thesis\\test images\\Standard aspect ratio\\FHD\\4k-retro-80s-wallpaper-fhd-1920x1080.jpg'
    #filePath = 'C:/Users/longw/Desktop/G Drive/Praca_inżynierska/Engineering_Thesis/test images/Standard aspect ratio/FHD/4k-retro-80s-wallpaper-fhd-1920x1080.jpg'
    filePath = path.realpath(filePath) # change the provided delim to '\'
    finalPath, datePath = copyToDatePath(filePath)
    datePath = datePath + '\\'
    # next step, image processing
    #newImage = changeToPng(finalPath)
    return finalPath, datePath

#########################################   DEPRECATED (!!!!!!!!!!!!!!!!!!!!!!!!!)
# Saving the copy of a source file as PNG
def changeToPng(filePath: str):
    fileName = filePath.split('\\')[-1]
    image = Image.open(filePath) # https://www.developer.com/languages/displaying-and-converting-images-with-python/ <- about file extensions
    #image.show()
    finFile = filePath+EXT
    image.save(finFile) # saving the file as png format
    image.close()
    #print(image.close) # example: <bound method Image.close of <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=1920x1080 at 0x2AC4B3DE6D0>>
    if path.isfile(pathlib.Path(finFile)):
        logMessage('copiedOk', fileName+EXT)
        return finFile
    elif not path.isfile(pathlib.Path(finFile)):
        logMessage('copiedFalse', fileName+EXT)

def checkImage(myDivisor: int, imWidth: int, imHeight: int, toFind: str):
    blocksArea = (imWidth * imHeight) / myDivisor
    blocksSize = round(pow(blocksArea,0.5))
    blocksVertical, blocksHorizontal = imWidth / blocksSize, imHeight / blocksSize
    totalImages = ceil(blocksHorizontal) * ceil(blocksVertical)
    restVertical, restHorizontal = float('.' + str(blocksVertical).split('.')[-1]), float('.' + str(blocksHorizontal).split('.')[-1])
    myCondition = ((restHorizontal > 1 - BLOCKSBOUNDARY/100) and (restVertical > 1 - BLOCKSBOUNDARY/100))
    conditionSkipLastRowCol = ((restHorizontal < BLOCKSBOUNDARY/100) and (restVertical < BLOCKSBOUNDARY/100))
    if not toFind:
        if myCondition:
            return (True, myDivisor, totalImages, blocksSize, int(str(blocksHorizontal).split('.')[0]), restHorizontal, int(str(blocksVertical).split('.')[0]), restVertical), (False), (False)
        if conditionSkipLastRowCol:
            horizontal = int(str(blocksHorizontal).split('.')[0])
            vertical = int(str(blocksVertical).split('.')[0])
            return (True, myDivisor, horizontal * vertical, blocksSize, horizontal, restHorizontal, vertical, restVertical), (False), (False)
        else: 
            smallerBlock = checkImage(myDivisor-1, imWidth, imHeight, 'smaller')
            largerBlock = checkImage(myDivisor+1, imWidth, imHeight, 'larger')
            return (False, myDivisor, blocksSize, restVertical, restHorizontal), smallerBlock, largerBlock
        
    elif toFind == 'smaller':
        if myCondition or conditionSkipLastRowCol:
            return (True, myDivisor)
        elif myDivisor > 20: 
            return checkImage(myDivisor-1, imWidth, imHeight, 'smaller')
        else:
            return (False)
        
    elif toFind == 'larger':
        if myCondition or conditionSkipLastRowCol:
            return (True, myDivisor)
        elif (myDivisor < imHeight) or (myDivisor < imWidth):
            return checkImage(myDivisor+1, imWidth, imHeight, 'larger')
        else: 
            return (False)
        
def isTrue(myVar):
    if type(myVar) == tuple:
        if myVar[0] == True:
            return True
        elif myVar[0] == False:
            return False
    elif type(myVar) == bool:
        if myVar:
            return True
        elif not myVar:
            return False
        
# Cutting the image into smaller images
def ratioAnalyzer(filePath: str, datePath: str):
    image = Image.open(filePath)
    imWidth, imHeight = int(image.size[0]), int(image.size[1])
    image.close()
    while(True):
        myDivisor = 500
        logMessage('waitInput', False)
        myDivisor = int(input('Please provide a number of YxY areas you would like to divide your image into: '))
        ratioData, smaller, larger = checkImage(myDivisor, imWidth, imHeight, False)
        if ratioData[0] == True:
            logMessage('configBlocksArea', str(ratioData[1]))
            logMessage('configBlocksNumber', str(ratioData[2]))
            logMessage('configBlocksPixels', str(ratioData[3]))
            logMessage('configBlocksWidthRest', str(ratioData[5]))
            logMessage('configBlocksHeightRest', str(ratioData[7]))
            ratioData = ratioData[1:]
            imageData = imageCutting(filePath, ratioData)
            saveAsCsv(IMAGEFILENAME, datePath, imageData)
            return imageData, ratioData
        elif ratioData[0] == False:
            logMessage('incorrectNumberBlocks', str(ratioData[1]))
            if isTrue(smaller):
                print('Closest smaller correct number of parts is: ' + str(smaller[1]))
            if isTrue(larger):
                print('Closest larger correct number of parts is: ' + str(larger[1]))

def generateBlocks(datePath: str, amount: int, size: int):
    createPaths(datePath, BLOCKSDIR)
    blocksPath = datePath + BLOCKSDIR + '\\'
    blocksData = []
    old_percentage = 0
    
    # generate {amount} amount of images to the /blocks children directory within the /backups/images/[date]/ directory
    for singleImage in range(1, amount+1):
        percentage = round((singleImage / amount) * 100, 0)
        blockPath = blocksPath + str(singleImage) + '.png'
        redAmnt = random.randrange(0,255,1)
        greenAmnt = random.randrange(0,255,1)
        blueAmnt = random.randrange(0,255,1)
        blockData = (redAmnt, greenAmnt, blueAmnt)
        img = Image.new('RGB', (size, size), blockData)
        img.save(blockPath)
        img.close
        blockData = redAmnt, greenAmnt, blueAmnt, blockPath
        blocksData.append(blockData)
        
        # print the progress of image generation
        if percentage > old_percentage:
            old_percentage = percentage
            percentage = str(percentage).split('.')[0]
            print(f'{percentage}% of images generated...')
    logMessage('blocksGenerated', False)
    saveAsCsv(BLOCKFILENAME, datePath, blocksData)
    return(blocksData)

def imageCutting(filePath: str, ratioData: tuple):
    image = Image.open(filePath)
    pix = image.load()
    imageData = []
    lastCol = round(ratioData[6] * ratioData[2])
    lastRow = round(ratioData[4] * ratioData[2])
    #print(ratioData) # e.g.: (28, 32, 272, 3, 0.9705882352941178, 7, 0.0588235294117645)
    for myRow in range(0, ratioData[3] + 1):
        for myCol in range(0, ratioData[5] + 1):
            red = 0
            blue = 0
            green = 0
            if (myRow != ratioData[3] and myCol != ratioData[5]):
                for y in range(myRow * ratioData[2], (myRow + 1) * ratioData[2]):
                    for x in range(myCol * ratioData[2], (myCol + 1) * ratioData[2]):
                        color = pix[x, y]
                        red = red + color[0]
                        green = green + color[1]
                        blue = blue + color[2]
                partMean = (myRow, myCol, round(red/pow(ratioData[2], 2)), round(green/pow(ratioData[2], 2)), round(blue/pow(ratioData[2], 2)))
                imageData.append(partMean)
            if myCol == ratioData[5] and myRow != ratioData[3]:
                    for y in range(myRow * ratioData[2], (myRow + 1) * ratioData[2]):
                        for x in range(myCol * ratioData[2], myCol * ratioData[2] + lastCol):
                            color = pix[x, y]
                            red = red + color[0]
                            green = green + color[1]
                            blue = blue + color[2]
                    partMean = (myRow, myCol, round(red/pow(ratioData[2], 2)), round(green/pow(ratioData[2], 2)), round(blue/pow(ratioData[2], 2)))
                    imageData.append(partMean)
            elif myCol != ratioData[5] and myRow == ratioData[3]:
                    for y in range(myRow * ratioData[2], myRow * ratioData[2] + lastRow):
                        for x in range(myCol * ratioData[2], (myCol + 1) * ratioData[2]):
                            color = pix[x, y]
                            red = red + color[0]
                            green = green + color[1]
                            blue = blue + color[2]
                    partMean = (myRow, myCol, round(red/pow(ratioData[2], 2)), round(green/pow(ratioData[2], 2)), round(blue/pow(ratioData[2], 2)))
                    imageData.append(partMean)
            elif myCol == ratioData[5] and myRow == ratioData[3]:
                    for y in range(myRow * ratioData[2], myRow * ratioData[2] + lastRow):
                        for x in range(myCol * ratioData[2], myCol * ratioData[2] + lastCol):
                            color = pix[x, y]
                            red = red + color[0]
                            green = green + color[1]
                            blue = blue + color[2]
                    partMean = (myRow, myCol, round(red/pow(ratioData[2], 2)), round(green/pow(ratioData[2], 2)), round(blue/pow(ratioData[2], 2)))
                    imageData.append(partMean)
    if imageData:
        return imageData
            
def saveAsCsv(name: str, filePath: str, data: list or tuple):
    with open(filePath + name, 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)

# to find the correct block, we will need to calculate the three-dimensional Euclidean distance
# the mathematical formula for that would be: pow((x2-x1)**2+(y2-y1)**2+(z2-z1)**2, 0.5)  
def euclidian_distance_vector_single_block(block: tuple, images: pd.DataFrame):
    largeDistanceListWithIndexes = []
    largeDistanceList = []
    y = []
    for index in range(0, images.index[-1]+1):
        x = (((images['R_images'][index]-block[0])**2 + (images['G_images'][index]-block[1])**2 + (images['B_images'][index]-block[2])**2)**0.5)
        y.append(x)
        y.append(index)
        largeDistanceListWithIndexes.append(y)
        largeDistanceList.append(x)
        y = []
    return largeDistanceListWithIndexes, largeDistanceList

# find the closest number within array which is the closest to the mean
def find_closest(array, mean: float):
    newArray = []
    for n in range(0, len(array)-1):
        if len(array[n]) == 2:
            newArray.append(array[n][0])
        else:
            newArray.append(-1)
    array2 = np.asarray(newArray)
    idx = (np.abs(array2 - mean)).argmin()
    return array[idx]
# remove an element from a list
def removeElement(distanceList: list, index: int):
    for n in range(0, len(distanceList)):
        newList = distanceList[n]
        newList[index].pop(0)
        newList[index].pop(0)
        distanceList[n] = newList
    return distanceList

def comparingImagesAndBlocks():
    trainPath = BASEPATH + IMAGESPATH
    #print(trainPath) # C:\Users\longw\Desktop\G Drive\Praca_inżynierska\Engineering_Thesis\backups\images\
        
    # find the newest directory within backups/images/
    withinImages= pathlib.Path(trainPath).glob('*')
    dataPaths = [file for file in withinImages if file.is_dir()]
    newestDir = str(dataPaths[-1]) + '\\'
    #print(newestDir) # C:\Users\longw\Desktop\G Drive\Praca_inżynierska\Engineering_Thesis\backups\images\220117_21214749\

    dfImages = pd.read_csv(newestDir + IMAGEFILENAME, index_col=None, header=None, names=['image row', 'image col', 'R_images','G_images','B_images'])
    dfBlocks = pd.read_csv(newestDir + BLOCKFILENAME, index_col=None, header=None, names=['R_blocks','G_blocks','B_blocks', 'Path'])

    # new dataframe columns, the element will be changed once the block is assigned to the part of an image
    dfBlocks['assigned row'] = 0 
    dfBlocks['assigned col'] = 0

    # deleting unnecessary data if the image's edges were rounded
    dfImages = dfImages[0:len(dfBlocks)]
    singleBlockDistanceWithIndexes = []
    singleBlockDistance = []
    for n in range(0, dfBlocks.index[-1]+1):
        x, y = euclidian_distance_vector_single_block((dfBlocks['R_blocks'][n], dfBlocks['G_blocks'][n], dfBlocks['B_blocks'][n]), dfImages)
        singleBlockDistanceWithIndexes.append(x)
        singleBlockDistance.append(y)
    meanBlockDistance = []
    for n in range(0, dfBlocks.index[-1]+1):
        x = np.mean(singleBlockDistance[n])
        meanBlockDistance.append(x)
    closestBlocks = []
    for n in range(0, dfBlocks.index[-1]):
        x = find_closest(singleBlockDistanceWithIndexes[n], meanBlockDistance[n])
        y = [x[0], x[1], n]
        if n != dfBlocks.index[-1]-1:
            closestBlocks.append(y)
        singleBlockDistanceWithIndexes = removeElement(singleBlockDistanceWithIndexes, x[1])
        
    for n in singleBlockDistanceWithIndexes[dfBlocks.index[-1]]:
        if n:
            closestBlocks.append([n[0], n[1], dfBlocks.index[-1]])
    #print(closestBlocks)
    for n in closestBlocks:
        dfBlocks['assigned row'][n[2]] = dfImages['image row'][n[1]]
        dfBlocks['assigned col'][n[2]] = dfImages['image col'][n[1]]
    dfBlocksColumns = dfBlocks.columns.tolist()
    dfBlocksColumns = dfBlocksColumns[0:3] + dfBlocksColumns[4:] + dfBlocksColumns[3:4]
    dfBlocks = dfBlocks[dfBlocksColumns]
    dfBlocks.to_csv(newestDir + 'blocksAssignedToImages.csv', index=False)
    
def main():
    if checkDirs(BASEPATH, BASEDIRS): # initial check for directories # commented as it's working properly
        myFile, datePath = fileInput()
        setrecursionlimit(10000) # increase only if met with "RecursionError: maximum recursion depth exceeded while calling a Python object"
        ratioData = ratioAnalyzer(myFile, datePath)
        generateBlocks(datePath, ratioData[1], ratioData[2])
        comparingImagesAndBlocks()
        
if __name__ == '__main__':
    main()