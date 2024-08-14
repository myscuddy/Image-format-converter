import sys
import argparse
import logging
import traceback
import pillow_heif

import myfuncs as funcs
import my_constants as const

# ----------------------------------------------------
# Starting method
# ----------------------------------------------------
def chek_image(fp):
    __data = pillow_heif.misc._get_bytes(fp, 12)
    funcs.log_debug_message (f"chek_image :: __data[4:8]: [{__data[4:8]}], pillow_heif.get_file_mimetype(__data): [{pillow_heif.get_file_mimetype(__data)}]")


def introspect_image(fp):
    heif_file = pillow_heif.open_heif(fp, convert_hdr_to_8bit=False)
    funcs.log_debug_message (f"introspect_image :: image size: [{heif_file.size}], image mode: [{heif_file.mode}], \
                                image data length: [{heif_file.data}], image data stride: [{heif_file.stride}]")
                                # image data length: [{len(heif_file.data)}], image data stride: [{heif_file.stride}]")


# def chek_image_pyheif(fp):
#     from PIL import Image
#     import pyheif

#     heif_file = pyheif.read(fp)
#     image = Image.frombytes(
#         heif_file.mode, 
#         heif_file.size, 
#         heif_file.data,
#         "raw",
#         heif_file.mode,
#         heif_file.stride,
#         )
    

def main():
    parser=argparse.ArgumentParser()

    # -- Parse arguments
    parser.add_argument('-source_img_file_with_path', required=True, help='Name of source image file with full path')
    parser.add_argument('-overide_debug', type=int, required=False, default=0, help='Whether to enable/override debug on and set log levels to INFO (most verbose level)')
    parser.add_argument('-help', required=False, help='Help about the script')

    from rich.traceback import install
    install(show_locals=True)

    errorEncountered=False
    smessage=""
    try :
        args = parser.parse_args()

        # -- Create custom logger
        logger = funcs.setup_logger()
        if args.overide_debug == 1:
            const.ISDEBUG = args.overide_debug
            logger.setLevel(logging.DEBUG) 

        funcs.log_info_message (f"=============== Inside [{funcs.get_method_name()}] ===============")

        if pillow_heif.is_supported(args.source_img_file_with_path):
            funcs.log_debug_message (f"{funcs.get_method_name()}::[{args.source_img_file_with_path}] is supported ...")
            chek_image(args.source_img_file_with_path)
            introspect_image(args.source_img_file_with_path)
        else:
            smsg=f"{funcs.get_method_name()}::[{args.source_img_file_with_path}] is NOT supported ..."
            funcs.log_debug_message (smsg)
            chek_image(args.source_img_file_with_path)
            raise funcs.CustomError(smsg)

    except argparse.ArgumentError as ae:
        errorEncountered=True
        smessage=f"ArgumentError exception encountered:: *** Error: [{str(ae)}] ***"
    # except SystemExit as se:
    #     errorEncountered=True
    #     smessage=f"SystemExit exception encountered:: *** Error: [{str(se)}] ***"
    except Exception as e:
        errorEncountered=True
        smessage=f"Exception encountered:: *** Error: [{str(e)}] evaluating file [{args.source_img_file_with_path}] ***"
    finally:
        if errorEncountered:
            funcs.log_error_message (smessage)
        funcs.log_info_message (f"=============== Exiting [{funcs.get_method_name()}] ===============")


if __name__ == "__main__":
    sys.exit(main())

