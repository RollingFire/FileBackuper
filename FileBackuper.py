'''
By Austin Dorsey
Started: 4/13/18
Last Modified: 6/5/18
Version : 2.0
Discription: Reads the file in the working directory named "BackupData.txt"
             with the first path on a line being the file/directory to be
             backed up, and the second path on the line being the destination.
             Will create any needed directories. Paths are to be sepporated
             by "|". "*" may be used for file layout either befor or after the
             "|" as they will be ignored. If the drive or path does not exist,
             the path pair will be skipped. If the first path is "Exclude"
             without the quotations, that file or directory will not be
             backed up.
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


def backupFile(src, dest):
    '''Backsup the file if it is newer than what is in the destination. Creates any needed directories.'''
    try:
        os.makedirs(dest)
    except:
        pass
    desPath = os.path.join(dest, pathSplit(src)[1])
    if os.path.exists(desPath):
        if (os.path.getmtime(src) > os.path.getmtime(desPath)):
            shutil.copy2(src, desPath)
            print('Backedup  - ', src)
    else:
        shutil.copy2(src, desPath)
        print('Copied    - ', src)


def backupPath(src, dest, excludes):
    '''Recursivly called to backup all of the files in the src path, and saves them to the destination.'''
    if src in excludes:
        return
    if not os.path.exists(os.path.splitdrive(dest)[0]):
        print('Drive does not exist. Connect drive', os.path.splitdrive(dest)[0])
        return
    if not os.path.exists(src):
        print('Source file', src, 'does not exist.')
        return
    srcDir, srcFile = pathSplit(src)
    if srcFile != None:
        backupFile(src, dest)
    else:
        newDest = os.path.join(dest, srcDir.split('\\')[-1])
        paths = os.listdir(src)
        for path in paths:
            if path.startswith('.'):
                continue
            backupPath(os.path.join(src, path), newDest, excludes)


def main():
    '''Runs the program and does the heavy lifting to backup the files.'''
    excludes = []
    try:
        with open(r'.\\BackupData.txt', "r") as backupFile:
            pathPairs = backupFile.readlines()
    except OSError:
        print('Failed to load "BackupData.txt". Make sure file exists and is',
              'located in the working directory.')
        return
    
    for pathPair in pathPairs:
        if pathPair == '\n':
            continue
        #Formating path pair.
        pathPair = pathPair.replace('\n', '')
        paths = pathPair.split('|')
        if len(paths) != 2:
            print('Invalid path pair:', pathPair)
            continue
        paths[0] = paths[0].replace('*', '')
        paths[1] = paths[1].replace('*', '')
            
        if paths[0] == "Exclude":
            excludes.append(paths[1])
            continue

        paths[0] = os.path.normpath(paths[0])
        paths[1] = os.path.normpath(paths[1])

        backupPath(paths[0], pathSplit(paths[1])[0], excludes)


if __name__ == '__main__':
    main()
    input('Press enter to close.')
