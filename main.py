import pathlib
from os import path
from sys import setrecursionlimit
from datetime import date
from datetime import datetime
from csv import reader
import shutil
from PIL import Image
from math import ceil
import random
import _thread

# Global variables:
BASEPATH = str(pathlib.Path(__file__).parent.resolve()) + '\\' # directory of the main.py
BASEDIRS = ('logs', 'backups\\images') # main directories used throughout the program
IMAGESPATH = 'backups\\images\\' # path to where the images inputted by the user are copied to
CONFIGFILE = '.\\config.properties' # config file
LOGCONFIG = '.\\logs_config.csv' # config file of the logging system: msgType, msgId, msgContent, addition
SUPPORTED = ('png', 'jpg', 'jpeg') # supported file extensions
MAXPIXELS = 33177600 # maximum amount of pixels supported, 33177600 is equal to 8k
LOGFILE = 'logs/logs_' # directory/name of a log file
CURRENTDATE = str(date.today().strftime('%Y_%m_%d')) # date at which the script is run
LOGTODAY = BASEPATH + LOGFILE + CURRENTDATE + '.txt' # defining today's log path
INITMESSAGE = 'Welcome to the program!'
MAXBLOCKS, STANDBLOCKS, MINBLOCKS = 100, 60, 20 # maximum/minimum amount of Randomly Rendered Blocks(RRB) possible to generate
BLOCKSBOUND = 15
EXT = '.png' # deprecated
BLOCKSDIR = 'blocks'

# Check what directories are present, needed and then create them with createPaths()
def checkDirs(base, dirs):
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
            logMessage('presentDir', base, x)
        elif not x in presentDirs:
            neededDirs.append(x)
    #create necessary paths that are not present
    if neededDirs:
        createPaths(base, neededDirs)
    logMessage('dirsPresent', base, True)

# Check whether the file is supported
def fileChecker(file: str, imWidth: int, imHeight: int):
    fileMod = file.split('.')
    if len(fileMod) <= 1:
        logMessage('noFileExt', file, fileMod)
        printSupported()
        return False
    else:
        fileExt = file.split('.')[-1].lower()
        if fileExt in SUPPORTED and imWidth*imHeight <= MAXPIXELS:
            logMessage('correctFile', False, fileExt)
            return True
        elif fileExt in SUPPORTED and imWidth*imHeight > MAXPIXELS:
            logMessage('tooBigRes', False, file)
            printSupported()
            return False
        else:
            logMessage('wrongFileExt', False, fileExt)
            printSupported()
            return False

# Read message config from the LOGCONFIG based on msgId, then go to writeMessage
def logMessage(msgId, directory, extras):
    #return True # not logging in messages into logs & terminal for the sake of small tests
    currentTime = str(datetime.now().strftime('%H_%M_%S_%f')[:-3])

    with open(LOGCONFIG, 'r') as singleRow:
        singleRow = reader(singleRow) # read a single row
        for col in singleRow: # col[0] = msgType, col[1] = msgId, col[2] = msgContent, col[3] = extras(optional)
            if msgId == col[1]:
                if col[3] == '':
                    msg = f'{currentTime} [{col[0]}] {col[2]}\n'
                    writeMessage(msg, LOGTODAY)
                elif col[3] == 'extras':
                    msg = f'{currentTime} [{col[0]}] {col[2]} {extras}\n' 
                    writeMessage(msg, LOGTODAY)

# Print the message and log it into LOGTODAY
def writeMessage(msg, logPath):
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
def createPaths(base, dirs):
    if type(dirs) == list:
        for x in dirs:
            pathlib.Path(base + x).mkdir(parents = True, exist_ok = True)
            logMessage('newDir', base, x)
    elif type(dirs) == str:
        pathlib.Path(base + dirs).mkdir(parents = True, exist_ok = True)
        logMessage('newDir', base, dirs)

# print a list of supported file extensions
def printSupported():
    print('\nSupported file extensions are: ', end='')
    for ext in SUPPORTED:
        print(ext, end='')
        if ext != SUPPORTED[-1]:
            print(',', end=' ')
    print(f'\nAnd the greatest number of pixels can be: {MAXPIXELS}, which is equal to 7680×4320 - 8k')

# return file name and delimiter the user used to enter a directory
def copyToDatePath(filePath):
    splitPath = filePath.split('\\') # split path on '\\', since all the directories are processed as with double backslashes
    delimPlace = len(str(splitPath[-1])) + 1
    file = filePath[len(filePath) - delimPlace + 1:]
    if filePath[-delimPlace] == '\\':
        delim = '\\'
        newDir = str(datetime.now().strftime('%Y%m%d_%H%M%S%f')[2:-4]) # define a directory, e.g. 211210_13241078
        image = Image.open(filePath)
        imWidth, imHeight = int(image.size[0]), int(image.size[1])
        image.close()
        logMessage('loadedFile', BASEPATH, file)
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
    #print(INITMESSAGE)
    logMessage('waitInput', False, False)
    #filePath = input('Please put in an absolute path to an image you would like to have replicated:\n')
    #filePath = 'C:\\Users\\longw\\Desktop\\G Drive\\Praca inżynierska\\Engineering_Thesis\\test images\\Standard aspect ratio\\FHD\\4k-retro-80s-wallpaper-fhd-1920x1080.jpg'
    filePath = 'C:/Users/longw/Desktop/G Drive/Praca inżynierska/Engineering_Thesis/test images/Standard aspect ratio/FHD/4k-retro-80s-wallpaper-fhd-1920x1080.jpg'
    filePath = path.realpath(filePath) # change the provided delim to '\'
    finalPath, datePath = copyToDatePath(filePath)
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
        logMessage('copiedOk', False, fileName+EXT)
        return finFile
    elif not path.isfile(pathlib.Path(finFile)):
        logMessage('copiedFalse', False, fileName+EXT)

