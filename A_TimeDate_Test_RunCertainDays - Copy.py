# ---------------------------------------------------------------------------
# A_TimeDate_Test_RunCertainDays_Copy.py
# Description: a test script for Brandon Roberts to run and test out logging.
# ---------------------------------------------------------------------------
import arcpy, sys, logging, logging.handlers, os, time, string, inspect, smtplib, datetime
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# NEXT THREE VARIABLES NEEDED FOR EMAIL ERROR EVENTS
MailSendTO = 'brian.bond@yavapai.us'
MailSendFROM ='yavgis@yavapai.us'
SERVER = 'webmail'
GisServer = "ntgisd"
Fullname = os.path.basename(inspect.getfile(inspect.currentframe()))
PyName = os.path.splitext(Fullname)[0]      # Name of the Py script
PyLocation = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

#TODO:Set these variables
#********************************************************
arcpy.env.overwriteOutput = True
LogName = PyName    # Name of the Log Same as PyName for individual log or name this to something else for a continual log
PyFunction = "Weekly script frequency tables on Street Centerline FC, output to file gdb table to see history of attribute changes over time."     #IMPORTANT!!!: Purpose of the script.
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
    if os.path.exists(errlog) == True:
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
def DeleteFCIfExists(InFCName,Data_Type):
    if arcpy.Exists(InFCName):
        arcpy.Delete_management(InFCName,Data_Type); GpMsg()
def fieldExists(dataset, field_name):
    if field_name in [field.name for field in arcpy.ListFields(dataset)]:
        return True
#TODO: Add Local Variables Here
#******************************************************
try:
    currDate = datetime.now().strftime("%m%d%Y")
    print ("\n" + arcpy.GetMessages() + "\n" + currDate)
    dd=datetime.now().day
    print ("\n" + arcpy.GetMessages() + "\n" + str(dd))
    
    if dd == 2 or dd == 15 or dd == 30:
      print ("TODAY IS A TIME TO RUN THIS SCRIPT "  + str(dd))
    else:
      print ("TODAY IS NOT A DAY WHEN THIS SCRIPT WILL BE RUN "  + str(dd))
    sys.exit(0)
      
    # if dd >= 14 <= 16:
      # print ("TODAY IS BETWEEN 14 AND 16 "  + str(dd))
    # else:
      # print ("TODAY IS NOT EITHER 14, 15 OR 16 "  + str(dd))
      # sys.exit(0)
    try:
        Destination_FileGDBName = "Transportation_FrequencyTbls.gdb"
        Destination_Path = "\\\\" + GisServer + "\\gis\\data\\YavapaiCountyData\\Analysis\\"
        Destination_FileGDBOutput = Destination_Path + Destination_FileGDBName
        
        if not arcpy.Exists(Destination_FileGDBOutput):
            # Process: Create File GDB
            PyMsg("Creating New " + Destination_FileGDBName + " File Geodatabase.")
            arcpy.CreateFileGDB_management(Destination_Path, Destination_FileGDBName, "CURRENT"); GpMsg()
        
        #*******************************************************
        DeleteErrLog() #Deletes error log if no errors are present
        PyMsg("***********************************************************")
        PyMsg("***** COMPLETED SCRIPT " + PyFunction)
        PyMsg("***********************************************************")
    except Exception, ex:
        PyMsg("Error while executing script. \n Please see error log. Located at " + errlog)
        logerror.exception(PyName)
        closeLogger()
            # TO EMAIL ERROR TO MailSendTO; YOU MUST DEFINE MailSendTO IN VARIABLES
        SUBJECT = "Error while executing script " + Fullname
        BODYMSG = "Error in " + str.upper(PyFunction) + ".  View error log at " + errlog
        py_mail(BODYMSG, SUBJECT, MailSendTO, MailSendFROM)
finally:
    PyMsg("*****  The current time and date is " + datetime.now().strftime("%m%d%Y"))
