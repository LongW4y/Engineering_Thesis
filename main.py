import pathlib
from os import path
from datetime import date
from datetime import datetime
from csv import reader
from shutil import copyfile
import re
import timeit

# Global variables:
BASEPATH = str(pathlib.Path(__file__).parent.resolve()) + '\\'
BASEDIRS = ('logs', 'backups\\blocks', 'backups\\images')
IMAGESPATH = 'backups\\images\\'
CONFIGFILE = '.\\config.properties'
LOGCONFIG = '.\\logs_config.csv'
SUPPORTED = ('png', 'jpg', 'jpeg')
LOGFILE = BASEPATH + 'logs/logs_'


def logMessage(messagetype, directory, file):
    CURRENTDATE = str(date.today().strftime("%Y_%m_%d"))
    CURRENTTIME = str(datetime.now().strftime('%H_%M_%S_%f')[:-3])
    logToday = LOGFILE + CURRENTDATE + '.txt'

    with open('logs_config.csv', 'r') as read_obj:
        next(read_obj)
        csv_reader = reader(read_obj)
        for row in csv_reader:
            if messagetype == row[1]:
                if row[3] == 'file':
                    msg = CURRENTTIME + ' [' + row[0] + ']' + row[2] + file + '\n'
                    writeMessage(msg, logToday)
                elif row[3] == '':
                    msg = CURRENTTIME + ' [' + row[0] + ']' + row[2] + '\n'
                    writeMessage(msg, logToday)


def writeMessage(msg, logPath):
    print(msg[:len(msg) - 1])
    if path.isfile(pathlib.Path(logPath)):
        ff = open(logPath, "a")
        ff.write(msg)
        ff.close()
    elif not path.isfile(pathlib.Path(logPath)):
        ff = open(logPath, "x")
        ff.write(msg)
        ff.close()


def createPaths(base, dirs):
    if type(dirs) == list:
        for x in dirs:
            pathlib.Path(base + x).mkdir(parents=True, exist_ok=True)
            logMessage('newDir', base, x)
    elif type(dirs) == str:
        pathlib.Path(base + dirs).mkdir(parents=True, exist_ok=True)
        logMessage('newDir', base, dirs)


def checkDirs(base, dirs):
    presentDirs = []
    if base == BASEPATH:
        for x in pathlib.Path(base).rglob('*'):
            if x.is_dir():
                presentDirs.append(str(x)[len(BASEPATH):])
    neededDirs = []
    for x in dirs:
        if x in presentDirs:
            logMessage('presentDir', base, x)
        elif not x in presentDirs:
            neededDirs.append(x)
    if neededDirs:
        createPaths(base, neededDirs)
    logMessage('dirsPresent', base, True)


def extensionChecker(filePath):
    fileExt = filePath.split(".")[-1].lower()
    if fileExt in SUPPORTED:
        logMessage('correctFile', filePath, fileExt)
        return True
    elif fileExt == '':
        logMessage('noFileExt', filePath, fileExt)
        print("Supported file extensions are:", end='')
        for ext in SUPPORTED:
            print(ext, end='')
            if ext != SUPPORTED[-1]:
                print(',', end=' ')
        return False
    else:
        logMessage('wrongFileExt', filePath, fileExt)
        print("Supported file extensions are: ", end='')
        for ext in SUPPORTED:
            print(ext, end='')
            if ext != SUPPORTED[-1]:
                print(',', end=' ')
        return False


def copyFile(filePath):
    delimPlace = len(str(re.split('/|\\\\', filePath)[-1])) + 1
    if filePath[-delimPlace] == '/':
        delim = '/'
        newDir = str(datetime.now().strftime('%Y%m%d_%H%M%S%f')[2:-4])
        createPaths(BASEPATH + IMAGESPATH, newDir)
        extensionChecker(filePath)
        copyfile(filePath, BASEPATH + IMAGESPATH + newDir + delim + filePath.split(delim)[-1])
    elif filePath[-delimPlace] == '\\':
        delim = '\\'
        newDir = str(datetime.now().strftime('%Y%m%d_%H%M%S%f')[2:-4])
        createPaths(BASEPATH + IMAGESPATH, newDir)
        extensionChecker(filePath)
        copyfile(filePath, BASEPATH + IMAGESPATH + newDir + delim + filePath.split(delim)[-1])


def fileInput():
    logMessage('waitInput', False, False)
    #    filePath = input("Please put in an absolute path to an image you would like to have replicated:\n")
    #    filePath = "C:\\Users\\longw\\Desktop\\G Drive\\Praca inżynierska\\Engineering_Thesis\\test images\\Standard aspect ratio\\FHD\\4k-retro-80s-wallpaper-fhd-1920x1080.jpg"
    filePath = 'C:/Users/longw/Desktop/G Drive/Praca inżynierska/Engineering_Thesis/test images/Standard aspect ratio/FHD/4k-retro-80s-wallpaper-fhd-1920x1080.jpg'
    copyFile(filePath)


if __name__ == "__main__":
     checkDirs(BASEPATH, BASEDIRS)
     fileInput()
#    print(timeit.timeit('fileInput', 'from __main__ import fileInput')) # ~0.010789599999999996
