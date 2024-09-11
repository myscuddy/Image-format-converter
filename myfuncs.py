import glob
import logging.handlers
import os, sys
import logging
import traceback
import datetime
import time
import pathlib
from xmlrpc.client import boolean

from rich import print as rprint
from rich.pretty import pprint as rpprint
from rich.logging import RichHandler

from functools import wraps

from PIL import Image, UnidentifiedImageError
from pillow_heif import HeifImagePlugin

# -------------------------------------------------------------------------------------------
# Import local library
# -------------------------------------------------------------------------------------------
import my_constants as const

# -------------------------------------------------------------------------------------------
"""
Custom Class to store components of a FileName
# E.g. C:\\p1\\p2\\p3\\GQ7ZuGWXsAAgGt1.jfif
"""
class FileNameObject:
    def __init__ (self, _org_file_name_with_path:str="", _fn_with_ext:str="", _path_to_file:str="", _fn_with_path_noext:str="", _fn_with_nopath_noext:str="", _file_ext:str=""):
        # C:\p1\p2\p3\GQ7ZuGWXsAAgGt1.jfif
        self.org_file_name_with_path = _org_file_name_with_path
        # GQ7ZuGWXsAAgGt1.jfif
        self.fn_with_ext = _fn_with_ext
        # C:\p1\p2\p3\
        self.path_to_file = _path_to_file
        # C:\p1\p2\p3\GQ7ZuGWXsAAgGt1
        self.fn_with_path_noext = _fn_with_path_noext
        # GQ7ZuGWXsAAgGt1
        self.fn_with_nopath_noext = _fn_with_nopath_noext
        # .jfif
        self.file_ext = _file_ext
        # method name, possibly set later when needed
        self.method_name = None

    def add_method_name(self, _method_name):
        self.method_name = _method_name

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


"""
Custom Exception Class
"""
class CustomError (Exception):
    pass


""" The @debug decorator is used to print debug information about a function 
    call, including its arguments and return value. This can be useful for 
    debugging complex functions or finding performance bottlenecks. """
def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed_time=end - start
        log_debug_message (f"[{func.__name__}] called with args [{args}], kwargs[{kwargs}] and completed in {elapsed_time:.6f} secs")
        # print(f"{func.__name__} returned {result}")
        # print(f'{func.__name__} took {end - start:.6f} seconds to complete')
        return result
    return wrapper


"""
Wrapper method to trap exceptions of called functions
"""
def trap_exception(function):
    @wraps(function)
    def wrapped(self, *args, **kwargs):
        result = function(self, *args, **kwargs)
        if not bool(result):
            self.raise_exception()
        return result
    return wrapped



"""
Wrapper method to handle exceptions from within wrapped methods and print it right then and there.
"""
def exception(logger): 
    # logger is the logging object 
    # exception is the decorator objects  
    # that logs every exception into log file 
    def decorator(func): 

        @wraps(func) 
        def wrapper(*args, **kwargs): 
            try: 
                return func(*args, **kwargs) 
              
            except: 
                issue = "exception in "+func.__name__+"\n"
                issue = issue+"-------------------------------------------------------------------------\n" 
                logger.exception(issue) 
            # raise
          
        return wrapper 
    return decorator 


""" The @wraps decorator is used to preserve the metadata of a function or 
    method after it has been decorated. This can be useful for debugging, 
    introspection, and documentation purposes. """
def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # do something before
        result = func(*args, **kwargs)
        # do something after
        return result
    return wrapper


""" The @timeit decorator is used to measure the execution time of a function 
    and print it to the console. This can be useful for profiling your code 
    and finding performance bottlenecks. """
def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'{func.__name__} took {end - start:.6f} seconds to complete')
        return result
    return wrapper


""" If your Python script accidentally terminates and you still want to perform 
    some tasks to save your work, perform cleanup or print a message, then the 
    register decorator is quite handy in this context."""
# @register

