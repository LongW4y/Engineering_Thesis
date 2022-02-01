from pathlib import Path
from os import path
from pickle import FALSE
from sys import setrecursionlimit
from datetime import date, datetime
from csv import reader, writer
from shutil import copyfile
from PIL import Image
from math import ceil
from random import randrange
import pandas as pd
import numpy as np
import cv2

#############################################################################################################################

# Global variables:
# directory of the main.py
BASEPATH = str(Path(__file__).parent.resolve()) + '\\' 
# main directories used throughout the program
BASEDIRS = ('logs', 'images') 
# path to where the images inputted by the user are copied to
IMAGESPATH = BASEDIRS[1] + '\\' 
# config file of the logging system: msgType, msgId, msgContent, addition
LOGCONFIG = '.\\logs_config.csv' 
# supported file extensions
SUPPORTED = ('png', 'jpg', 'jpeg') 
# directory\name of a log file
LOGFILE = f'{BASEDIRS[0]}\\logs_' 
# date at which the script is run
CURRENTDATE = str(date.today().strftime('%Y_%m_%d')) 
# defining today's log path
LOGTODAY = BASEPATH + LOGFILE + CURRENTDATE + '.log' 
# first message shown to the user introducing to the program
INITMESSAGE = 'Welcome to the program!\n' + 'What it does?\n' + 'It handles your input, divides the image into N (provided by the user) YxY path.\n' + 'Do not worry, just input any number and the program will tell you if the number is incorrect.\n' + 'Once the number is correct, the program will calculate each part\'s mean color.\n' + 'Then, N number of YxY blocks with random colors will be generated.\n' + 'At last they will be assigned to images\' parts to match the original image in the most accurate way.' 
# rounding boundary accepted, set it to a value between [0, 100)
BLOCKSBOUNDARY = 15
# directory in which the blocks with randomly generated colors would be put in
BLOCKSDIR = 'blocks'
# minimum and maximum amount of accepted parts by the system
MINPARTS, MAXPARTS = 20, 9000
# name of the csv file containing the data about the blocks with pseudo-randomly generated colors
BLOCKFILENAME = 'blocksData.csv'
# name of the csv file containing the data about the source image
IMAGEFILENAME = 'imageData.csv'
# name of the csv file containing the data about the blocks with pseudo-randomly generated colors which were assigned to certain parts of the source image
ASSIGNEDFILENAME = 'blocksAssignedToImages.csv'
# name of the image generated at the end of a program
FINALIMAGE = 'final.png'

#############################################################################################################################
# Check what directories are present, needed and then create them
def checkDirs(base: str, dirs: list().__class__ == str):
    presentDirs = []
    # check what directories are present
    if base == BASEPATH:
        # check what directories are present within base recursively
        for x in Path(base).rglob('*'): 
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
def fileChecker(file: str):
    fileMod = file.split('.')
    if len(fileMod) <= 1:
        logMessage('noFileExt', fileMod)
        printSupported()
        return False
    else:
        fileExt = file.split('.')[-1].lower()
        if fileExt in SUPPORTED:
            logMessage('correctFile', fileExt)
            return True
        else:
            logMessage('wrongFileExt', fileExt)
            printSupported()
            return False

# Read message config from the LOGCONFIG based on msgId, then go to writeMessage
def logMessage(msgId: str, toAdd: str):
    currentTime = str(datetime.now().strftime('%H_%M_%S_%f')[:-3])

    with open(LOGCONFIG, 'r') as singleRow:
        # read a single row
        singleRow = reader(singleRow) 
        for col in singleRow:
            # col[0] = msgType, col[1] = msgId, col[2] = msgContent, col[3] = extras(optional)
            if msgId == col[1]:
                if col[3] == '':
                    msg = f'{currentTime} [{col[0]}] {col[2]}\n'
                    writeMessage(msg, LOGTODAY)
                elif col[3] == 'extras':
                    msg = f'{currentTime} [{col[0]}] {col[2]} {toAdd}\n' 
                    writeMessage(msg, LOGTODAY)

# Print the message and log it into LOGTODAY
def writeMessage(msg: str, logPath: str):
    # print msg without the date at the start and without a newline at the end
    print(msg[13:len(msg) - 1]) 
    #log msg into LOGTODAY
    if path.isfile(Path(logPath)):
        ff = open(logPath, 'a')
        ff.write(msg)
        ff.close()
    elif not path.isfile(Path(logPath)):
        ff = open(logPath, 'x')
        ff.write(msg)
        ff.close()

