# -*- coding: utf-8 -*-
"""
Created on Fri May 31 09:29:00 2019

@author: HUANJ126
"""

#Python Connect Linux and download html tables

#package to be used
import pysftp
from bs4 import BeautifulSoup
import csv
import re
#user input ntid, password, study location and file name
myUsername = "huanj126"
myPassword = "XXXXXX"
location="/Volumes/app/cdars/prod/sites/train/prjA000/qc_toolkit/B1234567/saseng/cdisc3_0/table"
#below localdir can be reset
localdir="C:/Users/huanj126/Desktop/test/"



file=[]
myHostname = "cdars.pfizer.com"
cnopts=pysftp.CnOpts()
cnopts.hostkeys=None

with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword,cnopts=cnopts) as sftp:
    print ("Connection succesfully stablished ... ")
    myPassword=""
    # Switch to a remote directory
    sftp.cwd(location)
    filelist = sftp.listdir()
    for filename in filelist:
        filedate = re.search("ad.*\.html$", filename)
        if filedate:
            file.append(filename)        
        
    for file_chil in file:
        localFilePath = localdir+file_chil;
        sftp.get(file_chil, localFilePath)
        
#read and parse html to obtain title and footnote
TOT=[]
for file_chil in file:
    localFilePath = localdir+file_chil;
    with open(localFilePath,"rb") as f:
        page=f.read()
    
    soup=BeautifulSoup(page,"html.parser")
    OUT1={"TOT":file_chil.split(".")[0]+".tot"}
    #title part
    TTL=soup.find('thead').find('tr')
    TTLlst=list(TTL.stripped_strings)
    OUT1["TTLNUM"]=TTLlst[0]
    OUT1["TITLE"]=TTLlst[2]
    #footnote part
    FNTS=soup.find_all('p')
    FNTlst=list(FNTS[2].stripped_strings)
    for FNT in FNTlst:
        OUT1["FNT"]=FNT
        TOT.append(OUT1.copy())
    
#write list to csv
headings =['TITLE', 'TOT', 'TTLNUM', 'FNT']  
with open(localdir+'output.csv', 'w',newline="") as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerow(headings)
    for dic in TOT:             
        csv_output.writerow([dic[col] for index, col in enumerate(headings)])