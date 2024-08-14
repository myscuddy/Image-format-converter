from ctypes.wintypes import BOOLEAN
from functools import wraps
import glob, sys, os
import argparse
import logging
import traceback
from xmlrpc.client import boolean

import myfuncs as funcs
import my_constants as const

from PIL import Image, UnidentifiedImageError
from pillow_heif import HeifImagePlugin

def main():
    parser=argparse.ArgumentParser(
        exit_on_error=False,
        description='''This script allows for conveting one or more image files in a folder into another format. The source & target 
        folders are passed as arguments into the script.''',
        epilog='''Note: If "follow_recursively" is set to 1 a source folder is passed with or without source extension, remember that this script will perform its 
        conversion in a resursive manner and go through the files in source folder as well those in child folders.'''
    )

    # -- Parse arguments
    parser.add_argument('-source_path_with_img_files', type=str, required=True, help='Full path to source image file(s)')
    parser.add_argument('-src_ext', required=False, type=str, help='Format to filter the source image file(s) with')
    parser.add_argument('-target_path_for_converted_files', type=str, required=False, help='Full path to where converted image file(s) will be written to')
    parser.add_argument('-target_ext', type=str, required=True, help='Format to convert the source image file(s) to')
    parser.add_argument('-follow_recursively', type=int, required=False, default=0, help='Whether script should recursively look for files with "src_ext" under the "source_path_with_img_files" path. Default is False.')
    parser.add_argument('-overide_write', type=int, required=False, default=0, help='Whether to overide & write target file if it exists')
    parser.add_argument('-overide_debug', type=int, required=False, default=0, help='Whether to enable/override debug on and set log levels to INFO (most verbose level)')
    # parser.add_argument('-help', required=False, help='Help about the script')

    from rich.traceback import install
    install(show_locals=True)

    try :
        args = parser.parse_args()

        # -- Create custom logger
        logger = funcs.setup_logger()
        if args.overide_debug == 1:
            const.ISDEBUG = args.overide_debug
            logger.setLevel(logging.DEBUG) 

        funcs.log_info_message (f"=============== Inside [{funcs.get_method_name()}] ===============")

        processed_file_count=funcs.process_multiple_image_files(args)
        funcs.log_info_message (f"Finished conversion of [{processed_file_count}] files from [{args.source_path_with_img_files}] ...")

    except argparse.ArgumentError as ae:
        funcs.log_error_message (f"ERROR ArgumentError exception encountered:: *** Error: [{str(ae)}] ***")
    except Exception as e:
        funcs.log_error_message (f"ERROR converting files from {args.source_path_with_img_files} due to *** Error: [{str(e)}] ***")
    except SystemExit as se:
        funcs.log_error_message (f"ERROR SystemExit exception encountered:: *** Error: [{str(se)}] ***")
    finally:
        funcs.log_info_message (f"=============== Exiting [{funcs.get_method_name()}] ===============")


if __name__ == "__main__":
    sys.exit(main())