# Create paths
def createPaths(base: str, dirs: list or str):
    if type(dirs) == list:
        for x in dirs:
            Path(base + x).mkdir(parents = True, exist_ok = True)
            logMessage('newDir', x)
    elif type(dirs) == str:
        Path(base + dirs).mkdir(parents = True, exist_ok = True)
        logMessage('newDir', dirs)

# print a list of supported file extensions
def printSupported():
    print('\nSupported file extensions are: ', end='')
    for ext in SUPPORTED:
        print(ext, end='')
        if ext != SUPPORTED[-1]:
            print(',', end=' ')
    print()

# Handling user input
def fileInput():
    print(INITMESSAGE)
    printSupported()
    logMessage('waitInput', False)
    filePath = input('Please put in an absolute path to an image you would like to have replicated:\n')
    #filePath = 'C:\\Users\\longw\\Desktop\\G Drive\\Praca_inzynierska\\Engineering_Thesis\\test images\\Standard aspect ratio\\FHD\\4k-retro-80s-wallpaper-fhd-1920x1080.jpg'
    #filePath = 'C:/Users/longw/Desktop/G Drive/Praca_inzynierska/Engineering_Thesis/test images/Standard aspect ratio/FHD/4k-retro-80s-wallpaper-fhd-1920x1080.jpg'
    filePath = path.realpath(filePath) # change the provided delim to '\'
    finalPath, datePath = copyToDatePath(filePath)
    datePath = datePath + '\\'

    return finalPath, datePath

# return file name and delimiter the user used to enter a directory
def copyToDatePath(filePath: str):
    # split path on '\\', since all the directories are processed as with double backslashes
    splitPath = filePath.split('\\') 
    delimPlace = len(str(splitPath[-1])) + 1
    file = filePath[len(filePath) - delimPlace + 1:]
    if filePath[-delimPlace] == '\\':
        delim = '\\'
        newDir = str(datetime.now().strftime('%Y%m%d_%H%M%S%f')[2:-5]) # define a directory, e.g. 211210_1324103
        logMessage('loadedFile', file)
        # check whether the file extension is supported and the image resolutions are correct
        if fileChecker(splitPath[-1]): 
            # create new directory for the file
            createPaths(BASEPATH + IMAGESPATH, newDir) 
            datePath = BASEPATH + IMAGESPATH + newDir
            finalPath = datePath + delim + splitPath[-1]
            copyfile(filePath, finalPath)
            return finalPath, datePath
        else:
            exit()

# Cutting the image into smaller images
def ratioAnalyzer(filePath: str, datePath: str):
    image = Image.open(filePath)
    imWidth, imHeight = int(image.size[0]), int(image.size[1])
    image.close()
    while(True):
        myDivisor = 500
        logMessage('waitInput', False)
        myDivisor = int(input('Please provide a number of YxY parts you would like to divide your image into: '))
        if myDivisor < MINPARTS:
            print(f'Provided number of parts is too small: {myDivisor}. Minimal amount of parts is {MINPARTS}')
        elif myDivisor > MAXPARTS:
            print(f'Provided number of parts is too large: {myDivisor}. Maximal amount of parts is {MAXPARTS}')
        else:
            ratioData, smaller, larger = checkImage(myDivisor, imWidth, imHeight, False)
            if ratioData[0] == True:
                x = input(f'Provided number of parts is correct: {myDivisor}. To proceed enter \'Yes\'/\'Y\', or press enter: ')
                x = x.lower()
                if x == 'yes' or x == 'y' or x == '':
                    logMessage('configBlocksArea', str(ratioData[1]))
                    logMessage('configBlocksNumber', str(ratioData[2]))
                    logMessage('configBlocksPixels', str(ratioData[3]))
                    logMessage('configBlocksWidthRest', str(1-ratioData[5]))
                    logMessage('configBlocksHeightRest', str(1-ratioData[7]))
                    ratioData = ratioData[1:]
                    imageData = imageCutting(filePath, ratioData)
                    logMessage('imageAnalyzed', True)
                    saveAsCsv(IMAGEFILENAME, datePath, imageData)
                    logMessage('csvGenerated', IMAGEFILENAME)
                    return (imWidth, imHeight, ratioData[2]), ratioData
            elif ratioData[0] == False:
                logMessage('incorrectNumberBlocks', str(ratioData[1]))
                if isTrue(smaller):
                    print('Closest smaller correct number of parts is: ' + str(smaller[1]))
                if isTrue(larger):
                    print('Closest larger correct number of parts is: ' + str(larger[1]))

