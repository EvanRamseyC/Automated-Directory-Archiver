import os
import shutil
import re
import subprocess
import sys
import datetime
import time


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


# Finds date at the end of each directory in 1ReadytoProcess
def datefinder(dirstring):
    xmlnumbers = [float(directory) for directory in re.findall(r'-?\d+\.?\d*', dirstring)]
    xmlnumbers = str(xmlnumbers)
    xmlnumbers = xmlnumbers.replace("[", "").replace("]", "").replace(".0", "")
    return xmlnumbers


def check():
    inputdir = input("Input path to your input file. This should not include the file name and extension: \n")
    inputdir = inputdir.replace("\\", "/")
    inputfile = input("Input file name and extension. Ex. inputfile.txt: \n")
    inputpath = inputdir + "/" + inputfile
    dictionary2 = dict()

    # Splits input file parameters so that code can get the variables it needs after the equal sign.
    with open(inputpath) as f:
        contents = f.readlines()
        for line in contents:
            split_line = line.split("=")
            if len(split_line) >= 2:
                split_line[0] = split_line[0].strip()
                split_line[1] = split_line[1].strip()
                dictionary2[split_line[0]] = split_line[1]

    """Gets the year and paths of the directories and files the code needs and formats it into a way python accepts.
       year variable is added to the directory containing all your mod paths for that year.
       You can remove adding the year variable to certain folders to have more control over what
       folders you want to work with if it follows a different structure. Ultimately though, 
       the structure must have these things:

       -One directory that contains all the subdirectories you want to archive (rootdir)
       -One directory that contains all the mod (xml) files you want to MOVE to its corresponding subdirectory
        you will archive (modpath)
       -One directory where you want your subdirectories to go after successfully archived (processed)
       -One directory where you want your compressed archives to go (zipdest)
       -one manifest file that you want COPIED into each rootdir subdirectory before archiving (manifest)
       -A pattern that you want each archived file to be named by. This script assumes that the archived file will
        be the same name as the mod file inside of it. It finds the mod you want to put into each folder by joining
        together your root of the name you want to archive your directory, then finds the date at the end.
        The assumed date format is MMDDYYYY
       """

    year = dictionary2["year"]
    rootdir = dictionary2["1ReadyToProcess"]
    rootdir = rootdir.replace("\\", "/")
    modpath = dictionary2["2MODS"]
    modpath = modpath.replace("\\", "/")
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
            processed) is True and os.path.exists(zipdest) is True \
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
    begin = input(f"Before the program begins, please confirm that everything looks correct.\nAny paths that required "
                  f"a year should be filled in automatically to avoid error.\n"
                  f"Year you are working with: {year}\n"
                  f"1ReadytoProcess directory path: {rootdir}\n"
                  f"2MODS directory path: {modpath}\n"
                  f"3Processed directory path: {processed}\n"
                  f"4ReadytoLoad directory path: {zipdest} \n"
                  f"Do you wish to begin archiving? [y/n]\n")
    if begin == "y":
        return inputdir, year, rootdir, modpath, processed, zipdest, manifest, zipname_root
    else:
        sys.exit(0)


