import pathlib
from os import path


def createPaths(base, dirs, confile):
    f = open("config.properties", "x")
    for x in dirs:
        pathlib.Path(base + x).mkdir(parents=True, exist_ok=True)
        f.write(str(x) + " - 1\n")
    f.close()


def checkConfig(base, dirs, confile):
    if path.isfile(pathlib.Path(confile)):
        return True
    else:
        createPaths(base, dirs, confile)


if __name__ == "__main__":
    BASEPATH = str(pathlib.Path(__file__).parent.resolve())
    CONFIGFILE = './config.properties'
    BASEDIRS = ['/backups/blocks', '/backups/images', '/logs']

    if checkConfig(BASEPATH, BASEDIRS, CONFIGFILE):
        f = open(CONFIGFILE, "r")
        for x in range(1, 2):
            print(f.readline())