def checkImage(myDivisor: int, imWidth: int, imHeight: int, toFind: str):
    blocksArea = (imWidth * imHeight) / myDivisor
    blocksSize = round(pow(blocksArea,0.5))
    blocksVertical, blocksHorizontal = imWidth / blocksSize, imHeight / blocksSize
    totalImages = ceil(blocksHorizontal) * ceil(blocksVertical)
    restVertical, restHorizontal = float('.' + str(blocksVertical).split('.')[-1]), float('.' + str(blocksHorizontal).split('.')[-1])
    myCondition = (restHorizontal < BLOCKSBOUND/100 or restHorizontal > 1 - BLOCKSBOUND/100) and (restVertical < BLOCKSBOUND/100 or restVertical > 1 - BLOCKSBOUND/100)
    if not toFind:
        if myCondition:
            #print(blocksVertical, blocksHorizontal)
            return (True, myDivisor, totalImages, blocksSize, int(str(blocksHorizontal).split('.')[0]), restHorizontal, int(str(blocksVertical).split('.')[0]), restVertical), (False), (False)
        else: 
            #print(blocksVertical, blocksHorizontal)
            smallerBlock = checkImage(myDivisor-1, imWidth, imHeight, 'smaller')
            largerBlock = checkImage(myDivisor+1, imWidth, imHeight, 'larger')
            return (False, myDivisor, blocksSize, restVertical, restHorizontal), smallerBlock, largerBlock
        
    elif toFind == 'smaller':
        if myCondition:
            return (True, myDivisor)
        elif myDivisor > 20: 
            return checkImage(myDivisor-1, imWidth, imHeight, 'smaller')
        else:
            #print('Couldn\'t find smaller number of images that would be suitable')
            return (False)
        
    elif toFind == 'larger':
        if myCondition:
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
def ratioAnalyzer(filePath: str):
    image = Image.open(filePath)
    imWidth, imHeight = int(image.size[0]), int(image.size[1])
    image.close()
    while(True):
        myDivisor = 500
        logMessage('waitInput', False, False)
        myDivisor = int(input('Please provide a number of YxY areas you would like to divide your image into: '))
        ratioData, smaller, larger = checkImage(myDivisor, imWidth, imHeight, False)
        if ratioData[0] == True:
            logMessage('configBlocksArea', False, str(ratioData[1]))
            logMessage('configBlocksNumber', False, str(ratioData[2]))
            logMessage('configBlocksPixels', False, str(ratioData[3]))
            logMessage('configBlocksWidthRest', False, str(ratioData[5]))
            logMessage('configBlocksHeightRest', False, str(ratioData[7]))
            ratioData = ratioData[1:]
            imageData = imageCutting(filePath, ratioData)
            return imageData, ratioData
        elif ratioData[0] == False:
            logMessage('incorrectNumberBlocks', False, str(ratioData[1]))
            if isTrue(smaller):
                print('Closest smaller correct number of parts is: ' + str(smaller[1]))
            if isTrue(larger):
                print('Closest larger correct number of parts is: ' + str(larger[1]))

def generateBlocks(datePath: str, amount: int, size: int):
    datePath = datePath + '\\'
    createPaths(datePath, BLOCKSDIR)
    blocksPath = datePath + BLOCKSDIR + '\\'
    blocksData = []
    old_percentage = 0
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
        if percentage > old_percentage:
            old_percentage = percentage
            percentage = str(percentage).split('.')[0]
            #print(f'{percentage}% of images generated...')
    logMessage('blocksGenerated', False, False)
    return(blocksData)

def imageCutting(filePath: str, ratioData: tuple):
    image = Image.open(filePath)
    pix = image.load()
    imageData = []
    i = 0
    #print(ratioData) # e.g.: (28, 32, 272, 3, 0.9705882352941178, 7, 0.0588235294117645)
    for partRow in range(0,ratioData[]):
        for partCol in range(0,ratioData[]):
            for row in (partRow * ratioData[2], (partCol) * ratioData[2]):
                for col in range(part * ratioData[2], ratioData[2]):
                    print(i)
                    i = i + 1

if __name__ == '__main__':
    checkDirs(BASEPATH, BASEDIRS) # initial check for directories # commented as it's working properly
    myFile, datePath = fileInput()
    setrecursionlimit(10000) # increase only if met with "RecursionError: maximum recursion depth exceeded while calling a Python object"
    imageData, ratioData = ratioAnalyzer(myFile)
    blocksData = generateBlocks(datePath, ratioData[1], ratioData[2])
    