"""
When an unexpected event occurs, we might want our code to wait a while, allowing the external system to correct itself and rerun.
Implemented this retry logic inside a python decorator so that we can annotate any function to apply the retry behavior.
"""
import time
from functools import wraps
def retry(max_tries=3, delay_seconds=1):
    def decorator_retry(func):
        @wraps(func)
        def wrapper_retry(*args, **kwargs):
            tries = 0
            while tries < max_tries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    tries += 1
                    if tries == max_tries:
                        raise e
                    time.sleep(delay_seconds)
        return wrapper_retry
    return decorator_retry


"""
Caching function results
"""
def memoize(func):
    cache = {}
    def wrapper(*args):
        if args in cache:
            return cache[args]
        else:
            result = func(*args)
            cache[args] = result
            return result
    return wrapper


"""
The following decorator sends an email whenever the execution of the inner function fails. 
It doesn’t have to be an email notification in your case. You can configure it to send a 
Teams/slack notification.
"""
import smtplib
import traceback
from email.mime.text import MIMEText

def email_on_failure(sender_email, password, recipient_email):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # format the error message and traceback
                err_msg = f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
                
                # create the email message
                message = MIMEText(err_msg)
                message['Subject'] = f"{func.__name__} failed"
                message['From'] = sender_email
                message['To'] = recipient_email
                
                # send the email
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(sender_email, password)
                    smtp.sendmail(sender_email, recipient_email, message.as_string())
                    
                # re-raise the exception
                raise
                
        return wrapper
    
    return decorator


"""
Print image properties as a string
"""
# @log_decorator
# Prints the name of the file, fomat of the file. [Eg- PNG, JPG, GIF, etc.], mode of the file [Eg- RGB, RFBA, CMYK, etc.], 
# Prints size as a width, height tuple (in pixels), width of the image (in pixels), height of the image (in pixels)
def print_image_properties (image) -> None:
    log_info_message(f"Image has following properties => Filename: [{image.filename}], Format: [{image.format}], Mode: [{image.mode}], Size: [{image.size}], Width: [{image.width}], Height: [{image.height}]")


"""
"""
def pretty_print (obj) -> None:
    import prettyprinter as pp1
    # print (f"In {get_method_name()} ... before I call pprint() ...")
    log_info_message(f"{pp1.pprint(obj)}")

    from pprint import pprint
    log_info_message(f"{pprint(obj)}")


"""
Method to split filename with path to its constituent parts
"""
def split_fp_to_parts(filename_with_path) -> FileNameObject:
    fn_with_path_noext, file_ext = os.path.splitext(filename_with_path)
    fn_with_ext=os.path.basename(filename_with_path)
    path_to_file=os.path.dirname(filename_with_path)
    fn_with_nopath_noext=os.path.basename(fn_with_path_noext)

    return FileNameObject(_org_file_name_with_path=filename_with_path, _fn_with_ext=fn_with_ext, _path_to_file=path_to_file, \
                          _fn_with_path_noext=fn_with_path_noext, _fn_with_nopath_noext=fn_with_nopath_noext, _file_ext=file_ext)


"""
Wrapper method to process single image file, will call process_image_file
"""
# @log_decorator
def process_single_image_file(args) -> str:
    fno=split_fp_to_parts(args.source_img_file_with_path)

    # -- If no output path is passed, then default to source file's path
    output_path=args.target_path_for_converted_files
    if output_path is None:
        output_path=fno.path_to_file

    # -- if target extension does not startwith '.', then prefix it       
    target_ext=args.target_ext
    if target_ext.startswith(".") == False:
        target_ext=f".{target_ext}"

    # -- overide & write file is asked
    overide_write=1 if args.overide_write == 1 else 0

    return process_image_file (fno.path_to_file, fno.fn_with_nopath_noext, fno.fn_with_ext, fno.file_ext, output_path, target_ext, overide_write)


"""
Common method to process single image file, will be called by method that either processes a single image file or multiple files
"""
def process_image_file (path_to_file: str, fn_with_nopath_noext: str, fn_with_ext: str, file_ext: str, output_path: str, target_ext: str, overide_write: int) -> str:
    return convert_image_to_format(path_to_file, fn_with_nopath_noext, fn_with_ext, file_ext, output_path, target_ext, overide_write)


"""
Check argument value for True|False|1|0 as possible values, else return Custome Exception
"""
def t_or_f(argval):
    ua = str("" if argval is None else argval).upper()
    if 'TRUE'.startswith(ua):
       return True
    elif 'FALSE'.startswith(ua):
       return False
    elif argval == '1' or argval == 1:
        return True
    elif argval == '0' or argval == 0:
        return False
    else:
       raise CustomError (f"Unknown argument value {argval}")


"""
Create file name with path
"""
def prep_file_with_path(fpath: str, fname: str, file_ext: str) -> str:
    if fname is None and file_ext is None:
        fp = fpath if fpath.endswith(os.path.sep) else fpath+os.path.sep
    elif file_ext is None:
        fp = fpath+fname if fpath.endswith(os.path.sep) else fpath+os.path.sep+fname
    else:
        fp = fpath+fname+file_ext if fpath.endswith(os.path.sep) else fpath+os.path.sep+fname+("" if file_ext is None else file_ext)
    return fp


"""
"""
def prepare_file_ext (file_ext) -> str:
    if file_ext is None:
        file_ext="**/*.*" 
    else:
        if file_ext.startswith("."):
            file_ext = "**/*"+file_ext
        elif file_ext.startswith("**/*"):
            file_ext = file_ext
        elif file_ext.startswith("*"):
            file_ext = "**/"+file_ext
        else:
            raise CustomError (f"Unknown value in file_ext [{file_ext}]")

    return file_ext



"""
Count files in a folder path and do it recursively if requested
"""
@log_decorator
@exception(logging.getLogger(__name__))
def get_file_count(pathname:str, file_ext:str='*.*', do_recursive:bool=False) -> int:
    method_name=get_method_name()
    smsg=f"{method_name}::1::folder_path=[{pathname}], file_ext=[{file_ext}], do_recursive=[{do_recursive}]"
    log_info_message (smsg)

    file_ext=prepare_file_ext(file_ext)
    smsg=f"{method_name}::2::folder_path=[{pathname}], file_ext=[{file_ext}], do_recursive=[{do_recursive}]"

    file_cnt=0
    for file in glob.glob(os.path.join(pathname, file_ext), recursive=do_recursive):
        fn_with_path=os.path.join(pathname, file)
        fno=split_fp_to_parts(fn_with_path)

        print (f"fn_with_path={fn_with_path}, file_ext=[{file_ext}], fno.file_ext=[{fno.file_ext}], const.SUPPORTED_IN_FORMATS=[{list(map(lambda x: x.upper(), const.SUPPORTED_IN_FORMATS))}] ")
        if check_for_file(fn_with_path) and str.upper(fno.file_ext) in list(map(lambda x: x.upper(), const.SUPPORTED_IN_FORMATS)):
            file_cnt+=1

    smsg+=f" - returning with count of [{file_cnt}]."
    log_info_message (smsg)

    return file_cnt


# """
# Count files in a folder path and do it recursively if requested
# """
# @log_decorator
# @exception(logging.getLogger(__name__))
# def count_files_in_dir(folder_path: str, file_name:str = None, file_ext:str = None, do_recursive=False) -> int:
#     method_name=get_method_name()
#     file_name="" if file_name is None else file_name
#     file_ext="" if file_ext is None else file_ext
#     file_ctr=0
#     smsg=f"{method_name}::folder_path=[{folder_path}], file_name=[{file_name}], file_ext=[{file_ext}], do_recursive=[{do_recursive}]"

#     listdirstr = prep_file_with_path(folder_path, None if (file_name is None or file_name=="") else file_name, None) #file_ext)
#     smsg+=f", listdirstr=[{listdirstr}]"
#     log_info_message (smsg)

#     # return get_file_count(folder_path, file_ext, do_recursive)

#     listdir = os.listdir(listdirstr)

#     for fn in listdir:
#         fnwithpath=prep_file_with_path(folder_path, fn, None)
#         fno=split_fp_to_parts(fnwithpath)

#         """
#         if entry is a directory and you are asked to go recursively into the path, then go into the directory and count files in that level 
#         """
#         smsg=f"{method_name}::folder_path=[{folder_path}], fn=[{fn}], fnwithpath=[{fnwithpath}], file_ext=[{file_ext}], "
#         if os.path.isdir(fnwithpath) and do_recursive:
#             smsg+=" [Is A Directory] ..."
#             file_ctr += count_files_in_dir(fnwithpath, file_ext, do_recursive)
#             # file_ctr += get_file_count(fnwithpath, file_ext, do_recursive)
#         else:
#             smsg+=f" fno.file_ext=[{fno.file_ext}] ..."

#         log_debug_message (f"{smsg}")

#         """
#         If a entry is a file then count as one, else use 0 to not count it
#         """
#         if check_for_file(fnwithpath):
#             """ File extension is not passed as filter, take it as file to be counted """
#             if file_ext is None:
#                 file_ctr += 1 
#             else:
#                 """ Compare upper of both file extensions, passed as well of the file and count as expected file if they match or not """
#                 file_ctr += 1 if fno.file_ext == file_ext else 0
#         else:
#             file_ctr += 0 

#     log_debug_message (f"{method_name}::folder_path=[{folder_path}], file_ext=[{file_ext}], do_recursive=[{do_recursive}] - file_ctr [{file_ctr}] ...")
#     return file_ctr


#SDSDSD
# """
# Wrapper method to process multiple image files, will call process_image_file in a loo[]
# """
# @log_decorator
# @exception(logging.getLogger(__name__))
# def process_multiple_image_files (args) -> int:
#     method_name=get_method_name()
#     # -- checking non-required arguments
#     if args.src_ext is None:
#         src_ext = "*.*"
#     else:
#         # -- if target extension does not startwith '.*', then prefix it        
#         src_ext=f"*{args.src_ext}" if args.src_ext.startswith(".") else args.src_ext
#         src_ext=f"{args.src_ext}"  if args.src_ext.startswith("*") else f"*{args.src_ext}"

#     # -- If no output path is passed, then default to source file's path
#     output_path=args.target_path_for_converted_files
#     if output_path is None:
#         output_path=args.source_path_with_img_files

#     # -- if target extension does not startwith '.', then prefix it        
#     target_ext=f".{args.target_ext}" if args.target_ext.startswith(".") == False else args.target_ext

#     log_info_message (f"{method_name}::Starting conversion of file(s) from [{args.source_path_with_img_files}] with format [{args.src_ext}]/[{src_ext}] to [{output_path}] with format [{args.target_ext}]/[{target_ext}] ...")

#     fileCnt=0
#     follow_recursively = t_or_f(args.follow_recursively)

#     # Count the # of files to be processed based on what is passed as argument
#     # file_count=count_files_in_dir(args.source_path_with_img_files, file_ext=args.src_ext, do_recursive=follow_recursively)
#     file_count=get_file_count(args.source_path_with_img_files, file_ext=args.src_ext, do_recursive=follow_recursively)
    
#     log_info_message (f"{method_name}::There are [{file_count}] files with format [{src_ext}] to be processed ...")

#     # SDSDSD
#     # return

