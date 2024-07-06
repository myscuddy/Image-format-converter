import os, sys
import logging
import traceback
import datetime
import time
import pathlib

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
    def __init__ (self, _org_file_name_with_path=None, _fn_with_ext=None, _path_to_file=None, _fn_with_path_noext=None, _fn_with_nopath_noext=None, _file_ext=None):
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

    return process_image_file (fno.path_to_file, fno.fn_with_nopath_noext, fno.fn_with_ext, fno.file_ext, output_path, target_ext)


"""
Common method to process single image file, will be called by method that either processes a single image file or multiple files
"""
def process_image_file (path_to_file: str, fn_with_nopath_noext: str, fn_with_ext: str, file_ext: str, output_path: str, target_ext: str) -> str:
    return convert_image_to_format(path_to_file, fn_with_nopath_noext, fn_with_ext, file_ext, output_path, target_ext)


"""
Wrapper method to process multiple image files, will call process_image_file in a loo[]
"""
@log_decorator
def process_multiple_image_files (args) -> int:
    # -- checking non-required arguments
    src_fmt = args.src_fmt
    if src_fmt is None:
        src_fmt = "*.*"

    # -- If no output path is passed, then default to source file's path
    output_path=args.target_path_for_converted_files
    if output_path is None:
        output_path=args.source_path_with_img_files

    # -- if target extension does not startwith '.', then prefix it        
    target_ext=f".{args.target_ext}" if args.target_ext.startswith(".") == False else args.target_ext

    log_info_message (f"Starting conversion of file(s) from [{args.source_path_with_img_files}] with format [{src_fmt}] \
                                to [{output_path}] with format [{target_ext}] ...")

    fileCnt=0
    readpath = pathlib.Path(f"{args.source_path_with_img_files}")
    for file in readpath.rglob(f"{src_fmt}") :
        fno=split_fp_to_parts(file)

        img_file_with_path=f"{fno.path_to_file}{os.path.sep}{fno.fn_with_ext}"
        log_str=f"Processing [{img_file_with_path}] and if it is a file [{os.path.isfile(img_file_with_path)}] ..."

        if os.path.isfile(img_file_with_path):
            fileCnt += 1

            try:
                cnv_image_file_with_path=process_image_file (fno.path_to_file, fno.fn_with_nopath_noext, fno.fn_with_ext, fno.file_ext, output_path, target_ext)
                if cnv_image_file_with_path is not None:
                    log_info_message (f"{log_str} Converted [{img_file_with_path}] to [{cnv_image_file_with_path}] ...")
            except CustomError as ce:
                log_error_message (f"*** ERROR [{str(ce)}] converting file [{file}] ***")
            except UnidentifiedImageError as uie:
                log_error_message (f"*** ERROR [{str(uie)}] converting file [{file}] ***")
            except Exception as ex1:
                raise ex1
        else:
            log_info_message (f"{log_str} Skipped as it is not a File ...")

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
def check_for_dir(dir_name: str) -> None:
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
def check_for_file(file_name: str) -> None:
    return True if os.path.exists(file_name) and os.path.isfile(file_name) else False


