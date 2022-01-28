#################################################################################
# Compare domain service                                                        #
# By: Brandon Roberts                                                           #
# reference documentation for arcpy                                             #
# https://pro.arcgis.com/en/pro-app/2.7/arcpy/data-access/listdomains.htm       #
# reference for askOpenFileName                                                 #
# https://www.programcreek.com/python/example/4281/tkFileDialog.askopenfilename #
#################################################################################

import arcpy
import logging
import os
from tkinter.filedialog import askopenfilename

#VARIABLES
listOfDomaineOne = []
listOfDomaineTwo = []
differingData = []
#creating dictionary where key is domain and value is another dictionary of coded values
#EX: {DOMAIN NAME, {CODEDVALUE KEY, CODED VALUE}}
domainOneDict = {}
domainTwoDict = {}

#for logging/debug NOT IN USE
##baseDirctory = os.path.dirname(os.path.realpath(__file__))
##locationStatement = "This program is being ran from: ", baseDirctory

#logging setup
#logging.basicConfig(filename = "ceckForDifferencesLog.log", filemode = "w", level = logging.DEBUG)
##logging.info("Program started222222222222222222222222222222222")
#would like to use this for selecting compare files, for now it stays out
#filename = askopenfilename()

#domains
domainOne = arcpy.da.ListDomains("X:\E911_Dispatch\VestaMapLocal\Processing\Gisdatahub_yavapai_April2020TEST.gdb")
domainTwo = arcpy.da.ListDomains("X:\E911_Dispatch\VestaMapLocal\Processing\Gisdatahub_yavapai_February2020TEST.gdb")

#loop through domains
#each iteration 'domain' should update to next domain and append to it's list
for domain in domainOne:
    #print("could of slept more")
    print('Name of Domain: {0}'.format(domain.name)) 
    #add to my list for use in checking differences
    listOfDomaineOne.append('{0}'.format(domain.name))
    
for domain in domainTwo:
    #print("forgot my ID card so i cant pee without bothering somebody")
    print('Name of Domain: {0}'.format(domain.name)) 
    #append to list two for checking later
    listOfDomaineTwo.append('{0}'.format(domain.name))

#uncomment me if you want to see lists that are still untouched
##print(listOfDomaineOne)
##print(listOfDomaineTwo)

for domain in domainOne:
    #print("domain name: {0}".format(domain.name))
    domainOneDict[domain.name] = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    if domain.domainType == 'CodedValue':
        coded_values = domain.codedValues
        domainOneDict[domain.name] = coded_values
        ##print(coded_values)
        #for val, desc in coded_values.items():
            #print('{0} : {1}'.format(val, desc))
            
for domain in domainTwo:
    #print("domain name: {0}".format(domain.name))
    domainTwoDict[domain.name] = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    if domain.domainType == 'CodedValue':
        coded_values = domain.codedValues
        domainTwoDict[domain.name] = coded_values
        ##print(coded_values)
        #for val, desc in coded_values.items():
            #print('{0} : {1}'.format(val, desc))

#loops through the bigger list and then for every index it attempts to find it in the smaller list
#if not found then it must differ and gets added to differingData
def compareLists(listOne, listTwo):
    #find bigger list
    if len(listOne) >= len(listTwo):
        biggerList = listOne
        smallerList = listTwo
    else:
        biggerList = listTwo
        smallerList = listOne
        
    #loop through bigger list
    for search in biggerList:
        #loop through smaller list
        #false flag for flagging if the item was found
        found = False
        for find in smallerList:
            if search == find:
                found = True
        #check it not found, if not, add to list
        if found == False:
            differingData.append(search)
    #print differingData list
    print('differing domains: ', differingData)
    
#compare dictionarys
#first find bigger dictionary, this will be outer loop
#will tell if domain not found AND will also tell if two matching domains do not have matching values 
def compareDictionarys(dictOne, dictTwo):
    problemFlag = False
    if len(domainOneDict) >= len(domainTwoDict):
        biggerDict = domainOneDict
        smallerDict = domainTwoDict
    else:
        biggerDict = domainTwoDict
        smallerDict = domainOneDict
    
    #time for the painfull code
    #looping through bigger list first
    for outerKey in biggerDict:
        found = False 
        for innerKey in smallerDict:
            #if found then we must also compare sub dictionarys
            #set found equal to true so it does not set our flag woff
            if outerKey == innerKey:
                found = True
                if biggerDict[outerKey] != smallerDict[innerKey]:
                    problemFlag = True
                    print("Domain names match but coded values differ for domain: ", outerKey)
        if found == False:
            problemFlag = True
            print("domain: ", outerKey, " was not found in both geo databases")
    if problemFlag == False:
        print("There were no differences found in your geoDataBases")
    print("have a good day")

    
#will add a if name == main here eventually but for now this is fine
##compareLists(listOfDomaineOne,listOfDomaineTwo)
compareDictionarys(domainOneDict,domainTwoDict)


#secret
#https://www.bing.com/images/search?view=detailV2&ccid=x2FRyGtS&id=E987C1D3E5071D82A1F87C6863ADE22BDFBC8635&thid=OIP.x2FRyGtS0FU1W9s9y6nUsQHaF7&mediaurl=https%3a%2f%2fc2.staticflickr.com%2f6%2f5491%2f9794993314_96eaa4f013_b.jpg&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fRc76151c86b52d055355bdb3dcba9d4b1%3frik%3dNYa83yvirWNofA%26pid%3dImgRaw&exph=819&expw=1024&q=turtle+with+a+hat+on&simid=608048501711185846&ck=478ED329249172CA75DEAEC33AB60CA8&selectedIndex=3&FORM=IRPRST&ajaxhist=0&ajaxserp=0