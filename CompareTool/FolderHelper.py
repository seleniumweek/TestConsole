import os


def FilterFilesinFolder(folderPath):
   x = [os.path.abspath(os.path.join(folderPath, p)) for p in os.listdir(folderPath) if p.endswith('.pdf')]
   file_list = list(x)
   return file_list


def CreateFolder(dynamicfolder):
    if not os.path.exists(dynamicfolder):
        os.makedirs(dynamicfolder)
    else:
        for files in os.listdir(dynamicfolder):
            if files == "dataset":
                os.remove(dynamicfolder + "dataset")
                os.makedirs(dynamicfolder)

def GetMatchedFile(fileslist,requiredfilename):
    for filename in fileslist:
        dynamicfilename = os.path.basename(filename)
        if dynamicfilename == requiredfilename:
            file2filename = dynamicfilename
            file2filename = os.path.join(os.path.dirname(filename), dynamicfilename)
            return file2filename
    return None
    
def SaveFileInTheFolder():
   pass