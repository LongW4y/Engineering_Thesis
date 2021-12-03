import pathlib
from os import path
from datetime import date

def logMessage(messagetype, base, file):
    LOGFILE = base + 'logs/logs'
    NEWDIR_code = 'newDir'
    NEWDIR = 'New directory has been created - '
    logToday = LOGFILE + str(date.today().strftime("%Y_%m_%d")) + '.txt'
    if messagetype == NEWDIR_code:
        if path.isfile(pathlib.Path(logToday)):
            ff = open(logToday, "a")
            ff.write(NEWDIR + file)
        elif not path.isfile(pathlib.Path(logToday)):
            ff = open(logToday, "x")
            ff.write(NEWDIR + file)
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
    BASEDIRS = ['logs', 'backups/blocks', 'backups/images']

    if checkConfig(BASEPATH, BASEDIRS, CONFIGFILE):
        f = open(CONFIGFILE, "r")
        noDirs = []
        for x in f:
            myDir = x.split(None, 1)[0]
            isPresent = int(x[-2:])
            for y in BASEDIRS:
                if myDir == x and isPresent == 1:
                    noDirs.append(myDir)
        checkConfig(BASEPATH, noDirs, CONFIGFILE)