#     smsg=f"{method_name}::"
#     smsg1=f"asked to perform recursive read of file(s) [{follow_recursively}] ..."
#     readpath = pathlib.Path(f"{args.source_path_with_img_files}")
#     if args.follow_recursively == 1:
#         smsg=f"{smsg}Being {smsg1}"
#         files_glob = readpath.rglob(f"{src_ext}")
#     else:
#         smsg=f"{smsg}NOT being {smsg1}"
#         files_glob = readpath.glob(f"{src_ext}")
#     # log_debug_message (f"{method_name}::Being asked to perform recursive read of file(s) [{follow_recursively}] ...")
#     log_info_message (f"{method_name}::Being asked to perform recursive read of file(s) [{follow_recursively}] ...")

#     for file in files_glob :
#         fno=split_fp_to_parts(file)
#         log_info_message (f"{method_name}::[{file}] ...")

#         img_file_with_path=f"{fno.path_to_file}{os.path.sep}{fno.fn_with_ext}"
#         isAFile=check_for_file(img_file_with_path)
#         log_str=f"{method_name}::Processing [{img_file_with_path}] - Is a file? = [{isAFile}]"

#         if isAFile:
#             log_str+=" ..."
#             fileCnt += 1

#             overide_write=1 if args.overide_write == 1 else 0
#             try:
#                 cnv_image_file_with_path=process_image_file (fno.path_to_file, fno.fn_with_nopath_noext, fno.fn_with_ext, fno.file_ext, output_path, target_ext, overide_write)
#                 if cnv_image_file_with_path is not None:
#                     log_info_message (f"{method_name}::File [{fileCnt}/{file_count}] :: {log_str} Converted [{img_file_with_path}] to [{cnv_image_file_with_path}] ...")
#             except CustomError as ce:
#                 log_error_message (f"{method_name}::*** ERROR [{str(ce)}] converting file [{file}] ***")
#             except UnidentifiedImageError as uie:
#                 log_error_message (f"{method_name}::*** ERROR [{str(uie)}] converting file [{file}] ***")
#             except Exception as ex1:
#                 raise ex1
#         else:
#             log_str+=". Skipped as it is not a File ..."

#         log_info_message (f"{method_name}::{log_str}")

#     return fileCnt
#SDSDSD


"""
Wrapper method to process multiple image files, will call process_image_file in a loo[]
"""
@log_decorator
@exception(logging.getLogger(__name__))
def process_multiple_image_files (args) -> int:
    method_name=get_method_name()

    # -- If no output path is passed, then default to source file's path
    output_path=args.target_path_for_converted_files
    if output_path is None:
        output_path=args.source_path_with_img_files

    # -- if target extension does not startwith '.', then prefix it        
    target_ext=f".{args.target_ext}" if args.target_ext.startswith(".") == False else args.target_ext

    src_ext=prepare_file_ext(args.src_ext)
    log_info_message (f"{method_name}::Starting conversion of file(s) from [{args.source_path_with_img_files}] with format [{args.src_ext}]/[{src_ext}] to [{output_path}] with format [{args.target_ext}]/[{target_ext}] ...")

    fileCnt=0
    follow_recursively = t_or_f(args.follow_recursively)

    # Count the # of files to be processed based on what is passed as argument
    file_count=get_file_count(args.source_path_with_img_files, file_ext=args.src_ext, do_recursive=follow_recursively)
    
    log_info_message (f"{method_name}::There are [{file_count}] files with format [{args.src_ext}] to be processed ...")

    log_info_message (f"{method_name}::Being asked to perform recursive [{follow_recursively}] read & conversion of [{file_count}] file(s) under [{args.source_path_with_img_files}] with src_ext [{src_ext}] ...")

    # SDSDSD
    # return

    # for file in files_glob :
    for file in glob.glob(os.path.join(args.source_path_with_img_files, src_ext), recursive=follow_recursively):
        fno=split_fp_to_parts(file)
        log_info_message (f"{method_name}::[{file}] ...")

        # create full file name with path and extension of the source file
        img_file_with_path=os.path.join(fno.path_to_file, fno.fn_with_ext)

        #-- only process if a file and file extension is in supported formats to convert from
        isAValidFile=check_for_file(img_file_with_path) and str.upper(fno.file_ext) in list(map(lambda x: x.upper(), const.SUPPORTED_IN_FORMATS))
        log_str=f"{method_name}::Processing [{img_file_with_path}] - Is a Valid file? = [{isAValidFile}]"
        if isAValidFile:
            log_str+=" ..."
            fileCnt += 1

            overide_write=1 if args.overide_write == 1 else 0
            try:
                cnv_image_file_with_path=process_image_file (fno.path_to_file, fno.fn_with_nopath_noext, fno.fn_with_ext, fno.file_ext, output_path, target_ext, overide_write)
                if cnv_image_file_with_path is not None:
                    log_info_message (f"{method_name}::File [{fileCnt}/{file_count}] :: {log_str} Converted [{img_file_with_path}] to [{cnv_image_file_with_path}] ...")
            except CustomError as ce:
                log_error_message (f"{method_name}::*** ERROR [{str(ce)}] converting file [{file}] ***")
            except UnidentifiedImageError as uie:
                log_error_message (f"{method_name}::*** ERROR [{str(uie)}] converting file [{file}] ***")
            except Exception as ex1:
                raise ex1
        else:
            log_str+=". Skipped as it is not a File ..."

        log_info_message (f"{method_name}::{log_str}")

    return fileCnt



