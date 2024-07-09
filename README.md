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
### requirements.txt
This script requires the following libraries to be installed.
It can be used as,
[PATH WHERE INSTALLED]\python -m pip install -r .\requirements.txt 

## Script execution mechanism
### Windoze
#### Convert multiple files with following parameters
    [PATH WHERE INSTALLED]\python convert-all-files.py '-source_path_with_img_files' 'C:\\Code\\Python Scripts\\Data_path\\src' '-src_fmt' '*.*' '-target_ext' '.png' '-target_path_for_converted_files' 'C:\\Users\\Sudhir\\Documents\\Code\\Python Scripts\\Data_path\\target'
    OR
    [PATH WHERE INSTALLED]\python convert-all-files.py '-source_path_with_img_files' 'C:\\Code\\Python Scripts\\Data_path\\Data_path\src' '-src_fmt' '*.*' -target_ext' '.png'
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
#### Convert multiple files
    [PATH WHERE INSTALLED]/python convert-all-files.py -source_path_with_img_files '../Data_path/src' -src_fmt '*.*' -target_ext '.png'
    OR
    [PATH WHERE INSTALLED]/python convert-all-files.py -source_path_with_img_files '../Data_path/src' -src_fmt '*.*' -target_path_for_converted_files '../Data_path/target' -target_ext '.png'
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

