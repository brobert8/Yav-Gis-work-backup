#################################################################################
# Compare domain service                                                        #
# By: Brandon Roberts                                                           #
# reference documentation for arcpy                                             #
# https://pro.arcgis.com/en/pro-app/2.7/arcpy/data-access/listdomains.htm       #
# reference for askOpenFileName                                                 #
# https://www.programcreek.com/python/example/4281/tkFileDialog.askopenfilename #
#################################################################################

import arcpy, inspect, logging, os, datetime
from datetime import datetime
#from tkinter.filedialog import askopenfilename


#VARIABLES
#domains
domainOne = arcpy.da.ListDomains("X:\E911_Dispatch\VestaMapLocal\Processing\Gisdatahub_yavapai_April2020TEST.gdb")
domainTwo = arcpy.da.ListDomains("X:\E911_Dispatch\VestaMapLocal\Processing\Gisdatahub_yavapai_February2020TEST.gdb")
#domain list
listOfDomaineOne = []
listOfDomaineTwo = []
differingData = []
#creating dictionary where key is domain and value is another dictionary of coded values
#EX: {DOMAIN NAME, {CODEDVALUE KEY, CODED VALUE}}
domainOneDict = {}
domainTwoDict = {}
#logging variables
currDate = datetime.now().strftime("\n \t %d / %m / %Y \n")
Fullname = os.path.basename(inspect.getfile(inspect.currentframe()))
PyName = os.path.splitext(Fullname)[0]      # Name of the Py script
logName = PyName
logFile = "X:\ArcGis\Python\LogFiles\\" + logName + ".log"
errLog = "X:\ArcGis\Python\ErrorLogFiles\\" + PyName + "_Error.log"
baseDirctory = os.path.dirname(os.path.realpath(__file__))
locationStatement = "This program is being ran from: ", baseDirctory + "\n TIME/DAY: " + currDate
ContinuousLog = True #IMPORTANT: False(delete previous log file) True(continue log file)
if ContinuousLog == False:
    if os.path.exists(logFile)== True:
        os.remove(logFile)
        print ("Deleting existing log file " + logFile + "... Recreating " + logFile)
        print ("Running " + sys.argv[0])
    if os.path.exists(errLog) == True:
        os.remove(errLog)    
else:
    logging.info("... Appending to existing log file..." + logFile )
# Set logger
x = logging.getLogger("logerror")
x.setLevel(logging.DEBUG)
# Creates Error Log
h1 = logging.FileHandler(errLog)
f = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
h1.setFormatter(f)
h1.setLevel(logging.DEBUG)
x.addHandler(h1)
logerror = logging.getLogger("logerror")
#Warning example logerror.warning(Variable + "\n REASON: Reason why it is a warning! \n")

#loop through domains
#each iteration 'domain' should update to next domain and append to it's list
for domain in domainOne:
    #print('Name of Domain: {0}'.format(domain.name)) 
    #add to my list for use in checking differences
    listOfDomaineOne.append('{0}'.format(domain.name))
    
for domain in domainTwo:
    #print('Name of Domain: {0}'.format(domain.name)) 
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
        #print(coded_values)
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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
    #for debug
    print("\n\tHave a good day!\n")

print(currDate)

##compareLists(listOfDomaineOne,listOfDomaineTwo)
compareDictionarys(domainOneDict,domainTwoDict)

#secret
#https://www.bing.com/images/search?view=detailV2&ccid=x2FRyGtS&id=E987C1D3E5071D82A1F87C6863ADE22BDFBC8635&thid=OIP.x2FRyGtS0FU1W9s9y6nUsQHaF7&mediaurl=https%3a%2f%2fc2.staticflickr.com%2f6%2f5491%2f9794993314_96eaa4f013_b.jpg&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fRc76151c86b52d055355bdb3dcba9d4b1%3frik%3dNYa83yvirWNofA%26pid%3dImgRaw&exph=819&expw=1024&q=turtle+with+a+hat+on&simid=608048501711185846&ck=478ED329249172CA75DEAEC33AB60CA8&selectedIndex=3&FORM=IRPRST&ajaxhist=0&ajaxserp=0