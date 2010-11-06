 
# need to use os functions
import os
import xbmc, xbmcgui


# Shared resources
BASE_RESOURCE_PATH = xbmc.translatePath( os.path.join( os.getcwd(), "resources" ) )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib\\elementtree" ) )
# append the proper platforms folder to our path, xbox is the same as win32
env = ( os.environ.get( "OS", "win32" ), "win32", )[ os.environ.get( "OS", "win32" ) == "xbox" ]
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "platform_libraries", env ) )


from pysqlite2 import dbapi2 as sqlite
import ElementTree as ET

#Define the paths, SQL etc
videoDB =  xbmc.translatePath("special://profile/Database/MyVideos34.db")


movieFile = "special://profile/Database/watched.xml"

#Define the Confirmation Dialog Box
class MyClass(xbmcgui.Window):

    def getAction(self):
        menuItems = ["Export Watched Data","Import Watched Data"]
        dialog = xbmcgui.Dialog()
        action = dialog.select("Select an action",menuItems)
        return action

    def confirm(self,message,text):
        dialog = xbmcgui.Dialog()
        return dialog.yesno(message,text)

#Create the class instance
mydisplay = MyClass()



#Define the function to query the db and write the export file
def writeExportFile(strSQL,strFileName):
    dbCon = sqlite.connect(videoDB)	
    dbCur = dbCon.cursor()

    dbCur.execute(strSQL)
    
    xmlObj = ET.Element("watched")

    for row in dbCur:
        child = ET.SubElement(xmlObj, "file")
        child.text = row[0]        


    episodeFileObj = open(strFileName, 'w')
    episodeFileObj.write(ET.tostring(xmlObj))
    episodeFileObj.close()


def exportWatched(gui):
    movieSQL = "select strFileName from files where playCount > 0"


    #If the export file exists ask if we should overwrite it
    if os.path.isfile(movieFile):
        if gui.confirm("Overwrite File", "The watched export file exists.  Do you want to overwrite it?"):
            writeExportFile(movieSQL,movieFile)

    else:
        writeExportFile(movieSQL,movieFile)


def importWatched():

    dbCon = sqlite.connect(videoDB)	
    dbCur = dbCon.cursor()

    #Read the movie xml file
    movieFileObj = open(movieFile,'r')
    movieXML = movieFileObj.read()
    watchedXMLObj = ET.XML(movieXML)

    for subelement in watchedXMLObj:
        fileName = subelement.text
        dbCur.execute("UPDATE files SET playCount = 1 WHERE strFilename = ?", (fileName,))


    dbCon.commit()



#///////////////////////////////////////////////////////////////////////////////////////////////




action = mydisplay.getAction();

if action == 0:
    exportWatched(mydisplay)
if action == 1:
    importWatched()




del mydisplay



#/////////////////////////////////////////////////////////////////////////////////////////////







