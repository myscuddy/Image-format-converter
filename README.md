# Description
This repository "Image-format-converter" contains some code to convert image formats using Python.

Note: There is some handling of .heif and .heic formats but not always working

## Files
### my_constants.py
Contains the constants & parameters that can be changed
### myfuncs.py
Contains methods used
### convert_image.py
Script to convert one file at a time
### convert-all-files.py
Script to convert multiple files at a time
### myimageconvert.py
Contains class and methods to handle image conversion
### file_test.py
Check single image file of format HEIF and introspect it and print out its attributes
### requirements.txt
This script requires the following libraries to be installed.
It can be used as,
[PATH WHERE INSTALLED]\python -m pip install -r .\requirements.txt 

## Create a virtual environment
### On linux you will need to install python3.10-venv where 3.10 is the version of python that is active
sudo apt install python3.10-venv
### Create venv running following command
python3 -m venv ./.venv

THis will create a folder structure like,
=> ls -alrt .venv/
total 24
lrwxrwxrwx 1 [user] [group]    3 Jan 13 23:15 lib64 -> lib
drwxrwxr-x 3 [user] [group] 4096 Jan 13 23:15 lib
drwxrwxr-x 2 [user] [group] 4096 Jan 13 23:15 include
drwxrwxr-x 5 [user] [group] 4096 Jan 13 23:15 ..
drwxrwxr-x 5 [user] [group] 4096 Jan 13 23:15 .
-rw-rw-r-- 1 [user] [group]   71 Jan 13 23:15 pyvenv.cfg
drwxrwxr-x 2 [user] [group] 4096 Jan 13 23:15 bin

#### Install python libraries based on requirements.txt
source .venv/bin/activate
python3 -m pip install -r requirements.txt 

### Upgrade pip
python3 -m pip install --upgrade pip

## Script execution mechanism
### -- Common parameter "-overide_debug" available to override log level to DEBUG
### Windoze
#### Convert multiple files with following parameters
##### Additional optional arguments
###### "-follow_recursively" to force script to recursively search for files with "-src_ext" values
###### "-overide_write" to force overide & write out target file if it exists
    [PATH WHERE INSTALLED]\python convert-all-files.py '-source_path_with_img_files' 'C:\\Code\\Python Scripts\\Data_path\\src' '-src_ext' '*.*' '-target_ext' '.png' '-target_path_for_converted_files' 'C:\\Users\\Sudhir\\Documents\\Code\\Python Scripts\\Data_path\\target'
    OR
    [PATH WHERE INSTALLED]\python convert-all-files.py '-source_path_with_img_files' 'C:\\Code\\Python Scripts\\Data_path\\Data_path\src' '-src_ext' '*.*' -target_ext' '.png'
    OR 
    [PATH WHERE INSTALLED]\python convert-all-files.py will give you help and expected paramters

#### Convert single file
    [PATH WHERE INSTALLED]\python convert_image.py -source_path_with_img_files 'C:\\Code\\Python Scripts\\Data_path\\src' -target_ext '.png'
    OR
    [PATH WHERE INSTALLED]\python convert_image.py -source_path_with_img_files 'IMG_6453.HEIC' -target_ext '.png'
    OR
    [PATH WHERE INSTALLED]\python convert_image.py -source_path_with_img_files 'IMG_6453.HEIC' -target_ext '.png' -target_path_for_converted_files '..\Data_path\target' 
    OR 
    [PATH WHERE INSTALLED]\python convert_image.py will give you help and expected paramters

### Linux
### -- Common parameter "-overide_debug" available to override log level to DEBUG
#### Convert multiple files
##### Additional optional arguments 
###### "-follow_recursively" to force script to recursively search for files with "-src_ext" values
###### "-overide_write" to force overide & write out target file if it exists
    [PATH WHERE INSTALLED]/python convert-all-files.py -source_path_with_img_files '../Data_path/src' -src_ext '*.*' -target_ext '.png'
    OR
    [PATH WHERE INSTALLED]/python convert-all-files.py -source_path_with_img_files '../Data_path/src' -src_ext '*.*' -target_path_for_converted_files '../Data_path/target' -target_ext '.png'
    OR 
    [PATH WHERE INSTALLED]/python convert-all-files.py will give you help and expected paramters

#### Convert single file
    [PATH WHERE INSTALLED]/python convert_image.py -source_path_with_img_files '../Data_path/GQ7ZuGWXsAAgGt1.jfif' -target_ext gif
    OR
    [PATH WHERE INSTALLED]/python convert_image.py -source_path_with_img_files '../Data_path/IMG_6453.HEIC' -target_ext gif
    OR
    [PATH WHERE INSTALLED]/convert_image.py -source_path_with_img_files '../Data_path/GQ7ZuGWXsAAgGt1.jfif' -target_path_for_converted_files '../Data_path/target' -target_ext gif
    OR 
    [PATH WHERE INSTALLED]/convert_image.py will give you help and expected paramters

