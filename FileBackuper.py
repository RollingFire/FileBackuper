'''
By Austin Dorsey
Started: 4/13/18
Last Modified: 5/23/18
Discription: Reads the file in the working directory named "BackupData.txt" 
             with the first path on a line being the file/directory to be 
             backed up, and the second path on the line being the destination.
             Will create any needed directories. Paths are to be sepporated
             by "|". "*" may be used for file layout either befor or after the 
             "|" as they will be ignored. If the drive or path does not exist, 
             the path pair will be skipped.
'''

import os
import shutil

def pathSplit(path):
    '''Splits a absoute file path into its parts. directory path and filename.'''
    splitPath = path.split('\\')
    path = ''
    file = None
    for split in splitPath:
        if os.path.isfile(path + split):
            file = split
        else:
            path += split + '\\'
    return os.path.normpath(path), file


def getFiles(start):
    '''Gives the absolute file names for all of the files 
    including the ones in the sub directories.
    '''
    files = []
    paths = os.listdir(start)
    for path in paths:
        if path.startswith("."):
            continue
        fullPath = os.path.join(start, path)
        _, file = pathSplit(fullPath)
        if file is None:
            files += getFiles(fullPath)
        else:
            files.append(fullPath)
    return files


def main():
    '''Runs the program and does the heavy lifting to backup the files.'''
    try:
        with open(r'.\\BackupData.txt', "r") as backupFile:
            pathPairs = backupFile.readlines()
            backupFile.close()

        for pathPair in pathPairs:
            #Formating path pair.
            pathPair = pathPair.replace('\n', '')
            paths = pathPair.split('|')
            if len(paths) != 2:
                print('Invalid path pair:', pathPair)
                continue
            paths[0] = paths[0].replace('*', '')
            paths[1] = paths[1].replace('*', '')
            srcDir, srcFile = pathSplit(paths[0])
            desDir = pathSplit(paths[1])[0]

            #Checks for the directory.
            if not os.path.exists(os.path.splitdrive(desDir)[0]):
                print('Drive does not exist. Connect drive', os.path.splitdrive(desDir)[0])
                continue

            #To backup an entire folder.
            if srcFile is None:
                if os.path.exists(srcDir):
                    #Removes the last directoty from the sorce directory, so
                    #that the last directory will be created.
                    srcBaseList = []
                    srcBaseSplit = srcDir.split('\\')
                    while srcBaseSplit[-1] == '':
                        del srcBaseSplit[-1]
                    del srcBaseSplit[-1]
                    for i in srcBaseSplit:
                        i.replace('\\', '')
                        srcBaseList.append(i + '\\')
                    srcBase = ''.join(srcBaseList)
                
                    files = getFiles(srcDir)
                    for file in files:
                        fileDir, fileFile = pathSplit(file)
                        fileDir = fileDir.replace(srcBase, '')
                        try:
                            os.makedirs(os.path.join(desDir, fileDir))
                        except:
                            pass
                        desPath = os.path.join(desDir, fileDir, fileFile)
                        if os.path.exists(desPath):
                            if os.path.getmtime(file) > os.path.getmtime(desPath):
                                shutil.copy2(file, desPath)
                                print('Backedup  - ', file)
                        else:
                            shutil.copy2(file, desPath)
                            print('Copied    - ', file)
                else:
                    print('Source file', srcDir, 'does not exist.')

            #To backup just a file.
            else:
                srcPath = os.path.join(srcDir, srcFile)
                if os.path.exists(srcPath):
                    try:
                        os.makedirs(desDir)
                    except:
                        pass
                    desPath = os.path.join(desDir, srcFile)
                    if os.path.exists(desPath):
                        if (os.path.getmtime(srcPath) > os.path.getmtime(desPath)):
                            shutil.copy2(srcPath, desPath)
                            print('Backedup  - ', srcPath)
                    else:
                        shutil.copy2(srcPath, desPath)
                        print('Copied    - ', srcPath)
                else:
                    print('Source file', srcPath, 'does not exist.')
    except OSError:
        print('Failed to load "BackupData.txt". Make sure file exists and is',
              'located in the working directory.')


if __name__ == '__main__':
    main()
    input('Press enter to close.')