def main(inputdir, year, rootdir, modpath, processed, zipdest, manifest, zipname_root, error_folder_list, errorcount):
    # Zip output directory
    os.chdir(zipdest)
    # Path to run 7zip commands
    sevenzip_path = os.path.join("C:\\Program Files\\7-Zip", "7z.exe")

    # Creates error file and count each time it writes in error file.
    log = inputdir + "/logs" + year + ".txt"
    errorfile = inputdir + "/error_file_" + year + ".txt"

    fileline = "------------------------------------------------------------------------------------------" \
               "----------------------------------------------------------------------------- \n"

    # Gets directories you will be archiving
    directorylist = listdirs(rootdir)

    for directory_amount in range(len(directorylist)):
        dirstring = str(directorylist[directory_amount])
        if dirstring in error_folder_list:
            continue
        paperdate = datefinder(dirstring)
        # If the date it receives is less than 8 digits,
        # it adds a 0 at the beginning of string to accommodate float.
        if len(paperdate) < 8:
            paperdate = "0" + paperdate

        """The script assumes that the mod file will be the same name as what you want the zip file to be. So it 
        uses the zip name (something that should be consistent for all files) then adds the underscore and the 
        numbers behind it"""

        # Gets the name of the mod file.
        newspaper = '/' + zipname_root + '_' + paperdate + '.xml'
        mod = modpath + newspaper

        # Used to find folder to archive
        readytoprocessfolder = directorylist[directory_amount].path.replace("\\", "/")

        # zipname gives us the zipname of the file.
        zipname = zipname_root + '_' + paperdate + ".zip"
        zipfolder = zipname.replace(".zip", "")

        # xmlinfolder and manifestinfolder creates path for files.
        xmlinfolder = readytoprocessfolder + newspaper
        manifestinfolder = readytoprocessfolder + '/manifest.ini'

        # Copies manifest to current directory year
        if os.path.exists(manifestinfolder) is False:
            shutil.copy(manifest, readytoprocessfolder)
            with open(log, 'a') as f:
                f.write(f'Manifest file successfully copied\n')
            print("Manifest file successfully copied")
        else:
            with open(log, 'a') as f:
                f.write(f'Manifest file already exists in folder. Skipping step\n')
            print("Manifest file already exists in folder. Skipping step")

        # Moves file in mod folder to current directory list if it isn't there already
        if os.path.exists(xmlinfolder) is False:
            if os.path.exists(mod) is True:
                shutil.move(mod, readytoprocessfolder)
                with open(log, 'a') as f:
                    f.write(f"{datetime.datetime.now()}: Mod {zipname_root}_{paperdate} has been moved\n")
                print(f"Mod {zipname_root}_{paperdate} has been moved")
            else:
                with open(log, 'a') as f:
                    f.write(f"{datetime.datetime.now()}: {mod} file for this date is not in the MODS"
                            f" or ready to process folders for this date"
                            f". The script will not archive this until necessary files are in either folder.\n")

                print(f"{mod} file for this date is not in the MODS or ready to process folders for this date."
                      f"The script will not archive this until necessary files are in either folder.")
        elif os.path.exists(xmlinfolder) is True:
            with open(log, 'a') as f:
                f.write(f"{datetime.datetime.now()}: Your XML file is already in the folder. Skipping this step\n")
            print("Your XML file is already in the folder. Skipping this step")

        # Creates zip only if it contains a manifest.ini file and xml file.
        zipcheck = zipdest + "/" + zipname

        # Checks if zip file does not exist
        if os.path.exists(zipcheck) is False:
            if os.path.exists(xmlinfolder) is True and os.path.exists(manifestinfolder) is True:
                with open(log, 'a') as f:
                    f.write(f"{datetime.datetime.now()}: Zipping {zipfolder}\n")

                # Zips the folder and adds to the zip destination folder.
                print(f"Zipping {zipfolder}")
                sevenzip_arguments = " a " + zipname + " " + readytoprocessfolder + "\\* -mx5"
                command = sevenzip_path + sevenzip_arguments
                subprocess.run(command.replace("/", "\\"))
                with open(log, 'a') as f:
                    f.write(f"{datetime.datetime.now()}: Zip {zipname} complete\n")
                print(f"Zip {zipname} complete")

                # When 7zip crashes, paths to folders become false for an unknown reason.
                # This is why the code tests for it.
                if os.path.exists(readytoprocessfolder) is False:
                    # 7zip Crashed, restarts script
                    with open(errorfile, 'a') as f:
                        f.write(f"{datetime.datetime.now()}: 7zip errors occurred in zip process. "
                                f"Please check for {dirstring} in 1ReadyToProcess")
                    with open(log, 'a') as f:
                        f.write(f"{datetime.datetime.now()}: 7zip error occurred for {dirstring}. "
                                f"Continuing code and ignoring this file.")
                    print("7zip error occurred")
                    szip_error_file = dirstring

                    return True, szip_error_file, errorcount

                else:
                    shutil.move(readytoprocessfolder, processed)

                # Folder was successfully archived.
                if directory_amount < len(directorylist) - 1:
                    nextfile = str(directorylist[directory_amount + 1])
                    with open(log, 'a') as f:
                        f.write(f"{datetime.datetime.now()}: Next file is {nextfile}\n")
                    print(f"Archive complete. Next file is {nextfile}")
                else:
                    with open(log, 'a') as f:
                        f.write(f"{datetime.datetime.now()}: Task complete\n")
                    print("Task complete")
            else:
                # folder was not successfully archived due to missing files. You can look in the folder to see, but
                # typically, it is because the XML file is missing since the manifest file is very easy to get.
                with open(errorfile, 'a') as f:
                    f.write(f'{datetime.datetime.now()}: {zipfolder} did not zip correctly'
                            f' due to either not having a manifest file or xml file.\n')
                    errorcount += 1
        else:
            # File already zipped
            with open(log, 'a') as f:
                f.write(f"{datetime.datetime.now()}: The file you are trying to zip for"
                        f" {zipfolder} has already been zipped. "
                        f"Adding to error log\n")
            print(f"The file you are trying to zip for {zipfolder} "
                  f"has already been zipped. Adding to error log.\n")
            with open(errorfile, 'a') as f:
                f.write(f'{datetime.datetime.now()}: {zipfolder} did not zip correctly '
                        f'because it is already zipped and in 4readytoload. Please check if this is correct.\n')
                errorcount += 1
    # Once the code has attempted to zip each file...
    if errorcount == 0:
        with open(errorfile, 'a') as f:
            f.write(f'{datetime.datetime.now()}: All files'
                    f'have been successfully zipped. No issues found\n')
            f.write(fileline)
    elif errorcount > 0:
        with open(log, 'a') as f:
            f.write(f"{datetime.datetime.now()}: Check logs for errors before restarting.\n"
                    f" These files were not zipped due to 7zip crashing:\n {error_folder_list}")
            f.write(fileline)
        with open(errorfile, 'a') as f:
            f.write(fileline)

    return False, None, errorcount


# Does validation of inputs
input_directory, processing_year, rootdirectory, mod_file_path, processed_fold, \
zipdestination, manifest_file, zip_root_name = check()

work_still_to_do = True
if __name__ == "__main__":
    Seven_zip_crash_files = []
    error_number = 0
    while work_still_to_do:
        Seven_zip_crash, error_file, error_number = main(input_directory, processing_year, rootdirectory, mod_file_path,
                                                         processed_fold, zipdestination, manifest_file, zip_root_name,
                                                         Seven_zip_crash_files, error_number)
        if Seven_zip_crash is True:
            Seven_zip_crash_files.append(error_file)
            work_still_to_do = True
            time.sleep(15)
        else:
            # Untested: This code would go back and zip all the files left that did not zip due to 7zip crashing. Then
            # it will end the script regardless of what happens.

            """
            Seven_zip_crash_files = []
            Seven_zip_crash, error_file = main(input_directory, processing_year, rootdirectory, mod_file_path,
                                               processed_fold, zipdestination, manifest_file, zip_root_name,
                                               Seven_zip_crash_files)"""
            work_still_to_do = False
