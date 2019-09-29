#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys

print("lala "+ str() +"joder")

print("done")

sys.exit()


# In[ ]:


folderOrigin = sys.argv[1]
folderDestination = sys.argv[2]


# In[4]:


#we import the libraries we will use
import glob
import os
import os.path, time
import shutil
import sys
import filecmp

#the following function creates folders
def createFolders(year, imageOrVideo):
    try:
        if not os.path.exists(folderDestination+"/"+imageOrVideo):
            os.makedirs(folderDestination+"/"+imageOrVideo)
            print("\n Creating folder "+ str(imageOrVideo))
        else:
            if foldersExist not True:
                print("\n The folder "+str(imageOrVideo)+" already exists \n")

    except OSError:
        print ('Error: Creating directory. ' +  str(imageOrVideo))  
        
    try:
        if not os.path.exists(folderDestination+"/"+imageOrVideo+"/"+year):
            os.makedirs(folderDestination+"/"+imageOrVideo+"/"+year)
            print("\n Creating folder "+ str(year))
        else:
            if foldersExist not True:
                print("\n The folder "+str(year)+" already exists \n")

    except OSError:
        print ('Error: Creating directory. ' +  str(year))  




def isImageOrVideo(file):
    
    if file[1:].split(".")[len(file[1:].split("."))-1] in formats["video"]:
        return "videos"
    elif file[1:].split(".")[len(file[1:].split("."))-1] in formats["image"]:
        return "images"
    else:
        print("\n The file "+str(file)+" will be ingored since it is not a video nor image \n")
            
        

def whichYear(file):
    predate = time.ctime(os.path.getmtime(file))
    date = predate[20:26]
    return date



def treatDuplicates(file,path,year,imageOrVideo):
    insideYearFolder = folderDestination+"/"+imageOrVideo+"/"+year
    duplicateExistentFile = insideYearFolder+"/"+file
    if filecmp.cmp(path,duplicateExistentFile):
        duplicateFilesNotCopied.append(" - "+file+ "\n") 
    else:
        file2= "c"+file
        
        while file2 in os.listdir(insideYearFolder):
              file2 = "c"+file2
        shutil.copy(path,insideYearFolder +"/"+file2)
        renamedDuplicateFiles.append(" - "+file+" " + "-->"+ " -"+file2+"\n")
        
folderOrigin = "/home/rangelrey/Documents/test"
folderDestination = "/home/rangelrey/Documents/test2"
foldersExist = False
videoExtensions= ("swf","mpg","qt","flv", "webm","wmv", "wma", "asf","ogg", "oga", "ogv", "ogx","3gp", "3gp2", "3g2", "3gpp", "3gpp2","mp4", "m4a", "m4v", "f4v", "f4a", "m4b", "m4r", "f4b", "mov","avi")
imageExtensions =("jpg", "jpeg", "jpe", "jif", "jfif", "jfi","png","gif","webp","tiff","tif","psd","raw", "arw", "cr2", "nrw", "k25","bmp", "dib","heif", "heic","ind", "indd", "indt","jp2", "j2k", "jpf", "jpx", "jpm", "mj2","svg", "svgz"    )
formats = { "video": videoExtensions, "image": imageExtensions }


# In[8]:


excluded = ["ipynb","DS","To_Be_Classified","html",".sample"]
duplicateFilesNotCopied = []
renamedDuplicateFiles = []
def function(folderOrigin,folderDestination ):
        #if it is a file
    if os.path.isfile(folderOrigin):
        file = folderOrigin[folderOrigin.rfind("/")+1:]
        imageOrVideo = isImageOrVideo(file)
        if imageOrVideo:
            print("\n\nWorking with file "+str(file)+" ("+imageOrVideo+") \n")
            year = whichYear(folderOrigin)
            createFolders(year, imageOrVideo)
            insideImageOrVideoFolder = folderDestination+"/"+imageOrVideo
            insideYearFolder = insideImageOrVideoFolder+"/"+year
            if file not in os.listdir(insideYearFolder):
                shutil.copy(folderOrigin,insideYearFolder)
                print("\n The file "+file+" was copied +\n"+
                "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
            else:
                treatDuplicates(file,folderOrigin,year, imageOrVideo)
                print("\n The file "+file+" was copied +\n"+
                "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
            

    #if it is a folder      
    elif os.path.isdir(folderOrigin):
        folder = folderOrigin[folderOrigin.rfind("/")+1:]
        print("\n ------------------ Working in folder "+ str(folder)+"------------------")
        if os.listdir(folderOrigin): 
            for item in os.listdir(folderOrigin):
                if not any(string in item for string in excluded):
                    pathitem = folderOrigin+"/"+item
                    function(pathitem,folderDestination)
        else:
            print("\n The folder "+str(folder)+ " is empty")
    else:
        print("It is a special file (socket, FIFO, device file)")    


# In[9]:


print("Starting Script...")
print("\n It will copy the files from: \n"
      +"   "+ str(folderOrigin) + "\n to \n"+"   " +str(folderDestination)+"\n \n")

print("\nIt will only work with the following extensions: \n")
print("Videos: "+str(videoExtensions)+"\n")
print("Images: "+str(imageExtensions))
print("\nIt will exclude the following extensions: \n")
print(excluded)




function(folderOrigin,folderDestination)


# In[ ]:




