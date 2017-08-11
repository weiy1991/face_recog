# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 16:30:53 2017

@author: weiyuan 

@generating the csv file for face_encoding
"""

import csv
import os,sys

#set the dataset path, relatively.
rootDir = "./dataset"
csvName = "face_encoding.csv"

def writedata(lines,log_path):
    if os.path.isfile(log_path):
        os.remove(log_path)
    for line in lines:
        linename = line.split('/')[-2] #get the name of the pic
        with open(log_path, 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([line,linename])
            csvFile.close()

def getFile(rootDir): 
    dirnamepath = []
    dirpicpath = []
    allpath = []
    #get the personal name file path
    dirname = os.listdir(rootDir)
    for listname in dirname: 
        dirnamepath.append(os.path.join(rootDir, listname))
    #print(dirnamepath)
    #get the pic path for every person
    for listpic in dirnamepath: 
        if os.path.isdir(listpic): #check if it is a folder 
            for listpicname in os.listdir(listpic): 
                #print(listpicname)
                dirpicpath.append(os.path.join(listpic, listpicname))
            dirpicpath.sort(key= lambda x:int((x.split('/')[-1])[:-4]))
            # print(dirpicpath)
            # input("pause")
            allpath += dirpicpath
            dirpicpath.clear()
    #return all the pic path
    return allpath

def genFaceCSV(csvName):
    picpath = getFile(rootDir)
    #picpath.sort(key = line.split('/')[-1] )
    #picpath.sort(key= lambda x:int((x.split('/')[-1])[:-4]))
    writedata(picpath,csvName)
    
if __name__ == "__main__":
    if len(sys.argv)==3:
        rootDir = "./"+sys.argv[1]
        csvName = sys.argv[2] + ".csv"
        print(rootDir, csvName)

    genFaceCSV(csvName)
    

    
    
    