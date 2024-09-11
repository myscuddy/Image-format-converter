from functools import wraps
import glob
import sys
import argparse
import logging
import traceback

import myfuncs as funcs
import my_constants as const

from PIL import Image
from pillow_heif import HeifImagePlugin

# -- Include folders to PATH here


# ----------------------------------------------------
# Starting method
# ----------------------------------------------------
def main():
    parser=argparse.ArgumentParser()

    # -- Parse arguments
    parser.add_argument('-source_img_file_with_path', required=True, help='Name of source image file with full path')
    parser.add_argument('-target_path_for_converted_files', required=False, help='Path to which converted image files will be written to')
    parser.add_argument('-target_ext', required=True, help='Format to convert the passed image file to')
    parser.add_argument('-show_image', required=False, default=0, help='1/0 on whether to show the converted file or not')
    parser.add_argument('-overide_write', type=int, required=False, default=0, help='Whether to overide & write target file if it exists')
    parser.add_argument('-overide_debug', type=int, required=False, default=0, help='Whether to enable/override debug on and set log levels to INFO (most verbose level)')
    parser.add_argument('-help', required=False, help='Help about the script')

    from rich.traceback import install
    install(show_locals=True)

    try :
        args = parser.parse_args()
        method_name = funcs.get_method_name()

        # -- Create custom logger
        logger = funcs.setup_logger()
        if funcs.t_or_f(args.overide_debug):
            # const.ISDEBUG = args.overide_debug
            logger.setLevel(logging.DEBUG) 

        funcs.log_info_message (f"[{method_name}]::=============== Inside ===============")
        cnv_image_file_with_path=funcs.process_single_image_file (args)
        if funcs.t_or_f(args.show_image): 
            funcs.open_and_present_image_file(cnv_image_file_with_path)
        funcs.log_info_message (f"[{method_name}]::Finished conversion of [{args.source_img_file_with_path}] to [{cnv_image_file_with_path}]...")
    except argparse.ArgumentError as ae:
        funcs.log_error_message (f"ERROR ArgumentError exception encountered:: *** Error: [{str(ae)}] ***")
    except SystemExit as se:
        funcs.log_error_message (f"ERROR SystemExit exception encountered:: *** Error: [{str(se)}] ***")
    except Exception as e:
        funcs.log_error_message (f"*** ERROR [{str(e)}] converting file [{args.source_img_file_with_path}] ***")
    finally:
        funcs.log_info_message (f"[{method_name}]::=============== Exiting ===============")


if __name__ == "__main__":
    sys.exit(main())

