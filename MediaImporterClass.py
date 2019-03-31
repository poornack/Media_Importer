import os
import sys
import shutil
from datetime import datetime

def isFileJpg(fileName):
    
    if fileName[-4:] == '.JPG' or fileName[-4:] == '.jpg':
        return True
    else:
        return False

def isFileAVCHD(fileName):
    
    if fileName[-4:] == '.MTS' or fileName[-4:] == '.mts':
        return True
    else:
        return False

def isFileAVCHDMetaData(fileName):
    if fileName[-4:] == '.CPI' or fileName[-4:] == '.cpi':
        return True
    else:
        return False


class MediaFile:
    
    filePath: str = ''
    fileName: str = ''
    fileType: str = ''
    dateCreated: int = 0  #UNIX time
    isMetaDataInSeperateFile: bool = False
    metaDataFileName: str = ''
    metaDataFilePath: str = ''
    
    def __init__(self, mediaFileName, metaDataFileName = None, ignoreMetaDataForVideoFile = False):
        
        if type(mediaFileName) is not str:
            raise TypeError("mediaFileName must be a String")
        if os.path.isfile(mediaFileName) == False:
            raise ValueError("Invalid file: '{0}'".format(mediaFileName))
        
        self.filePath = os.path.dirname(mediaFileName)
        self.fileName = os.path.basename(mediaFileName)
        self.fileType = (((os.path.splitext(mediaFileName))[1])[1:]).upper()
        self.dateCreated = os.stat(mediaFileName).st_ctime
        
        if metaDataFileName is not None:
            
            if type(metaDataFileName) is not str:
                raise TypeError("metaDataFileName must be a String")
            if os.path.isfile(metaDataFileName) == False:
                raise ValueError("Invalid file: '{0}'".format(metaDataFileName))
            
            self.metaDataFileName = os.path.basename(metaDataFileName)
            self.metaDataFilePath = os.path.dirname(metaDataFileName)
            isMetaDataInSeperateFile = True
    
    @classmethod
    def getMediaFileFromFileName(self, mediaFileList, fileName):
        
        for mediaFile in mediaFileList:
            fullFileName = os.path.join(mediaFile.filePath, mediaFile.fileName)
            if fullFileName == fileName:
                return mediaFile
        
        return None



class MediaImporter:
    
    IMAGES_PATH = 'DCIM/'
    VIDEOS_FILE_PATH = 'private/AVCHD/BDMV/STREAM/'
    VIDEOS_CPI_FILE_PATH = 'private/AVCHD/BDMV/CLIPINF/'
    VIDEOS_PLAYLIST_PATH = 'private/AVCHD/BDMV/PLAYLIST/'
    FOLDER_DATE_TIME_FORMAT = '%Y-%m-%D'
    
    rootPath = ''
    images = []
    videos = []
    filesNotImported = []
    importDirectory = ''
    
    def __init__(self, sdCardPath):
        
        # Check that sdCardPath is a valid path
        if type(sdCardPath) is not str:
            raise TypeError("sdCardPath must be a String")
        elif os.path.isdir(sdCardPath) == False:
            raise ValueError("Invalid path: '{0}'".format(sdCardPath))
        
        print("Found SD card at '{0}'".format(sdCardPath))
        self.rootPath = sdCardPath
        
        #Find All JPGs
        for root, dirs, files in os.walk(os.path.join(sdCardPath, self.IMAGES_PATH)):
            for filename in files:
                if isFileJpg(filename):
                    self.images.append(MediaFile(os.path.join(root, filename)))
                else:
                    self.filesNotImported.append(os.path.join(root, filename))
        
        metaDataFiles = []
        #Find ALl AVCHD Metadata Files
        for root, dirs, files in os.walk(os.path.join(sdCardPath, self.VIDEOS_CPI_FILE_PATH)):
            for filename in files:
                if isFileAVCHDMetaData(filename):
                    metaDataFiles.append(os.path.join(root, filename))
                else:
                    self.filesNotImported.append(os.path.join(root, filename))
        
        #Find All AVCHDs
        for root, dirs, files in os.walk(os.path.join(sdCardPath, self.VIDEOS_FILE_PATH)):
            for filename in files:
                if isFileAVCHD(filename):
                    correspondingMetaDataFile =    os.path.join(sdCardPath, self.VIDEOS_CPI_FILE_PATH,os.path.splitext(os.path.basename(filename))[0] + '.CPI')
                    
                    if correspondingMetaDataFile in metaDataFiles:
                        self.videos.append(MediaFile(os.path.join(root, filename), correspondingMetaDataFile))
                        metaDataFiles.remove(correspondingMetaDataFile)
                    else:
                        print("Could not fild metadata for file '{0}'".format(filename))
                        self.videos.append(MediaFile(os.path.join(root, filename)))
                else:
                    self.filesNotImported.append(os.path.join(root, filename))
    
    
    def importFile(self, file, destDir = importDirectory):
        
        if type(dest) is not str:
            raise TypeError("fileName musst be a String")
        if os.path.isdir(dest):
            raise ValueError("Invalid File '{0}'".format(fileName))
        if file is None:
            raise ValueError("File is empty")
            
        dateCreated = file.dateCreated
 
        destSubDir = os.path.join(destDir, datetime.utcfromtimestamp(dateCreated).strftime(FOLDER_DATA_TIME_FORMAT))
                
        shutil.copy2(file.filePath, destSubDir)
        
        if file.isMetaDataInSeperateFile == True:
            cpiDir = os.path.join(destSubDir, 'AVCHD_CPI')
            
        shutil.copy2(file.metaDataFilePath, cpiDir)
        
    def importAllFiles(self, destDir = importDirectory):
        
        for _file in images:
            importFile(_file, destDir)
        
        for _file in videos:
            importFile(_file, destDir)
        
    def setImportDirectory(self, importDirectory):
        
        if type(importDirectory) is not str:
            raise TypeError("importDirectory must be a String")
        if os.path.isdir(importDirectory) == False:
            raise ValueError("Invalid path '{0}'".format(importDirectory))
        
        self.importDirectory = importDirectory
    



if __name__ == '__main__':
    
    # sdCardPath = '/Volumes/Untitled'
    sdCardPath = '/Users/Poorna/Poorna/OneDrive - University of Victoria/ENGR_Hobby/SD_Card_Importer/sample'
    destPath = '/Volumes/Toshiba/Videos/Videos'
    mediaImporter = MediaImporter(sdCardPath)
    
    for image in mediaImporter.images:
        print(image.fileName)
        pass
    
    
    for video in mediaImporter.videos:
        print("{0} with metadata {1}".format(video.fileName, video.metaDataFileName))
        pass
    
    for _fileName in mediaImporter.filesNotImported:
        print(_fileName)
        pass
                    
    
    
    
    
