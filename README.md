Automated Directory Archiver

Under a given year, the program will perform these actions:
1. Locate the subsequent matching xml(mod file) file and move it to the newspaper directory.
2. Copy the manifiest.ini file from a specific directory to the newspaper directory.
3. Archive each newspaper directory after validating that all the files are there.
4. Puts the archive in a directory of choice
5. Move directories that are already zippped to the folder of the users choice.

You need 7zip to run this script. The script assumes that 7z.exe is in your program files folder (the default one).

Inputting Data:
The script uses a textfile where you fill in all required information. 
The script uses '=' as a delimiter in the input file, the user needs to keep it there. The user also shouldn't mess with any of the words that are left of the equal sign
unless the code is changed along with it.
the 'path' is the string of text at the top of your file explorer. Example: C:\Users\evanr\OneDrive\Documents\FSU\Zip_Project. This should be copy and pasted instead of typed out.

When the script runs, you must provide the path to reach the file, then the file name and extension itself. I recommend calling it just inputfile.txt, which you 
can download from here, but you can call it whatever. Since the script uses absolute pathing, you can put it anywhere. Whereever you make your input file, the script will make an error file
if any errors occur.

Values for input file:
The user will put each value after the '='. You can download the template in github called inputfile.txt

Year = "Year you are working with"
ex. 1893

1ReadyToProcess = the path that has all the subdirectories you want to archive in this instance. This path should include the words "1ReadyToProcess" and the year you are working on
Ex. G:\Digitization\CurrentProjects\Il_Secolo\1ReadyToProcess\1893

2MODS should be the copied path that contains the folder that has your xml files. The path should include the keywords "2MODS" and the year you are working in.
Ex. G:\Digitization\CurrentProjects\Il_Secolo\2MODS\1893

3Processed should be the copied path that is the directory you want your finished 1ReadyToProcess folders to move into. This path should include the keyword "3Processed"
Ex. G:\Digitization\CurrentProjects\Il_Secolo\3Processed

4ReadytoLoad is where your archives will appear once finished. This path should include the word "4ReadytoLoad
G:\Digitization\CurrentProjects\Il_Secolo\4ReadytoLoad

ziproot and zip confirmation is the root for what you want the name of the archive to be. The script assumes that the archive needs to be the same as the
2MODS file, so it will include an underscore and the date for each mode to the archive when it is created. The user manually puts in the base, which is everything before the underscore and date. You should receive the name from whoever gives you the project. Your ziproot is also how the script finds the xml file so the script will not work if the base name of the zip file if different than your 2MODS file.
Example. If the zip is supposed to be FSU_IlSecolo_08121893, your ziproot and zip confirmation will be "FSU_IlSecolo. The base name is FSU_IlSecolo because it is before the specific date after the underscore and it is a consistent pattern.


Errors that occur will be placed in an Error text file. The Error file will be in the same directory that your input file is in, and it will be labeled with the year
the user is working on.
Known Issues:

I do not know how the computer handles running a script that effects so many directories since I did not have a large pool to test it on. A workaround for this would be to make a subdirectory in your 1ReadyToProcess directory, put a certain amount of directories inside it, then path the script to that directory specifically. Just make sure the subdirectory you make has no spaces in it. 

The script cannot archive folders if the path to reach it includes any spaces. Example: "C:\Users\evanr\OneDrive\Documents\FSU\Zip_Project" is a valid path.
"C:\Users\evanr\OneDrive\Documents\FSU\Zip Project" is not. This means you must make sure that your 1ReadyToProcess directory's path has no spaces at all.
If a space exists, you must rename the folder with the space first and remove the space.
You cannot use the script if you want to name the archive differently than the xml file should be inside it. The base name of the archive, everything before its specific date at the end of its name, must be the same as the base name of your xml file(everything before its specific date at the end of its name.) Otherwise it will not find any xml files to move, and it will not archive directories that do not have an xml file.
