#!/usr/bin/env python
# coding: utf-8

# In[17]:


#we import the libraries we will use
import glob
import os
import os.path, time
import shutil
import sys
import filecmp

#we sort everything inside our folder by date and we print it to see what do we have inside
def sort_time(to_be_sorted):
    to_be_sorted.sort(key=os.path.getctime)
    print("\n \nThe following files are inside the folder: \n \n - "+  "\n - " .join(to_be_sorted) + "\n")

fileNames = []
def filesNames(allFiles):
    for a in allFiles:
        fileNames.append(a[a.rfind("\\") +1:])

    
#We create a list with all month + year, so if there is 
#any already existent folder with that name, the script does not
#move it
years =[]

for y in range(1995, 2100,1):
    years.append(y)

import calendar
months = []

for num in range(1,13,1):
    month = calendar.month_abbr[num]
    months.append(month)


monthANDyear = []

for m in months:
    for y in years:
        monthANDyear.append(m + ' ' + str(y))    

#Where is the file located ? This will give us the whole path
cwd = os.getcwd()

#Get me all of the files, including the ones inside the folders, but just the ones with the extension defined in formats
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = []
    # Iterate over all the entries
    for entry in listOfFile:
        for k in formats:
            if entry[1:].split(".")[len(entry[1:].split("."))-1] in formats[k]:
            # Create full path
                fullPath = os.path.join(dirName, entry)
                # If entry is a directory then get the list of files in this directory 
                if os.path.isdir(fullPath):
                    allFiles = allFiles + getListOfFiles(fullPath)
                else:
                    allFiles.append(fullPath)

    return allFiles


filesDatesType = {}

#extract the date and define which type of file is it, video or image ?
def giveFileDateType(to_be_extracted):
   
    for file in to_be_extracted:
        predate = time.ctime(os.path.getmtime(file))
        date = predate[4:7] +' '+ predate[20:26]
        uniqueDates.add(date)
        #If the file extension is present in the formats list, then this file will be "video"
        if file[1:].split(".")[len(file[1:].split("."))-1] in formats["video"]:
            filesDatesType.update({file: (date, "video")})
        #Same as before but "image"    
        elif file[1:].split(".")[len(file[1:].split("."))-1] in formats["image"]:
            filesDatesType.update({file: (date, "image")})    
    return(filesDatesType)
            

                
#the following function creates folders
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

    except OSError:
        print ('Error: Creating directory. ' +  directory)   
                

#El objetivo de esto es crear carpetas basado en si es JPG o bien video        
def createFolders(filesDatesType):
    for f in filesDatesType:
        createFolder("./Output/" +filesDatesType[f][0])
        createFolder("./Output/"+filesDatesType[f][0]+"/" +filesDatesType[f][1])  
    print("\n"+ "\n" + "The folders for the dates were created. Inside each folder you will find the folder of the file type, that is to say, videos and/or images")    

def move(filesDatesType):    
    for f in filesDatesType:
        shutil.copy(os.path.realpath(f), os.path.realpath("./Output/" +filesDatesType[f][0] + "/" +filesDatesType[f][1]))
    print("\n" +"The following files were moved: \n")
    for f in filesDatesType:
        print(f[1:].split("\\")[len(f[1:].split("\\"))-1])

#This function will search for files inside folders and folders inside folders
#it will get all files and will copy them in the main folder

notIncluded = []
renamed = []
excluded = ["ipynb","DS"]
def getAllFilesinFolders(path):
    if os.path.isfile(path):
        file = path[path.rfind("/")+1:]
        if file not in os.listdir("."):
            shutil.copy(path,".")
        else:
            fileInMainDir="./"+file
            if filecmp.cmp(path,fileInMainDir):
                notIncluded.append(" - "+file+ "\n") 
            else:
                file2= "c"+file
                
                while file2 in os.listdir("."):
                      file2 = "c"+file2
                shutil.copy(path,"./"+file2)
                renamed.append(" - "+file+" " + "-->"+ " -"+file2+"\n")
            
    elif os.path.isdir(path):
        for item in os.listdir(path):
            if not any(string in item for string in excluded):
                pathitem = path+"/"+item
                getAllFilesinFolders(pathitem)
    else:
        print("It is a special file (socket, FIFO, device file)")


# In[18]:


#which formats need to be checked ?

formats = { "video": ("mpg", "mp4","avi"), "image": ("jpg", "jpeg", "png")}

#Copies all files inside folders to the main folder where the script will worl
getAllFilesinFolders(".")
print("\nThe following files won't be included in the script since they are duplicated, only one of them will be moved.\n")
print("".join(notIncluded)+"\n") 
print("\nThe following files had the same name and they were renamed: \n")
print("".join(renamed)+"\n")

#Gets all the files
allFiles = getListOfFiles(cwd)

#We define the variables that will be used in our functions. They are now empty
uniqueDates = set()

#if the list ist empty, it means there are no files to work on, then we abort the script
if not allFiles:
    sys.exit("\n NO FILES FOUND! Please add files inside the folder. Otherwise what do you actually want to classify ? \n")

filesNames(allFiles)
sort_time(fileNames)    
    
#We extract the date from the files
giveFileDateType(allFiles)


#Creates the dates and file type folders
createFolders(filesDatesType)

#It moves the files to it respective folders
move(filesDatesType)

print(" \n - - - - - - - - - - - - - SCRIP ENDED - - - - - - - - - - - - - ")


# In[ ]:





# In[ ]:




