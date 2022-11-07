import os
import shutil
import re
import subprocess
import sys
import datetime
# If the folder path the user puts in the text file doesn't include key words in the path, but the
# path does exist, it give the option for the
# user to continue on if it is correct
def validate(string):
    x = input(f"[y/n] {string}")
    if x == "y":
        return False
    elif x == "n":
        return True
#Ends the program during the validation stage if user inputs "n" during validate functions.
def end(enderror):
    if enderror is True:
        print("Ending Program")
        sys.exit(0)
    else:
        return
#Function finds all directories that the user
def listdirs(rootdir):
    list = []
    for it in os.scandir(rootdir):
        if it.is_dir():
            list.append(it)
    return list
#Function finds the date at the end of each directory in 1ReadytoProcess to then help match it with its xml file in 2MODS
def datefinder(Dirstring):
    xmlnumbers = [float(directory) for directory in re.findall(r'-?\d+\.?\d*', Dirstring)]
    xmlnumbers = str(xmlnumbers)
    xmlnumbers = xmlnumbers.replace("[", "").replace("]", "").strip('.0')
    return xmlnumbers
#def copymanifest(manifest):
def main():
    inputdir = input("Input path to your input file. This should not include the file name and extension: \n")
    inputdir = inputdir.replace("\\", "/")
    inputfile = input("Input file name and extension. Ex. inputfile.txt: \n")
    inputpath = inputdir + "/" + inputfile
    dictionary2 = dict()

    # Splits inputfile parameters so that code can get the variables it needs after the equal sign.
    with open(inputpath) as f:
        contents = f.readlines()
        for line in contents:
            splitline = line.split("=")
            if len(splitline) >= 2:
                splitline[0] = splitline[0].strip()
                splitline[1] = splitline[1].strip()
                dictionary2[splitline[0]] = splitline[1]

    # Gets the year and paths of the directories and files the code needs and formats it into a way python accepts.
    year = dictionary2["year"]
    rootdir = dictionary2["1ReadyToProcess"]
    rootdir = rootdir.replace("\\", "/") + "/" + year
    modpath = dictionary2["2MODS"]
    modpath = modpath.replace("\\", "/") + "/" + year
    processed = dictionary2["3Processed"]
    processed = processed.replace("\\", "/")
    zipdest = dictionary2["4ReadytoLoad"]
    zipdest = zipdest.replace("\\", "/")
    manifest = dictionary2["manifest"]

    # Used for validate function to know if code should be stopped or not.
    error = False

    if os.path.exists(rootdir) is True and os.path.exists(modpath) is True and os.path.exists(
            processed) is True and os.path.exists(zipdest) is True and os.path.exists(manifest) is True:
        print("Passed path check")
        if "1ReadytoProcess" not in str(rootdir):
            error = validate(f"Your path: {rootdir} does not contain 1ReadytoProcess anywhere in it. is this correct")
            end(error)
            print("1ReadytoProccess folder is in correct spot on textfile")
        if error is False and "2MODS" not in str(modpath):
            error = validate(f"Your path: {modpath} does not contain 2MODS anywhere in it. is this correct")
            end(error)
            print("2MODS folder is in correct spot on textfile")
        if error is False and "3Processed" not in str(processed):
            error = validate(f"Your path: {processed} does not contain 3Processed anywhere in it. is this correct")
            end(error)
            print("3Processed folder is in correct spot on textfile")
        if error is False and "4ReadytoLoad" not in str(zipdest):
            error = validate(f"Your path: {zipdest} does not contain 4ReadytoLoad anywhere in it. is this correct")
            end(error)
            print("4ReadytoLoad folder is in correct spot on textfile")
    else:
        if os.path.exists(rootdir) is False:
            print("Your 1ReadytoProcess path is incorrect")
        if os.path.exists(modpath) is False:
            print("Your 2MODS path is incorecct")
        if os.path.exists(processed) is False:
            print("Your 3Processed path is incorrect")
        if os.path.exists(zipdest) is False:
            print("4ReadytoLoad path is incorrect")
        if os.path.exists(manifest) is False:
            print("Your manifest file path is incorrect")
        error = True
        end(error)
    begin = input( f"Before the program begins, please confirm that everything looks correct. Any paths that required a year should be filled in automatically to avoid error.\n"
        f"Year you are working with: {year}\n"
        f"1ReadytoProcess directory path: {rootdir}\n"
        f"2MODS directory path: {modpath}\n"
        f"3Processed directory path: {processed}\n"
        f"4ReadytoLoad directory path: {zipdest} \n"
        f"Do you wish to begin archiving? [y/n]\n")
    if begin == "y":
        os.chdir(zipdest)
        SevenZipath = os.path.join("C:\\Program Files\\7-Zip", "7z.exe")
        directorylist = listdirs(rootdir)
        for x in range(len(directorylist)):
            Dirstring = str(directorylist[x])
            paperdate = datefinder(Dirstring)
            #If the date it receives is less than 8 digits, it adds a 0 at the begining. This is because zero at the start of a number gets removed.
            if len(paperdate) < 8:
                paperdate = "0" + paperdate
            newspaper = '/FSU_Ilsecolonewspaper_' + paperdate + '.xml'
            mod = modpath + newspaper

            #Used to find folder to archive
            readytoprocessfolder = directorylist[x].path.replace("\\","/")

            #zipname gives us the zipname of the file.
            zipname = "FSU_Ilsecolonewspaper_" + paperdate + ".zip"
            #xmlinfolder and manifest in folder checks if these files already exist in the folder it is about to copy/cut them into.  If they are not there, it will proceed to add them.
            xmlinfolder = readytoprocessfolder + newspaper
            manifestinfolder = readytoprocessfolder + '/manifest.ini'

            #readytoprocess moves the directory that it just archived into the 3ReadytoProcess folder. It will not move directories it did not zip.
            # Copies manifest to current directory year
            errorfile = inputdir + "/errorfile_" + year + ".txt"
            if os.path.exists(manifestinfolder) is False:
                shutil.copy(manifest, readytoprocessfolder)
            else:
                print("Manifest file already exists in folder. Skipping step")

            # Moves file in mod folder to current directory list if it isn't there already
            if os.path.exists(xmlinfolder) is False:
                if os.path.exists(mod) is True:
                    shutil.move(mod, readytoprocessfolder)
                    print("Mod FSU_IIsecolonewspaper_" + paperdate + " has been moved")
                else:
                    print("XML file for your this date is not in the MODS folder or the ready to process folder for this date. Script will skip it and add to error log file")
            elif os.path.exists(xmlinfolder) is True:
                print("Your XML file is already in the folder. Skipping this tep")
            zipcheck = zipdest + "/" + zipname
            # Creates zip only if it contains a manifest.ini file and xml file.
            if os.path.exists(zipcheck) is False:
                if os.path.exists(xmlinfolder) and os.path.exists(manifestinfolder):
                    SevenZiparguments = " a " + zipname + " " + readytoprocessfolder + "\\* -mx5"
                    command = SevenZipath + SevenZiparguments
                    subprocess.run(command.replace("/","\\"))
                    print("Zip Complete")
                    #shutil.move(readytoprocessfolder, processed)
                    if x in range(len(directorylist) - 1):
                        nextfile = str(directorylist[x + 1])
                        print("File is complete. Moving to next file. Next file is " + nextfile)
                    else:
                        print("Task complete")
                else:
                    with open(errorfile, 'a') as f:
                        f.write(f'{datetime.datetime.now()}:{readytoprocessfolder} did not zip correctly due to either not having a manifest file or xml file.\n')
            else:
                print(f"The file you are trying to zip for {readytoprocessfolder} has already be zipped. Adding to error log")
                with open(errorfile, 'a') as f:
                    f.write(f'{datetime.datetime.now()}:{readytoprocessfolder} did not zip correctly because it is already zipped and in 4readytoload. Please check if this is correct.\n')

    else:
        sys.exit(0)


if __name__ == "__main__":

    main()
