# checking number of parts input by the user, returning True and statistics if the number is correct and returning suggested one smaller and one larger number of parts if the number is incorrect
def checkImage(myDivisor: int, imWidth: int, imHeight: int, toFind: str):
    blocksArea = (imWidth * imHeight) / myDivisor
    blocksSize = round(pow(blocksArea,0.5))
    blocksVertical, blocksHorizontal = imWidth / blocksSize, imHeight / blocksSize
    totalImages = ceil(blocksHorizontal) * ceil(blocksVertical)
    restVertical, restHorizontal = float('.' + str(blocksVertical).split('.')[-1]), float('.' + str(blocksHorizontal).split('.')[-1])
    myCondition = ((restHorizontal >= 1 - BLOCKSBOUNDARY/100) and (restVertical >= 1 - BLOCKSBOUNDARY/100))
    conditionSkipLastRowCol = ((restHorizontal <= BLOCKSBOUNDARY/100) and (restVertical <= BLOCKSBOUNDARY/100))
    if not toFind:
        if myCondition:
            return (True, myDivisor, totalImages, blocksSize, int(str(blocksHorizontal).split('.')[0]), restHorizontal, int(str(blocksVertical).split('.')[0]), restVertical), (False), (False)
        elif conditionSkipLastRowCol:
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
        elif myDivisor >= MINPARTS: 
            return checkImage(myDivisor-1, imWidth, imHeight, 'smaller')
        else:
            return (False)
        
    elif toFind == 'larger':
        if myCondition or conditionSkipLastRowCol:
            return (True, myDivisor)
        elif myDivisor < MAXPARTS:
            return checkImage(myDivisor+1, imWidth, imHeight, 'larger')
        else: 
            return (False)

# check whether the variable is true based on it's type
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

# analyze parts of an image, by appending the list with row, column, and mean R, G, B values
def imageCutting(filePath: str, ratioData: tuple):
    image = Image.open(filePath)
    pix = image.load()
    imageData = []
    lastCol = round(ratioData[6] * ratioData[2])
    lastRow = round(ratioData[4] * ratioData[2])
    if ratioData[4] != 0.0:
        width = ratioData[3] + 1
        height = ratioData[5] + 1
    else:
        width = ratioData[3]
        height = ratioData[5]
    #print(ratioData) # e.g.: (298, 289, 70, 17, 0.142857142857142, 17, 0.142857142857142)
    for myRow in range(0, width):
        for myCol in range(0, height):
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

def generateSingleImage(path: str, sizeTuple: tuple, colorTuple: tuple):
    img = Image.new('RGB', sizeTuple, colorTuple)
    img.save(path)
    img.close
    
def generateBlocks(datePath: str, amount: int, size: int):
    createPaths(datePath, BLOCKSDIR)
    blocksPath = datePath + BLOCKSDIR + '\\'
    blocksData = []
    old_percentage = 0
    
    # generate {amount} amount of images to the /blocks children directory within the /backups/images/[date]/ directory
    for singleImage in range(1, amount+1):
        percentage = round((singleImage / amount) * 100, 0)
        blockPath = blocksPath + str(singleImage) + '.png'
        redAmnt = randrange(0,255,1)
        greenAmnt = randrange(0,255,1)
        blueAmnt = randrange(0,255,1)
        blockData = (redAmnt, greenAmnt, blueAmnt)
        blocksData.append(blockData)
        generateSingleImage(blockPath, (size, size), blockData)
        
        # print the progress of image generation
        if percentage > old_percentage:
            old_percentage = percentage
            percentage = str(percentage).split('.')[0]
            print(f'{percentage}% of images generated...')
    logMessage('blocksGenerated', False)
    saveAsCsv(BLOCKFILENAME, datePath, blocksData)
    logMessage('csvGenerated', BLOCKFILENAME)
    return(blocksData)
            
def saveAsCsv(name: str, filePath: str, data: list or tuple):
    with open(filePath + name, 'w', newline='', encoding='UTF8') as f:
        file = writer(f)
        for row in data:
            file.writerow(row)

