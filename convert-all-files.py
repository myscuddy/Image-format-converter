from functools import wraps
import glob, sys, os
import argparse
import logging
import traceback

import myfuncs as funcs
import my_constants as const

from PIL import Image, UnidentifiedImageError
from pillow_heif import HeifImagePlugin



def main():
    # -- Create custom logger
    logger = funcs.setup_logger()

    funcs.log_info_message (f"=============== Inside [{funcs.get_method_name()}] ===============")

    parser=argparse.ArgumentParser()

    # -- Parse arguments
    parser.add_argument('-source_path_with_img_files', required=True, help='Full path to source image file(s)')
    parser.add_argument('-src_fmt', required=False, help='Format to filter the source image file(s) with')
    parser.add_argument('-target_path_for_converted_files', required=False, help='Full path to where converted image file(s) will be written to')
    parser.add_argument('-target_ext', required=True, help='Format to convert the source image file(s) to')
    parser.add_argument('-help', required=False, help='Help about the script')

    try :
        args = parser.parse_args()

        processed_file_count=funcs.process_multiple_image_files(args)
        funcs.log_info_message (f"Finished conversion of [{processed_file_count}] files from [{args.source_path_with_img_files}] ...")

    except SystemExit as se:
        funcs.log_error_message (f"ERROR SystemExit exception encountered:: *** Error: [{str(se)}] ***")
    except Exception as e:
        funcs.log_error_message (f"ERROR converting files from {args.source_path_with_img_files} due to *** Error: [{str(e)}] ***")
    finally:
        funcs.log_info_message (f"=============== Exiting [{funcs.get_method_name()}] ===============")


if __name__ == "__main__":
    sys.exit(main())




# --- OLD CODE
# from PIL import Image
# import glob
# for file in glob.glob("images/*.jpg"):
#     image = Image.open(file)
#     image.save(file.replace("jpg", "png"))