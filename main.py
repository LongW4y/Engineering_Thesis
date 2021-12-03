import pathlib
from os import path
from datetime import date


def logMessage(messagetype, base, file):
    LOGFILE = base + 'logs/logs'
    NEWDIR_code = 'newDir'
    NEWDIR = ' New directory has been created - '
    NONEWDIRS_code = 'presentDir'
    NONEWDIR = ' Directory already present - '
    logToday = LOGFILE + str(date.today().strftime("%Y_%m_%d")) + '.txt'
    if messagetype == NEWDIR_code:
        if path.isfile(pathlib.Path(logToday)):
            ff = open(logToday, "a")
            ff.write(NEWDIR + file + '\n')
        elif not path.isfile(pathlib.Path(logToday)):
            ff = open(logToday, "x")
            ff.write(NEWDIR + file + '\n')
        ff.close()
        return True
    elif messagetype == NONEWDIRS_code:
        if path.isfile(pathlib.Path(logToday)):
            ff = open(logToday, "a")
            ff.write(NONEWDIR + file + '\n')
        elif not path.isfile(pathlib.Path(logToday)):
            ff = open(logToday, "x")
            ff.write(NONEWDIR + file + '\n')
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
                logMessage('presentDirs', BASEPATH, x)



