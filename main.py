import pathlib
from os import path
from datetime import date
from datetime import datetime

# Global variables:
BASEPATH = str(pathlib.Path(__file__).parent.resolve()) + '/'
BASEDIRS = ('logs', 'backups\\blocks', 'backups\\images',)
CONFIGFILE = '.\\config.properties'
SUPPORTED = ('png', 'jpg', 'jpeg')
LOGFILE = BASEPATH + 'logs/logs_'
INFO = ' [INFO]'
ERROR = ' [ERROR]'

def logMessage(messagetype, directory, file):
    CURRENTDATE = str(date.today().strftime("%Y_%m_%d"))
    CURRENTTIME = str(datetime.now().strftime('%H_%M_%S_%f')[:-3])

    NEWDIR_code = 'newDir'
    NEWDIR_msg = CURRENTTIME + INFO + ' New directory has been created - '
    NONEWDIRS_code = 'presentDir'
    NONEWDIR_msg = CURRENTTIME + INFO + ' Directory already present - '
    DIRSPRESENT_code = 'dirsPresent'
    DIRSPRESENT_msg = CURRENTTIME + INFO + ' All directories needed are present'
    WAITINPUT_code = 'waitInput'
    WAITINPUT_msg = CURRENTTIME + INFO + ' Waiting for user input...'
    WRONGFILEEXT_code = 'wrongFileExt'
    WRONGFILEEXT_msg = CURRENTTIME + ERROR + ' File with the provided extension is not supported: '
    NOFILEEXT_code = 'noFileExt'
    NOFILEEXT_msg = CURRENTTIME + ERROR + ' File provided does not have any file extension defined'
    CORRFILEEXT_code = 'correctFile'
    CORRFILEEXT_msg = CURRENTTIME + INFO + ' Provided file extension is supported: '

    logToday = LOGFILE + CURRENTDATE + '.txt'

    if messagetype == NEWDIR_code:
        msg = NEWDIR_msg + file + '\n'
        writeMessage(msg, logToday)
    elif messagetype == NONEWDIRS_code:
        msg = NONEWDIR_msg + file + '\n'
        writeMessage(msg, logToday)
    elif messagetype == DIRSPRESENT_code:
        msg = DIRSPRESENT_msg + '\n'
        writeMessage(msg, logToday)
    elif messagetype == WAITINPUT_code:
        msg = WAITINPUT_msg + '\n'
        writeMessage(msg, logToday)
    elif messagetype == WRONGFILEEXT_code:
        msg = WRONGFILEEXT_msg + file + '\n'
        writeMessage(msg, logToday)
    elif messagetype == NOFILEEXT_code:
        msg = NOFILEEXT_msg + file + '\n'
        writeMessage(msg, logToday)
    elif messagetype == CORRFILEEXT_code:
        msg = CORRFILEEXT_msg + file + '\n'
        writeMessage(msg, logToday)

def writeMessage(msg, logPath):
    print(msg[:len(msg)-1])
    if path.isfile(pathlib.Path(logPath)):
        ff = open(logPath, "a")
        ff.write(msg)
        ff.close()
    elif not path.isfile(pathlib.Path(logPath)):
        ff = open(logPath, "x")
        ff.write(msg)
        ff.close()

def createPaths(base, dirs):
    for x in dirs:
        pathlib.Path(base + x).mkdir(parents=True, exist_ok=True)
        logMessage('newDir', base, x)

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

def fileInput():
    logMessage('waitInput', False, False)
    #    filePath = input("Please put in an absolute path to an image you would like to have replicated:\n")
    filePath = 'file.png'
    if extensionChecker(filePath):
        print("Passed the vibe check!")


if __name__ == "__main__":
    checkDirs(BASEPATH, BASEDIRS)
    fileInput()
