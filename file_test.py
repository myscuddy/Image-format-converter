import sys
import argparse
import logging
import traceback
import pillow_heif
import rich

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
    parser.add_argument('-source_path_with_img_files', required=True, help='Name of source image file with full path')
    parser.add_argument('-file_ext', required=False, help='File extension to filter files under file path')
    parser.add_argument('-do_recursive', type=int, required=False, default=0, help='Should we go recursively down the file path into directories')
    parser.add_argument('-overide_debug', type=int, required=False, default=0, help='Whether to enable/override debug on and set log levels to INFO (most verbose level)')
    parser.add_argument('-help', required=False, help='Help about the script')

    from rich.traceback import install
    rich.traceback.install(show_locals=True)

    errorEncountered=False
    smessage=""
    try :
        args = parser.parse_args()

        do_recursive = funcs.t_or_f(args.do_recursive)
        overide_debug = funcs.t_or_f(args.overide_debug)

        # -- Create custom logger
        logger = funcs.setup_logger()
        if overide_debug:
            const.ISDEBUG = overide_debug
            logger.setLevel(logging.DEBUG) 

        funcs.log_info_message (f"{funcs.get_method_name()}::=================================== Inside 1 ...")
        funcs.log_info_message (f"{funcs.get_method_name()}::[{args.source_path_with_img_files}], [{args.do_recursive}]=[{do_recursive}], [{args.overide_debug}], [{overide_debug}] ...")
        funcs.log_info_message (f"{funcs.get_method_name()}::=================================== Inside 2 ...")

        # if pillow_heif.is_supported(args.source_path_with_img_files):
        #     funcs.log_debug_message (f"{funcs.get_method_name()}::[{args.source_path_with_img_files}] is supported ...")
        #     chek_image(args.source_path_with_img_files)
        #     introspect_image(args.source_path_with_img_files)
        # else:
        #     smsg=f"{funcs.get_method_name()}::[{args.source_path_with_img_files}] is NOT supported ..."
        #     funcs.log_debug_message (smsg)
        #     chek_image(args.source_path_with_img_files)
        #     raise funcs.CustomError(smsg)

        # file_count=funcs.count_files_in_dir(args.source_path_with_img_files, file_ext=args.file_ext, do_recursive=do_recursive)
        file_count=funcs.get_file_count(args.source_path_with_img_files, file_ext=args.file_ext, do_recursive=do_recursive)

        funcs.log_info_message (f"{funcs.get_method_name()}::funcs.count_files_in_dir({args.source_path_with_img_files}, {do_recursive}) returned [{file_count}] entries ...")

    except argparse.ArgumentError as ae:
        errorEncountered=True
        smessage=f"{funcs.get_method_name()}::ArgumentError exception encountered:: *** Error: [{str(ae)}] ***"
    except Exception as e:
        errorEncountered=True
        smessage=f"{funcs.get_method_name()}::Exception encountered:: *** Error: [{str(e)}] evaluating file [{args.source_path_with_img_files}] ***"
        raise e
    finally:
        if errorEncountered:
            funcs.log_error_message (smessage)
        funcs.log_info_message (f"{funcs.get_method_name()}::=================================== Exiting ")


def main2():
    import glob
    import os

    # glob.glob() return a list of file name with specified pathname
    rootpath='/home/sudhir/Downloads/Localsend/2024-Srini-Baylor-MS_Convocation'
    file_ext='.heic' #None #'**/*.*'
    # file_ext=None
    recursive=True
    # recursive=False
    # for file in glob.glob(f'{rootpath}' + '**/*.txt', recursive=True):
    # # for file in glob.glob(f'{rootpath}' + '**/*.heic', recursive=True):
    # for file in glob.glob(os.path.join(rootpath, file_ext), recursive=True):
    #     # print the path name of selected files
    #     print('['+os.path.basename(file)+'] - ['+os.path.join(f'{rootpath}', file)+']')

    file_count=funcs.get_file_count(rootpath, file_ext, recursive)
    print(f"rootpath [{rootpath}], file_ext [{file_ext}], file_count [{file_count}]")


if __name__ == "__main__":
    # sys.exit(main())
    sys.exit(main2())