"""
# ----------------------------------------------------------------------------------
# Check if either source format or expected formats are supported before going ahead
# ----------------------------------------------------------------------------------
"""
def check_if_supported_extension(in_ext: str, target_ext: str):
    if in_ext.lower() not in const.SUPPORTED_IN_FORMATS:
        raise CustomError (f"{get_method_name()}::UNSUPPORTED file format [{in_ext}] ...")
    if target_ext.lower() in const.UNSUPPORTED_OUT_FORMATS:
        raise CustomError (f"{get_method_name()}::UNSUPPORTED file format [{target_ext}] ...")
    
    return True


"""
Checks if a directory exists and creates it if it doesn't.

Args:
    - dir_name (str): Name of the directory.
Returns:
- None
"""
def create_dir_if_it_does_not_exist(dir_name: str) -> None:
    if os.path.exists(dir_name) and os.path.isdir(dir_name):
        pass
    else:
        os.mkdir(dir_name)
        log_info_message(f"{dir_name} created in the current folder.")


"""
Checks if filename exists and is a file

Args:
    - file_name (str): Name of the file with path.
Returns:
- None
"""
def check_for_file(file_name: str) -> boolean:
    return True if os.path.exists(file_name) and os.path.isfile(file_name) else False


"""
Method that will convert single file of one format into another format
"""
@exception(logging.getLogger(__name__))
def convert_image_to_format(path_to_file: str, fn_with_nopath_noext: str, fn_with_ext: str, in_ext: str, output_path: str, target_ext: str, overide_write: int) -> str:
    log_debug_message (f"{get_method_name()}::path_to_file [{path_to_file}], fn_with_nopath_noext [{fn_with_nopath_noext}], fn_with_ext [{fn_with_ext}], in_ext [{in_ext}], output_path [{output_path}], target_ext [{target_ext}], overide_write [{overide_write}] ...")
    matched_ext=False

    try:
        # Create source file name with full path 
        img_file_with_path=f"{path_to_file}{os.path.sep}{fn_with_ext}"
        if check_for_file(img_file_with_path):
            pass
        else:
            raise CustomError (f"[{img_file_with_path}] is not a valid file!!!")

        # Check if target dir exists, else try to create it
        create_dir_if_it_does_not_exist(output_path)

        # Create target file name with full path 
        cnv_img_file_with_path=f"{output_path}{os.path.sep}{fn_with_nopath_noext}{target_ext}"
        # If target file exists, then log that before continuing ...
        if check_for_file(cnv_img_file_with_path):
            if overide_write==1:
                log_warn_message (f"{get_method_name()}::Target file [{cnv_img_file_with_path}] exists. But continuing as overide_write=[{overide_write}] ...")
            else:
                raise CustomError (f"{get_method_name()}::Target file [{cnv_img_file_with_path}] exists. Skipping ...")

        # Compare if file exists in target folder. Therefore possibly making it the same. Then skip
        if img_file_with_path == cnv_img_file_with_path:
            if overide_write==1:
                log_warn_message (f"{get_method_name()}::Source [{img_file_with_path}] and to be Converted file [{cnv_img_file_with_path}] exist. But continuing as overide_write=[{overide_write}] ...")
            else:
                raise CustomError (f"{get_method_name()}::Source [{img_file_with_path}] and to be Converted file [{cnv_img_file_with_path}] exist. Skipping conversion ...")

        # ----------------------------------------------------------------------------------
        # Check if either source format or expected formats are supported before going ahead
        # ----------------------------------------------------------------------------------
        matched_ext=check_if_supported_extension(in_ext, target_ext)

        # This means we could do not handle this file format to convert from
        if matched_ext == False:
            raise CustomError(f"{get_method_name()}::NO SUPPORT for files with format - in_ext [{in_ext}] to target_ext [{target_ext}] ...")
        else:
            # Create instance of MyImageConverter class
            from myimageconverter import MyImageConverter
            mic = MyImageConverter()

            """
            Note that in order to convert HEIF and HEIC files to JPEG using Pillow, we need to convert them to the 
            RGB color space. This can result in a loss of some of the advanced features of HEIF and HEIC, such as 
            support for high dynamic range (HDR) and wide color gamut (WCG).
            """
            if in_ext.lower() in [".heif", ".heic"]:
                log_debug_message (f"{get_method_name()}::Before call to convert_heic_to_format with img_file_with_path=[{img_file_with_path}], in_ext=[{in_ext}], cnv_img_file_with_path=[{cnv_img_file_with_path}], target_ext=[{target_ext}] ...")
                mic.convert_heic_to_format(img_file_with_path, in_ext, cnv_img_file_with_path, target_ext)
            elif target_ext.lower() in ["jpeg", "jpg"] and in_ext.lower() not in [".heif", "heic"]:
                log_debug_message (f"{get_method_name()}::Before call to convert_to_jpeg with img_file_with_path=[{img_file_with_path}], in_ext=[{in_ext}], cnv_img_file_with_path=[{cnv_img_file_with_path}] ...")
                mic.convert_to_jpeg(img_file_with_path, in_ext, cnv_img_file_with_path)
            else:
                log_debug_message (f"{get_method_name()}::Before ELSE call to convert_to_nonjpeg with img_file_with_path=[{img_file_with_path}], in_ext=[{in_ext}], cnv_img_file_with_path=[{cnv_img_file_with_path}] ...")
                mic.convert_to_nonjpeg(img_file_with_path, in_ext, cnv_img_file_with_path)

            log_debug_message (f"{get_method_name()}::Successfully converted file [{img_file_with_path}] to [{cnv_img_file_with_path}] ...")
            return cnv_img_file_with_path
    except UnidentifiedImageError as uie:
        raise #uie
    except Exception as e:
        # -- send the exception on upwards
        raise #e


