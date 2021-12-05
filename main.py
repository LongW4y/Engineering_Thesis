import pathlib
from os import path
from datetime import date
from datetime import datetime

# Global variables:
BASEPATH = str(pathlib.Path(__file__).parent.resolve()) + '/'
BASEDIRS = ('logs', 'backups\\blocks', 'backups\\images',)
CONFIGFILE = '.\\config.properties'
LOGFILE = BASEPATH + 'logs/logs_'
INFO = ' [INFO]'
ERROR = ' [ERROR]'

def logMessage(messagetype, base, file):
    CURRENTDATE = str(date.today().strftime("%Y_%m_%d"))
    CURRENTTIME = str(datetime.now().strftime('%H_%M_%S_%f')[:-3])

    NEWDIR_code = 'newDir'
    NEWDIR_msg = CURRENTTIME + INFO + ' New directory has been created - '
    NONEWDIRS_code = 'presentDir'
    NONEWDIR_msg = CURRENTTIME + INFO + ' Directory already present - '
    DIRSPRESENT_code = 'dirsPresent'
    DIRSPRESENT_msg = CURRENTTIME + INFO + ' All directories needed are present'

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

def writeMessage(msg, logPath):
    print(msg)
    if path.isfile(pathlib.Path(logPath)):
        ff = open(logPath, "a")
        ff.write(msg)
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


if __name__ == "__main__":
    checkDirs(BASEPATH, BASEDIRS)


