# ---------------------------------------------------------------------------
# YCTemplateWithEmail.py
# Created By: Brian Bond 
# Modified:
# Description: A template python script.
# Modified: 5-13-2021 BB - Updated to be PYTHON 3 compatible.
# ---------------------------------------------------------------------------
import arcpy, sys, logging, logging.handlers, os, time, string, inspect, smtplib
from arcpy import env
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# NEXT THREE VARIABLES NEEDED FOR EMAIL ERROR EVENTS
MailSendTO = 'yavgis@yavapai.us'  # CHANGE TO WHOM YOU WANT ANY EMAILS SENT TO
MailSendFROM ='yavgis@yavapai.us'
SERVER = 'relaymail'  # NEW CLOUD EXCHANGE SERVER 4/2020
GisServer = "ntgis"
Fullname = os.path.basename(inspect.getfile(inspect.currentframe()))
PyName = os.path.splitext(Fullname)[0]      # Name of the Py script
PyLocation = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

#TODO:Set these variables
#********************************************************
LogName = PyName    # Name of the Log Same as PyName for individual log or name this to something else for a continual log
PyFunction = "This note is from the template script (YCTemplate.py) if you see this in a production script than you forgot to set a purpose"     #IMPORTANT!!!: Purpose of the script.
ContinuousLog = False    #IMPORTANT!!!: Set to true for continual log file, False to delete existing log    
#********************************************************
# Defining Log files
errlog = "\\\\" + GisServer + "\\GIS\ArcGIS\Python\ErrorLogFiles\\" + PyName + "_Error.Log"  
logFile = "\\\\" + GisServer + "\\GIS\ArcGIS\Python\LogFiles\\" + LogName + ".log" 
# Removes Log File
if ContinuousLog == False:
    if os.path.exists(logFile)== True:
        os.remove(logFile)
        print ("Deleting existing log file " + logFile + "... Recreating " + logFile)
        print ("Running " + sys.argv[0])
    if os.path.exists(errlog)== True:
        os.remove(errlog)
else:
    print ("... Appending to existing log file..." + logFile )
# Set logger
x = logging.getLogger("logerror")
x.setLevel(logging.DEBUG)
# Creates Error Log
h1 = logging.FileHandler(errlog)
f = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
h1.setFormatter(f)
h1.setLevel(logging.DEBUG)
x.addHandler(h1)
logerror = logging.getLogger("logerror")
#Warning example logerror.warning(Variable + "\n REASON: Reason why it is a warning! \n")
def DeleteErrLog(): #Deletes error log if no errors are present
    closeLogger()
    if os.path.exists(errlog):
        if os.path.getsize(errlog) == 0:
            print ("No errors were found, removing" + errlog)
            os.remove(errlog)
        else:
            print ("Errors were found in the errlog. And " + errlog + "s size is "),
            print (os.path.getsize(errlog)),
            print ("bytes.")
def closeLogger():
    h1.close()
    h1.flush()
def GpMsg():
    #v3 compliance new code
    mMsg = "\n" + arcpy.GetMessages() + "\n";
    arcpy.AddMessage(mMsg);
    with open(logFile, "a") as f:
        f.write(arcpy.GetMessages() + "\n")
def PyMsg(msg):
    #v3 compliance new code
    mTxt ="\n{} - {}".format(msg,time.ctime());
    arcpy.AddMessage(mTxt)
    with open(logFile, "a") as f:
        f.write("\n{} - {}".format(msg,time.ctime()))
def DeleteIfExists(objectName):
    if arcpy.Exists(objectName):
        arcpy.Delete_management(objectName); GpMsg()
def py_mail(bmsg, subject, TO, FROM, CC=''):
    global errMsg
    try:
        import smtplib
        from email.mime.text import MIMEText as text
        server = smtplib.SMTP(SERVER)
        if type(TO) == string:
            modTo = TO
        elif type(TO) == list:
            modTo = ','.join(TO)
        modCC = ','.join(CC)
        msg = text(bmsg)
        msg['Subject'] = subject
        msg['From'] = FROM
        msg['To'] = modTo
        msg['Cc'] = modCC
        #  The actual sending of the e-mail
        server.sendmail(FROM, modTo, msg.as_string())
        server.quit()
    except Exception:
        pTxt = "\npy_mail() Error: while executing script: {}\n".format(LogName)
        pTxt += "{}".format(ex)
        PyMsg(pTxt)
        errMsg += pTxt
        logerror.exception(PyName)
        closeLogger()
def asciiConvert():
    L = [84, 111, 112, 111, 108, 105, 110, 101]
    mystring = ''.join(chr(i) for i in L)
    return mystring
#TODO: Add Local Variables Here
#******************************************************
# Local variables...
## DATABASE TARGET; P=PRODUCTION, PWeb=DMZ14PRODUCTION, P16=SQL16PRODUCTION,T=TEST, D=DEVELOPMENT
ActiveGISDBType = "P"
ActiveDBOwner = "_missdeadm_"
ActiveDBName = "yavgis"
ConnString = "\\\\" + GisServer + "\\gis\\ArcGis\\ArcCatalog_Connections\\"
if ActiveGISDBType == "P":
    ActiveGISDBName = "ntsql14p"
    ActiveDBUser = "ScriptConnections\\" + ActiveGISDBName + ActiveDBOwner + ActiveDBName + ".sde"