# to find the correct block, we will need to calculate the three-dimensional Euclidean distance
# the mathematical formula for that would be: pow((x2-x1)**2+(y2-y1)**2+(z2-z1)**2, 0.5)  
def euclidian_distance_vector_single_block(block: tuple, images: pd.DataFrame):
    largeDistanceListWithIndexes = []
    largeDistanceList = []
    for index in range(0, images.index[-1]+1):
        x = (((images['R_images'][index]-block[0])**2 + (images['G_images'][index]-block[1])**2 + (images['B_images'][index]-block[2])**2)**0.5)
        y = [x, index]
        largeDistanceListWithIndexes.append(y)
        largeDistanceList.append(x)
    return largeDistanceListWithIndexes, largeDistanceList

# find the closest number within array which is the closest to the block
def find_closest2(array):
    newArray = []
    for n in range(0, len(array)-1):
        if len(array[n]) == 2:
            newArray.append(array[n][0]) 
        else:
            newArray.append(-1)
    array2 = np.asarray(newArray)
    idx = array2.argmin()
    return array[idx]

# find the closest number within array which is the closest to the mean
def find_closest(array, mean: float):
    newArray = []
    for n in range(0, len(array)-1):
        if len(array[n]) == 2:
            newArray.append(array[n][0]) 
        else:
            newArray.append(-1)
    array2 = np.asarray(newArray)
    idx = (np.abs(array2-mean)).argmin()
    return array[idx]

# remove an element from a list for the second mode
def removeElement2(distanceList: list, index: int):
    for n in range(0, len(distanceList)):
        newList = distanceList[n]
        # setting the distance to maximum possible distance for an image to have (pow(3*pow(256,2),0.5)) plus one, effectively 'removing' the image from the list
        newList[index][0] = 445
        distanceList[n] = newList
    return distanceList

# remove an element from a list for the first mode
def removeElement(distanceList: list, index: int):
    for n in range(0, len(distanceList)):
        newList = distanceList[n]
        newList[index].pop(0)
        newList[index].pop(0)
        distanceList[n] = newList
    return distanceList

def comparingImagesAndBlocks():
    
    #Choosing the mapping mode
    # Mode 1: Every block is assigned to the closest to average part of an image, so the variation in terms of a distance between a block and an image is the smallest. 
    # Mode 2: Every block is assigned to the closest-matching part of an image, starting from the first block from the 'blocksData.csv'. 
    answer = input('Please select block mapping mode(1/2): ')
    trainPath = BASEPATH + IMAGESPATH
    #print(trainPath) # C:\Users\longw\Desktop\G Drive\Praca_inżynierska\Engineering_Thesis\backups\images\
        
    # find the newest directory within backups/images/
    withinImages= Path(trainPath).glob('*')
    dataPaths = [file for file in withinImages if file.is_dir()]
    newestDir = str(dataPaths[-1]) + '\\'
    #print(newestDir) # C:\Users\longw\Desktop\G Drive\Praca_inżynierska\Engineering_Thesis\backups\images\220117_21214749\

    dfImages = pd.read_csv(newestDir + IMAGEFILENAME, index_col=None, header=None, names=['image row', 'image col', 'R_images','G_images','B_images'])
    dfBlocks = pd.read_csv(newestDir + BLOCKFILENAME, index_col=None, header=None, names=['R_blocks','G_blocks','B_blocks', 'Path'])

    # new dataframe columns, the element will be changed once the block is assigned to the part of an image
    dfBlocks['assigned row'] = 0 
    dfBlocks['assigned col'] = 0
    
    singleBlockDistanceWithIndexes = []
    singleBlockDistance = []
    old_percentage = 0
    length = dfBlocks.index[-1]
    for n in range(0, length+1):
        x, y = euclidian_distance_vector_single_block((dfBlocks['R_blocks'][n], dfBlocks['G_blocks'][n], dfBlocks['B_blocks'][n]), dfImages)
        percentage = round((n / length) * 100)
        # print the progress of image generation
        if percentage > old_percentage:
            old_percentage = percentage
            percentage = str(percentage).split('.')[0]
            print(f'{percentage}% of mapping done...')
        singleBlockDistanceWithIndexes.append(x)
        singleBlockDistance.append(y)
    print('We are finalizing some things, please don\'t exit the application. This is expected!')
    if answer == '1':
        meanBlockDistance = []
        for n in range(0, length + 1):
            x = np.mean(singleBlockDistance[n])
            meanBlockDistance.append(x)
        closestBlocks = []
        for n in range(0, length):
            x = find_closest(singleBlockDistanceWithIndexes[n], meanBlockDistance[n])
            y = [x[0], x[1], n]
            
            if n != length-1:
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
        dfBlocks.to_csv(newestDir + ASSIGNEDFILENAME, index=False)
        return True
    elif answer == '2':
        closestBlocks = []
        for n in range(0, length):
            x = find_closest2(singleBlockDistanceWithIndexes[n])
            y = [x[0], x[1], n]
            
            if n != length-1:
                closestBlocks.append(y)
            singleBlockDistanceWithIndexes = removeElement2(singleBlockDistanceWithIndexes, x[1])
            
        for n in singleBlockDistanceWithIndexes[dfBlocks.index[-1]]:
            if n:
                closestBlocks.append([n[0], n[1], dfBlocks.index[-1]])
        #print(closestBlocks)
        for n in closestBlocks:
            dfBlocks['assigned row'][n[2]] = dfImages['image row'][n[1]]
            dfBlocks['assigned col'][n[2]] = dfImages['image col'][n[1]]
        logMessage('blocksMatched', True)
        dfBlocksColumns = dfBlocks.columns.tolist()
        dfBlocksColumns = dfBlocksColumns[0:3] + dfBlocksColumns[4:] + dfBlocksColumns[3:4]
        dfBlocks = dfBlocks[dfBlocksColumns]
        dfBlocks.to_csv(newestDir + ASSIGNEDFILENAME, index=False)
        logMessage('csvGenerated', ASSIGNEDFILENAME)
        return True
    
