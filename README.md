Automated Directory Archiver

All projects that follow this structure will work for the script:
       -A year that you are working with
       -One directory that contains all the subdirectories you want to archive for that given year
       -One directory that contains all the mod (XML) files for a year you want to move(cut and paste) to its corresponding subdirectory
        you will archive 
       -One directory where you want your readytoprocess directory to go after successfully archived 
       -One directory where you want your compressed archives to go 
       -one manifest file that you want to copy and paste into each directory
       -A pattern that you want each archived file to be named by. This script assumes that the archived file will
        be the same name as the mod file inside of it.


Under a given year, the program will perform these actions:
1. Locate the subsequent matching XML (mod file) file and move it to the newspaper directory.
2. Copy the manifiest.ini file from a specific directory to the newspaper directory.
3. Archive each newspaper directory after validating that all the files are there.
4. Puts the archive in a directory of choice
5. Move directories that are already zipped to the folder of the user's choice.

You need 7zip to run this script. The script assumes that 7z.exe is in your program files folder (the default one). I also used pycharmer to run the script

Inputting Data:
The script uses a text file where you fill in all required information. 
The script uses '=' as a delimiter in the input file. The user should only add their inputs after the = sign.
the 'path' is the string of text at the top of your file explorer. Example: C:\Users\evanr\OneDrive\Documents\FSU\Zip_Project. This should be copied and pasted instead of typed out.

When the script runs, you must provide the path to reach your input file which you have downloaded. When you run your script, it will also make an error log file in the same folder your input file is in to log any errors that occur.

Values for input file:
The user will put each value after the '='. You can download the template in GitHub called inputfile.txt
Year = "Year you are working with"
ex. 1893

1ReadyToProcess is the path that has all the directories you want to archive in this instance. This path should include the words "1ReadyToProcess" and the year you are working on

Ex. G:\Digitization\CurrentProjects\Il_Secolo\1ReadyToProcess\1893

2MODS is the path to the directory that contains XML files. The path should include the keywords "2MODS" and the year you are working in.
Ex. G:\Digitization\CurrentProjects\Il_Secolo\2MODS\1893

3Processed is the path to the directory you want the finished 1ReadyToProcess folders to move to. The path should include the keyword "3Processed"
Ex. G:\Digitization\CurrentProjects\Il_Secolo\3Processed

4ReadytoLoad is where your archives will appear once finished. This path should include the word "4ReadytoLoad
G:\Digitization\CurrentProjects\Il_Secolo\4ReadytoLoad

ziproot and zip confirmation is the root for what you want the name of the archive to be. The script assumes that the archive needs to be the same as the 2MODS file, so it will include an underscore and the date for each mode to the archive when it is created. The user manually puts in the base name, which is everything before the underscore that has the date after it. 

Your ziproot is also how the script finds the XML file so the script will not work if the base name of the zip file is different than your 2MODS file.
Example. If the zip is supposed to be FSU_IlSecolo_08121893, your ziproot and zip confirmation will be "FSU_IlSecolo. The base name is FSU_IlSecolo because it is before the underscore and the date after, and it is a consistent pattern.

Upon successfully running the script, it creates a log file and an error file in the same place your input file is. When the code is not running, you can look at the log and error file to see what the script did during its runtime and any errors it ran into across the way.  Please look at the error file at the very least before restarting. 


Known Issues:

The script cannot archive folders if the path to reach it includes any spaces. Example: "C:\Users\evanr\OneDrive\Documents\FSU\Zip_Project" is a valid path.
"C:\Users\evanr\OneDrive\Documents\FSU\Zip Project" is not. This means you must make sure that your 1ReadyToProcess directory's path has no spaces at all.
If a space exists, you must rename the folder with the space first and remove the space.

You cannot use the script if you want to name the archive differently than the XML file should be inside it. The base name of the archive, everything before its specific date at the end of its name, must be the same as the base name of your XML file(everything before its specific date at the end of its name.) Otherwise, it will not find any XML files to move, and it will not archive directories that do not have an XML file. The way the code finds these files is by using the date it extrapolates from the 1ReadyToProcess folders and adds it to the root of your ziproot. So if it is off at all, it won't work.


For every 300 directories, 7zip will crash about 5 times which prevents the file from being zipped. This issue has been addressed so that when it does happen, the script will continue and ignore the folders that caused 7zip to crash. This is so that in a single running of the script it can archive a vast majority of the files without having to restart it each time it crashes. When manually run the second time, any file that previously caused an error for 7zip will then be archived correctly. There is a piece of the script that will not run that would theoretically zip error files once it finishes archiving all the others in one go, but it has not been tested because I ran out of folders to archive. 
