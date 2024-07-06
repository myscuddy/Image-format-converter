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
    # -- Create custom logger
    logger = funcs.setup_logger()

    funcs.log_info_message (f"=============== Inside [{funcs.get_method_name()}] ===============")

    parser=argparse.ArgumentParser()

    # -- Parse arguments
    parser.add_argument('-source_img_file_with_path', required=True, help='Name of source image file with full path')
    parser.add_argument('-target_ext', required=True, help='Format to convert the passed image file to')
    parser.add_argument('-target_path_for_converted_files', required=False, help='Path to which converted image files will be written to')
    parser.add_argument('-help', required=False, help='Help about the script')

    from rich.traceback import install
    install(show_locals=True)

    try :
        args = parser.parse_args()

        cnv_image_file_with_path=funcs.process_single_image_file (args)
        funcs.open_and_present_image_file(cnv_image_file_with_path)
        funcs.log_info_message (f"Finished conversion of [{args.source_img_file_with_path}] to [{cnv_image_file_with_path}]...")
    # except funcs.CustomError as ce:
    #     funcs.log_error_message (f"*** ERROR [{str(ce)}] converting file [{args.source_img_file_with_path}] ***")
    except SystemExit as se:
        funcs.log_error_message (f"ERROR SystemExit exception encountered:: *** Error: [{str(se)}] ***")
    except Exception as e:
        funcs.log_error_message (f"*** ERROR [{str(e)}] converting file [{args.source_img_file_with_path}] ***")
    finally:
        funcs.log_info_message (f"=============== Exiting [{funcs.get_method_name()}] ===============")


if __name__ == "__main__":
    sys.exit(main())