def generateImage(imWidthHeight: tuple):
    dataPath = BASEPATH + IMAGESPATH
    # find the newest directory within backups/images/
    withinImages= Path(dataPath).glob('*')
    dataPaths = [file for file in withinImages if file.is_dir()]
    dataPath = str(dataPaths[-1]) + '\\'
    dataFile = dataPath + ASSIGNEDFILENAME
    imagePath = dataPath + FINALIMAGE
    #print(newestDir) # C:\Users\longw\Desktop\G Drive\Praca_inżynierska\Engineering_Thesis\backups\images\220125_23002288\blocksAssignedToImages.csv
    generateSingleImage(imagePath, (imWidthHeight[0], imWidthHeight[1]), (255, 255, 255))
    n = 1
    print('Keep pushing any key to see the progress of image generation!')
    with open(dataFile, 'r') as singleRow:
        singleRow = reader(singleRow) # read a single row
        next(singleRow)
        img = cv2.imread(imagePath)
        for col in singleRow:
            n = n + 1
            color = (col[0], col[1], col[2])
            rowNum = int(col[3])
            colNum = int(col[4])
            size = int(imWidthHeight[2])
            img[rowNum*size:(rowNum+1)*size,colNum*size:(colNum+1)*size] = color
            if n % 5 == 0:
                cv2.imshow("img",img)
                cv2.waitKey()

    #cv2.imshow("img",img)
    #cv2.waitKey()
    #cv2.destroyAllWindows()
    cv2.imwrite(imagePath, img)
    logMessage('imageGenerated', True)
    print('Final image generated!')
    print(f'{imagePath}')
    
def main():
    # initial check for directories # commented as it's working properly
    if checkDirs(BASEPATH, BASEDIRS): 
        #handling user input
        myFile, datePath = fileInput()
        
        # increase only if met with "RecursionError: maximum recursion depth exceeded while calling a Python object"
        setrecursionlimit(100000) 
        
        # image processing
        imWidthHeight, ratioData = ratioAnalyzer(myFile, datePath)
        
        # generation of N YxY blocks based on the data of the original image (Amount of parts, Height/Width of a single part)
        generateBlocks(datePath, ratioData[1], ratioData[2])
        
        # disabling the false positive message which pandas return in regards with the operation
        pd.options.mode.chained_assignment = None
        
        # matching blocks to images' parts
        if comparingImagesAndBlocks():
            # final image generation
            generateImage(imWidthHeight)
        
if __name__ == '__main__':
    main()