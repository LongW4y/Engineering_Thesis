import pathlib
from os import path
from datetime import date
from datetime import datetime


def logMessage(messagetype, base, file):
    LOGFILE = base + 'logs/logs_'
    CURRENTDATE = str(date.today().strftime("%Y_%m_%d"))
    CURRENTTIME = str(datetime.now().strftime('%H_%M_%S_%f')[:-3])
    NEWDIR_code = 'newDir'
    INFO = ' [INFO]'
    ERROR = ' [ERROR]'
    NEWDIR = CURRENTTIME + INFO + ' New directory has been created - '
    NONEWDIRS_code = 'presentDir'
    NONEWDIR = CURRENTTIME + INFO + ' Directory already present - '
    logToday = LOGFILE + CURRENTDATE + '.txt'
    if messagetype == NEWDIR_code:
        msg = NEWDIR + file + '\n'
        print(msg)
        if path.isfile(pathlib.Path(logToday)):
            ff = open(logToday, "a")
            ff.write(msg)
        elif not path.isfile(pathlib.Path(logToday)):
            ff = open(logToday, "x")
            ff.write(NEWDIR + file + '\n')
        ff.close()
        return True
    elif messagetype == NONEWDIRS_code:
        msg = NONEWDIR + file + '\n'
        print(msg)
        if path.isfile(pathlib.Path(logToday)):
            ff = open(logToday, "a")
            ff.write(msg)
        elif not path.isfile(pathlib.Path(logToday)):
            ff = open(logToday, "x")
            ff.write(msg)
        ff.close()
        return True



def createPaths(base, dirs, confile):
    f = open("config.properties", "x")
    for x in dirs:
        pathlib.Path(base + x).mkdir(parents=True, exist_ok=True)
        f.write(str(x) + " - 1\n")
        print("Directory has been created - " + str(x))
        logMessage('newDir', base, x)
    f.close()


def checkConfig(base, dirs, confile):
    if path.isfile(pathlib.Path(confile)):
        return True
    else:
        createPaths(base, dirs, confile)


if __name__ == "__main__":
    BASEPATH = str(pathlib.Path(__file__).parent.resolve()) + '/'
    CONFIGFILE = './config.properties'
    BASEDIRS = ('logs', 'backups/blocks', 'backups/images')

    if checkConfig(BASEPATH, BASEDIRS, CONFIGFILE):
        f = open(CONFIGFILE, "r")
        presentDirs = []
        for x in f:
            presentDirs.append(x.split("=")[0])
            neededDirs = []
        for x in presentDirs:
            if not x in BASEDIRS:
                print(presentDirs)
                neededDirs.append(x)
            elif x in BASEDIRS:
                logMessage('presentDir', BASEPATH, x)