"""
"""
# @log_decorator
# def convert_image_to_format (img_file_with_path, in_ext, target_ext):
def convert_image_to_format(path_to_file: str, fn_with_nopath_noext: str, fn_with_ext: str, in_ext: str, output_path: str, target_ext: str) -> str:
    log_debug_message (f"{get_method_name()}::path_to_file [{path_to_file}], fn_with_nopath_noext [{fn_with_nopath_noext}], fn_with_ext [{fn_with_ext}], in_ext [{in_ext}], output_path [{output_path}], target_ext [{target_ext}] ...")
    matched_ext=False
    quality_in=None
    try:
        # Create source file name with full path 
        img_file_with_path=f"{path_to_file}{os.path.sep}{fn_with_ext}"
        if check_for_file(img_file_with_path):
            pass
        else:
            raise CustomError (f"[{img_file_with_path}] is not a valid file!!!")

        # Check if target dir exists, else try to create it
        check_for_dir(output_path)

        # Create target file name with full path 
        cnv_img_file_with_path=f"{output_path}{os.path.sep}{fn_with_nopath_noext}{target_ext}"

        # Compare if file exists in target folder. Therefore possibly making it the same. Then skip
        if img_file_with_path == cnv_img_file_with_path:
            log_warn_message (f"{get_method_name()}::Converted file [{cnv_img_file_with_path}] already exists. Skipping conversion ...")
            return cnv_img_file_with_path

        # Compare if source & target file names are same. Therefore skip
        fn_target_with_ext=f"{fn_with_nopath_noext}{target_ext}"
        if fn_with_ext == fn_target_with_ext:
            log_warn_message (f"{get_method_name()}::Source [{fn_with_ext}] and converted file [{fn_target_with_ext}] have same name+extension. Skipping conversion ...")
            return cnv_img_file_with_path

        # ----------------------------------------------------------------------------------
        # Check if either source format or expected formats are supported before going ahead
        # ----------------------------------------------------------------------------------
        matched_ext=check_if_supported_extension(in_ext, target_ext)

        # Create instance of MyImageConverter class
        mic = MyImageConverter()

        # # Converting an image from PNG, WEBP, JPG, JPEG, JIF formats
        # if in_ext.lower() in ['.png', '.heic', '.heif', ".jpg", ".jpeg", ".jif", ".jfif", ".webp"]:
        #     matched_ext=True

        # This means we could do not handle this file format to convert from
        if matched_ext == False:
            raise CustomError(f"{get_method_name()}::NO SUPPORT for files with format - in_ext [{in_ext}] to target_ext [{target_ext}] ...")
        else:
            """
            Note that in order to convert HEIF and HEIC files to JPEG using Pillow, we need to convert them to the 
            RGB color space. This can result in a loss of some of the advanced features of HEIF and HEIC, such as 
            support for high dynamic range (HDR) and wide color gamut (WCG).
            """
            if in_ext.lower() in [".heif", "heic"]:
                if target_ext.lower() in ["jpeg", "jpg"]:
                    mic.convert_heic_to_jpeg(img_file_with_path, in_ext, cnv_img_file_with_path, target_ext)
                else:
                    mic.convert_heic_to_jpg(img_file_with_path, in_ext, cnv_img_file_with_path, target_ext)
            elif target_ext.lower() in ["jpeg", "jpg"] and in_ext.lower() not in [".heif", "heic"]:
                mic.convert_to_jpeg(img_file_with_path, in_ext, cnv_img_file_with_path)
                # mic.convert_to_jpg(img_file_with_path, in_ext, cnv_img_file_with_path)
            else:
                mic.convert_to_nonjpeg(img_file_with_path, in_ext, cnv_img_file_with_path)

            log_debug_message (f"{get_method_name()}::Successfully converted file [{img_file_with_path}] to [{cnv_img_file_with_path}] ...")
            return cnv_img_file_with_path
    except UnidentifiedImageError as uie:
        raise uie
    except Exception as e:
        # -- send the exception on upwards
        raise e



