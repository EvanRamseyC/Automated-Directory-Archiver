# Secolo-Zip-Automater
While currently called the Secolo zip automater, it actually is now made to function with any project like it. I just don't have a better name for it yet

Under a given year, the program will perform these actions to prepare each directory for achiving.
1. Locate the subsequent matching xml file and move it to the newspaper directory.
2. Copy the manifiest.ini file from a specific directory to the newspaper directory.
3. Archive each newspaper directory after validating that all the files are there.
4. Move directories that are already zippped to the folder of the users choice.

Inputting Data:
The script uses a textfile where you fill in all required information. 
The script uses '=' as a delimiter in the input file, the user needs to keep it there. The user also shouldn't mess with any of the words that are left of the equal sign
unless the code is changed along with it.
the 'path' is the string of text at the top of your file explorer. Example: C:\Users\evanr\OneDrive\Documents\FSU\Zip_Project

When the script runs, you must provide the path to reach the file, then the file name and extension itself. I recommend calling it just inputfile.txt, which you 
can download from here, but you can call it whatever. Since the script uses absolute pathing, you can put it anywhere. 

Values for input file:
The user will put each value after the '='. You can download the template in github called inputfile.txt

The year should be a 4 digit number.

1ReadyToProcess should be the copied path that contains the folders you want to zip eventually. With how the script is made, it automatically includes
the year at the end of the path, so the user should copy the path up to the directory containing all the years, not including the year itself.

2MODS should be the copied path that contains the folder that has your xml files. The script is made to include the year at the end of the path you give it,
so the user should copy the path up to the directory containing all the years, not including the year itself

3Processed should be the copied path that is the directory you want your finished 1ReadyToProcess folders to move into.

4ReadytoLoad is where your archives will appear once finished.

ziproot and zip confirmation is the root for what you want the name of the archive to be. The script assumes that the archive needs to be the same as the
2Mods file, so it will include an underscore and the date for each mode to the archive when it is created. The user manually puts in the base, which is everything before
the underscore and date. You should receive the name from whoever gives you the project. 


Errors that occur will be placed in an Error text file. The Error file will in the same directory that your input file is in, and it will be labeled with the year
the user is working on.
Known Issues:
The script cannot archive folders if the path to reach it includes any spaces. Example: C:\Users\evanr\OneDrive\Documents\FSU\Zip_Project is a valid path.
C:\Users\evanr\OneDrive\Documents\FSU\Zip Project is not. This means you must make sure that your 1ReadyToProcess directory's path has no spaces at all.
If a space exists, you must rename the folder with the space first and remove the space.

The script assumes that your 1ReadyToProcess' and 2MODS' subdirectories will first be years, 
and then inside each year will be the newspaper directories themselves. Example: C:\Users\evanr\OneDrive\Documents\FSU\Zip_Project/1ReadyToProcess/1894.
I originally made the years be a value that is filled in after the original year input to make sure users remain on the same year, but that can be removed for greater
user control on folder paths.