if ActiveGISDBType == "PWeb":
    ActiveGISDBName = "ntdmzsql14p"
    ActiveDBName = "webgis"
    ActiveDBUser = "ScriptConnections\\" + ActiveGISDBName + ActiveDBOwner + ActiveDBName + ".sde"
if ActiveGISDBType == "P16":
    ActiveGISDBName = "ntsql16p"
    ActiveDBUser = "ScriptConnections\\" + ActiveGISDBName + ActiveDBOwner + ActiveDBName + ".sde"
if ActiveGISDBType == "T":
    ActiveGISDBName = "ntsql14Test"
    ActiveDBUser = "TestConnections\\" + ActiveGISDBName + ActiveDBOwner + ActiveDBName + ".sde"
elif ActiveGISDBType == "D":
    ActiveGISDBName = "ntsql14Devl"
    ActiveDBUser = "DevlConnections\\" + ActiveGISDBName + ActiveDBOwner + ActiveDBName + ".sde"
ActiveFullDBCon = ConnString + ActiveDBUser
SUBJECT = "Python error occurred in " + PyName
BODYMSG = "Auto generated Message. Python script error occurred. Review error log "  + errlog










#******************************************************
try:
    PyMsg("***********************************************************")
    PyMsg("*****  STARTING TO UPDATE " + PyFunction)
    PyMsg("*****  I am located at " + PyLocation)
    PyMsg("*****  The current time and date is " + datetime.now().strftime("%I:%M%p on %B %d, %Y"))
    PyMsg("***********************************************************")
    
    #TODO: Add code to run here
    #******************************************************
    ## FOR YOUR USE IF NEEDED - TEMPLATE TO CREATE POSTPROCESSING FILE GEODATABASE IF IT DOES NOT EXIST
    # if not arcpy.Exists(Temp_YourFileGDBNameHere):
        # # Process: Create File GDB
        # PyMsg("Creating New " + Temp_YourFileGDBNameHere + " File Geodatabase.")
        # arcpy.CreateFileGDB_management("\\\\" + GisServer + "\\gis\\\ArcGISPostProcess", "YourFileGDBNameHere.gdb", "CURRENT"); GpMsg()
    ## END OF TEMPLATE TO CREATE POSTPROCESSING FILE GEODATABASE IF IT DOES NOT EXIST
    
    ## FOR YOUR USE IF NEEDED -TEMPLATE TO DELETE FEATURE CLASS IN A FILE GEODATABASE IF EXIST
    # if arcpy.Exists(FileGDBOutput + "\\YourFeatureClassNameHere"):
        # # Process: Delete
        # arcpy.Delete_management(FileGDBOutput + "\\YourFeatureClassNameHere", "FeatureClass"); GpMsg()
    ## END OF TEMPLATE TO DELETE FEATURE CLASS IN A FILE GEODATABASE IF EXIST
    
    ## FOR YOUR USE IF NEEDED -TEMPLATE TO TEST SCHEMA LOCK ON FINAL OUTPUT FEATURE CLASS
    # if arcpy.TestSchemaLock(YourFeatureClassNameHere) = :
        # PyMsg("* Feature class " + YourFeatureClassNameHere + " is locked at this time *")
        # logerror.exception("* Feature class " + YourFeatureClassNameHere + " is locked at this time *")
        # sys.exit(1)
    # else:
        ## RUN YOUR SCRIPT BECAUSE THE FINAL FEATURE CLASS IS NOT LOCKED
    ## END OF TEMPLATE TO TEST SCHEMA LOCK ON FINAL OUTPUT FEATURE CLASS
    
    ## FOR YOUR USE IF NEEDED -TEMPLATE TO ADD RUNDATE FIELD AND CALCUATE IT TO IDENTIFY WHEN OUTPUT FEATURE CLASS WAS CREATED.
    # # Process: Add Field
    # arcpy.AddField_management({YOUR_FEATURE_CLASS_NAME_HERE}, "RunDate", "DATE", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""); GpMsg()
       
    # # Process: Calculate Field
    # arcpy.CalculateField_management({YOUR_FEATURE_CLASS_NAME_HERE}, "RunDate", "datetime.datetime.now( )", "PYTHON_9.3", ""); GpMsg()## END OF TEMPLATE TO ADD RUNDATE FIELD AND CALCUATE IT TO IDENTIFY WHEN OUTPUT FEATURE CLASS WAS CREATED.
    
    
    
    
    
    #*******************************************************
    DeleteErrLog() #Deletes error log if no errors are present
    PyMsg("***********************************************************")
    PyMsg("***** COMPLETED SCRIPT " + PyFunction)
    PyMsg("***********************************************************")
except Exception as ex:
    PyMsg("Error while executing script. Error description that occured: " + str(ex) + ". Error occured at " + datetime.now().strftime("%I:%M%p") + " \nPlease see error log. Located at " + errlog)
    logerror.exception(PyName)
    closeLogger()
    # Prepare actual message
    py_mail(BODYMSG, SUBJECT, MailSendTO, MailSendFROM)