class MyImageConverter:
    def convert_to_nonjpeg(self, img_file_with_path, in_ext, cnv_img_file_with_path):
        log_debug_message (f"{get_method_name()}::img_file_with_path [{img_file_with_path}], cnv_img_file_with_path [{cnv_img_file_with_path}], quality% [{None}] ...")
        rgb_im = Image.open(img_file_with_path)
        save_img_file(rgb_im, img_file_with_path, in_ext, cnv_img_file_with_path, None)

    def convert_to_jpeg(self, img_file_with_path, in_ext, cnv_img_file_with_path):
        log_debug_message (f"{get_method_name()}::img_file_with_path [{img_file_with_path}], cnv_img_file_with_path [{cnv_img_file_with_path}], quality% [{const.JPEG_QUALITY_IN_PERCENT}] ...")
        """
        Need to perform one extra step when converting from .png to .jpg
        """
        rgb_im = Image.open(img_file_with_path).convert('RGB')
        save_img_file(rgb_im, img_file_with_path, in_ext, cnv_img_file_with_path, const.JPEG_QUALITY_IN_PERCENT)

    def convert_heic_to_format(self, img_file_with_path, in_ext, cnv_img_file_with_path, target_ext):
        log_debug_message (f"{get_method_name()}::img_file_with_path [{img_file_with_path}], cnv_img_file_with_path [{cnv_img_file_with_path}], quality% [{const.JPEG_QUALITY_IN_PERCENT}] ...")
        import pillow_heif
        pillow_heif.register_heif_opener()

        if img_file_with_path.filename.endswith(('.heic', '.heif', '.HEIC', '.HEIF')):
            img = Image.open(img_file_with_path)
            img.format(target_ext.replace('.',''))
            # img.save('c:\image_name.png', format('png'))
            save_img_file(img, img_file_with_path, in_ext, cnv_img_file_with_path, const.JPEG_QUALITY_IN_PERCENT if target_ext in ["jpg","jpeg"] else None)

    def convert_heic_to_format(self, img_file_with_path, in_ext, cnv_img_file_with_path, target_ext):
        log_debug_message (f"{get_method_name()}::img_file_with_path [{img_file_with_path}], cnv_img_file_with_path [{cnv_img_file_with_path}], quality% [{const.JPEG_QUALITY_IN_PERCENT}] ...")
        from wand.image import Image

        if img_file_with_path.filename.endswith(('.heic', '.heif', '.HEIC', '.HEIF')):
            """Convert HEIC file to JPG."""
            with Image(filename=img_file_with_path) as img:
                img.format = target_ext.replace('.','')
                # img.save(filename=jpg_path)
                save_img_file(img, img_file_with_path, in_ext, cnv_img_file_with_path, const.JPEG_QUALITY_IN_PERCENT)


"""
"""
# @log_decorator
def save_img_file (rgb_im, img_file_with_path, in_ext, cnv_img_file_with_path, quality_in=None) -> str:
    try:
        log_debug_message (f"{get_method_name()}::img_file_with_path [{img_file_with_path}], cnv_img_file_with_path [{cnv_img_file_with_path}], quality% [{quality_in}] ...")

        if quality_in == None:
            rgb_im.save(cnv_img_file_with_path)
        else:
            rgb_im.save(cnv_img_file_with_path, quality=quality_in)

        # log_debug_message ("  2...")
        if quality_in == None:
            rgb_im.save(cnv_img_file_with_path)
        else:
            rgb_im.save(cnv_img_file_with_path, quality=quality_in)
        # log_debug_message ("  3...")
        log_debug_message (f"{get_method_name()}::Successfully converted file to [{cnv_img_file_with_path}] ...")
        return cnv_img_file_with_path
    except Exception as e:
        # print(f"Cannot convert {img_file_with_path} to {target_ext}")
        # raise Exception(f"{get_method_name()}::Error occurred [{e}] ====> img_file_with_path [{img_file_with_path}], in_ext [{in_ext}], target_ext [{target_ext}], quality [{quality_in}] -- cnvfile [{cnv_img_file_with_path}] ...")
        raise Exception(f"{get_method_name()}::Error occurred [{e}]")


def open_and_present_image_file (cnv_image_filename: str) -> None:
    cnv_image_file=Image.open(cnv_image_filename)
    print_image_properties (cnv_image_file)
    cnv_image_file.show()


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
def setup_logger():
    # Create custom logger
    logger = logging.getLogger(__name__)

    # Create handler for screen
    s_handler=logging.StreamHandler()
    # Create handler for log file
    f_handler=logging.FileHandler (f"{const.LOG_DIR}/{const.LOG_FILE_NAME}")

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
def log_message(msg_str, log_type='DEBUG') -> None:
    if log_type == logging.DEBUG:
        logging.getLogger(__name__).debug(msg_str)
    elif log_type == logging.WARNING:
        logging.getLogger(__name__).warning(msg_str)
    elif log_type == logging.INFO:
        logging.getLogger(__name__).info(msg_str)
    elif log_type == logging.ERROR:
        logging.getLogger(__name__).error(msg_str)
    elif log_type == logging.CRITICAL:
        logging.getLogger(__name__).critical(msg_str)
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