def open_and_present_image_file (cnv_image_filename: str) -> None:
    cnv_image_file=Image.open(cnv_image_filename)
    print_image_properties (cnv_image_file)
    cnv_image_file.show()


"""
Return a string containing a date time value formatted with passed format string, else in the "%Y%m%d%T%H%M%S" format
"""
def create_dt_string (fmt="%Y%m%d%T%H%M%S") -> str:
    log_debug_message (f"------ Inside:{get_method_name()} with fmt:[{fmt}]")
    return datetime.datetime.now().strftime(fmt)  #current date and time


"""
Method to return the name of the current executing method
"""
def get_method_name(fmt=None, *args, **kwargs) -> str:
    try:
        lf_code=sys._getframe(1).f_code
        fno = split_fp_to_parts(lf_code.co_filename)
        fno.add_method_name(lf_code.co_name)
        name=f"{fno.fn_with_ext}::{fno.method_name}"
    except Exception as e: #IndexError, TypeError, AttributeError):  #Something went wrong
        name="<unknown due to error>::{e}"

    return f"{name}"


"""
Method to setup logger for the running application
"""
def setup_logger() -> logging.Logger:
    # Create custom logger
    logger = logging.getLogger(__name__)

    # Create handler for screen
    s_handler=logging.StreamHandler()
    # Create handler for log file
    #SDSDSD f_handler=logging.FileHandler (f"{const.LOG_DIR}/{const.LOG_FILE_NAME}")
    f_handler=logging.handlers.RotatingFileHandler(f"{const.LOG_DIR}/{const.LOG_FILE_NAME}", maxBytes=const.LOG_FILE_MAXBYTES) #, backupCount=const.LOG_FILE_BACKUP_COUNT)
    # from concurrent_log_handler import ConcurrentRotatingFileHandler
    # f_handler = ConcurrentRotatingFileHandler(f"{const.LOG_DIR}/{const.LOG_FILE_NAME}", 'a', maxBytes=const.LOG_FILE_MAXBYTES, backupCount=const.LOG_FILE_BACKUP_COUNT)

    # Set default logging level as INFO and can be overridden in case ISDEBUG==1
    # logging.basicConfig(level=logging.INFO, format=const.LOGFILE_ENTRY_FORMAT_STRING, handlers=[RichHandler(rich_tracebacks=True)])
    logging.basicConfig(level=logging.INFO, format=const.LOGFILE_ENTRY_FORMAT_STRING)

    if const.ISDEBUG == 1:
        # Set LOG level according to OVERRIDE in constants
        s_handler.setLevel(const.CONSOLE_LOG_LEVEL)
        f_handler.setLevel(const.LOGFILE_LOG_LEVEL)
    else:
        # Set LOG level according to OVERRIDE in constants
        s_handler.setLevel(logging.ERROR)
        f_handler.setLevel(logging.INFO)

    # Create formatters and add to handlers
    s_handler.setFormatter(logging.Formatter(const.CONSOLE_ENTRY_FORMAT_STRING))
    f_handler.setFormatter(logging.Formatter(const.LOGFILE_ENTRY_FORMAT_STRING))

    # Add handlers to the Logger
    logger.addHandler(s_handler)
    logger.addHandler(f_handler)

    return logger


