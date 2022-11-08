import os
import shutil
import re
import subprocess
import sys
import datetime


# Function that lets user input whether to continue or not

def validate(string):
    x = input(f"[y/n] {string}")
    if x == "y":
        return False
    elif x == "n":
        return True


# Ends the program during the validation stage if user inputs "n" during validate functions.


def end(enderror):
    if enderror is True:
        print("Ending Program")
        sys.exit(0)
    else:
        return
# Function finds all directories that the user


def listdirs(rootdir):
    rootdirlist = []
    for it in os.scandir(rootdir):
        if it.is_dir():
            rootdirlist.append(it)
    return rootdirlist


# Function finds the date at the end of each directory in 1ReadytoProcess
# to then help match it with its xml file in 2MODS


def datefinder(dirstring):
    xmlnumbers = [float(directory) for directory in re.findall(r'-?\d+\.?\d*', dirstring)]
    xmlnumbers = str(xmlnumbers)
    xmlnumbers = xmlnumbers.replace("[", "").replace("]", "").strip('.0')
    return xmlnumbers


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
            split_line = line.split("=")
            if len(split_line) >= 2:
                split_line[0] = split_line[0].strip()
                split_line[1] = split_line[1].strip()
                dictionary2[split_line[0]] = split_line[1]

    """Gets the year and paths of the directories and files the code needs and formats it into a way python accepts.
       year variable is added to folders automatically instead of the user including it in their path. I made it 
       this way as an extra check to make sure users don't accidentally mix years. 
       You should keep the year variable if you are remaining consistent for each year, but you can remove it from 
       rootidir and modpath if you want the user to put in the exact path."""
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
    zipname_root = dictionary2["ziproot"]
    zipname_confirm = dictionary2["zip confirmation"]

    # Used for validate function to know if code should be stopped or not.
    error = False

    if os.path.exists(rootdir) is True and os.path.exists(modpath) is True and os.path.exists(
            processed) is True and os.path.exists(zipdest) is True\
            and os.path.exists(manifest) is True and zipname_root == zipname_confirm:
        print("Passed path check")

        """If the folder path the user puts in the text file doesn't include keywords in the path, but the
        path does exist, it gives the option for the user to continue on if it is correct
        Future archiving projects should be organized in a way where these keywords are a part of the file path."""

        if "1ReadyToProcess" not in str(rootdir):
            error = validate(f"Your path: {rootdir} does not contain 1ReadytoProcess anywhere in it. is this correct")
            end(error)
            print("1ReadyToProcess folder is in correct spot on text file")
        if error is False and "2MODS" not in str(modpath):
            error = validate(f"Your path: {modpath} does not contain 2MODS anywhere in it. is this correct")
            end(error)
            print("2MODS folder is in correct spot on text file")
        if error is False and "3Processed" not in str(processed):
            error = validate(f"Your path: {processed} does not contain 3Processed anywhere in it. is this correct")
            end(error)
            print("3Processed folder is in correct spot on text file")
        if error is False and "4ReadytoLoad" not in str(zipdest):
            error = validate(f"Your path: {zipdest} does not contain 4ReadytoLoad anywhere in it. is this correct")
            end(error)
            print("4ReadytoLoad folder is in correct spot on text file")
    else:
        # Prints each path is user inputfile.txt missing
        if os.path.exists(rootdir) is False:
            print("Your 1ReadytoProcess path is incorrect")
        if os.path.exists(modpath) is False:
            print("Your 2MODS path is incorrect")
        if os.path.exists(processed) is False:
            print("Your 3Processed path is incorrect")
        if os.path.exists(zipdest) is False:
            print("4ReadytoLoad path is incorrect")
        if os.path.exists(manifest) is False:
            print("Your manifest file path is incorrect")
        if zipname_root != zipname_confirm:
            print("The name you want to give your zip files do not match")
        error = True
        end(error)
    begin = input(f"Before the program begins, please confirm that everything looks correct.\n Any paths that required "
                  f"a year should be filled in automatically to avoid error.\n"
                  f"Year you are working with: {year}\n"
                  f"1ReadytoProcess directory path: {rootdir}\n"
                  f"2MODS directory path: {modpath}\n"
                  f"3Processed directory path: {processed}\n"
                  f"4ReadytoLoad directory path: {zipdest} \n"
                  f"Do you wish to begin archiving? [y/n]\n")
    if begin == "y":
        # Zip output directory
        os.chdir(zipdest)
        # Path to run 7zip commands
        sevenzip_path = os.path.join("C:\\Program Files\\7-Zip", "7z.exe")

        # Creates error file and count each time it writes in error file.
        errorfile = inputdir + "/errorfile_" + year + ".txt"
        errorcount = 0
        fileline = "------------------------------------------------------------------------ \n"

        # Gets directories you will be archiving
        directorylist = listdirs(rootdir)

        for directory_amount in range(len(directorylist)):
            dirstring = str(directorylist[directory_amount])
            paperdate = datefinder(dirstring)
            # If the date it receives is less than 8 digits,
            # it adds a 0 at the beginning of string to accommodate float.
            if len(paperdate) < 8:
                paperdate = "0" + paperdate
            newspaper = '/' + zipname_root + '_' + paperdate + '.xml'
            mod = modpath + newspaper
            # Used to find folder to archive
            readytoprocessfolder = directorylist[directory_amount].path.replace("\\", "/")

            # zipname gives us the zipname of the file.
            zipname = zipname_root + '_' + paperdate + ".zip"

            # xmlinfolder and manifestinfolder creates path for files.
            xmlinfolder = readytoprocessfolder + newspaper
            manifestinfolder = readytoprocessfolder + '/manifest.ini'

            # Copies manifest to current directory year

            if os.path.exists(manifestinfolder) is False:
                shutil.copy(manifest, readytoprocessfolder)
            else:
                print("Manifest file already exists in folder. Skipping step")

            # Moves file in mod folder to current directory list if it isn't there already
            if os.path.exists(xmlinfolder) is False:
                if os.path.exists(mod) is True:
                    shutil.move(mod, readytoprocessfolder)
                    print(f"Mod {zipname_root}_" + paperdate + " has been moved")
                else:
                    print(mod)
                    print("XML file for your this date is not in the MODS folder or the ready to process folder for "
                          "this date. Script will skip it and add to error log file")
            elif os.path.exists(xmlinfolder) is True:
                print("Your XML file is already in the folder. Skipping this tep")

            # Creates zip only if it contains a manifest.ini file and xml file.
            zipcheck = zipdest + "/" + zipname

            if os.path.exists(zipcheck) is False:
                if os.path.exists(xmlinfolder) is True and os.path.exists(manifestinfolder) is True:
                    incorrect_name = os.path.join(readytoprocessfolder, )
                    correct_name = incorrect_name.replace('*.XML', '.xml')
                    os.rename(incorrect_name, correct_name)
                    sevenzip_arguments = " a " + zipname + " " + readytoprocessfolder + "\\* -mx5"
                    command = sevenzip_path + sevenzip_arguments
                    subprocess.run(command.replace("/", "\\"))
                    print("Zip Complete")
                    shutil.move(readytoprocessfolder, processed)
                    if directory_amount in range(len(directorylist) - 1):
                        nextfile = str(directorylist[directory_amount + 1])
                        print("File is complete. Moving to next file. Next file is " + nextfile)
                    else:
                        print("Task complete")
                else:
                    with open(errorfile, 'a') as f:
                        f.write(f'{datetime.datetime.now()}:{readytoprocessfolder} did not zip correctly'
                                f' due to either not having a manifest file or xml file.\n')
                        errorcount += 1
            else:
                print(f"The file you are trying to zip for {readytoprocessfolder} "
                      f"has already be zipped. Adding to error log")
                with open(errorfile, 'a') as f:
                    f.write(f'{datetime.datetime.now()}:{readytoprocessfolder} did not zip correctly '
                            f'because it is already zipped and in 4readytoload. Please check if this is correct.\n')
                    errorcount += 1
        if errorcount == 0:
            with open(errorfile, 'a') as f:
                f.write(f'{datetime.datetime.now()}:All files for year {year} '
                        f'has been successfully zipped. No issues found')
                f.write(fileline)
        elif errorcount > 0:
            with open(errorfile, 'a') as f:
                f.write(fileline)

    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