"""
Method to wrap call to underlying logging with log level (default is DEBUG)
"""
def log_message(msg_str, log_type=logging.DEBUG) -> None:
    if log_type == logging.DEBUG:
        logging.getLogger(__name__).debug(msg_str)
    elif log_type == logging.WARNING:
        logging.getLogger(__name__).warning(msg_str)
    elif log_type == logging.INFO:
        logging.getLogger(__name__).info(msg_str)
    elif log_type == logging.ERROR:
        logging.getLogger(__name__).error(msg_str, exc_info=True)
        # logging.getLogger(__name__).exception(msg_str)
    elif log_type == logging.CRITICAL:
        logging.getLogger(__name__).critical(msg_str, exc_info=True)
        # logging.getLogger(__name__).critical(msg_str, exc_info=sys.exc_info())
    else:
        print(f'{create_dt_string()} - {msg_str}')


"""
Friendly wrapper methods
"""
def log_debug_message (msg_str) -> None:
    log_message(msg_str, logging.DEBUG)

def log_warn_message (msg_str) -> None:
    log_message(msg_str, logging.WARNING)

def log_info_message (msg_str) -> None:
    log_message(msg_str, logging.INFO)

def log_error_message (msg_str) -> None:
    log_message(msg_str, logging.ERROR)

def log_critical_message (msg_str) -> None:
    log_message(msg_str, logging.CRITICAL)

