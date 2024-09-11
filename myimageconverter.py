from fileinput import filename
from PIL import Image, UnidentifiedImageError
from pillow_heif import HeifImagePlugin

import myfuncs as funcs
import my_constants as const


"""
Save file and return the converted file with complete path as passed to it
"""
# @log_decorator
def save_img_file (rgb_im, cnv_img_file_with_path, quality_in=-666) -> str:
    try:
        funcs.log_debug_message (f"{funcs.get_method_name()}::cnv_img_file_with_path [{cnv_img_file_with_path}], quality% [{quality_in}] ...")

        if quality_in == -666:
            rgb_im.save(fp=cnv_img_file_with_path)
        else:
            rgb_im.save(fp=cnv_img_file_with_path, quality=quality_in)

        funcs.log_debug_message (f"{funcs.get_method_name()}::Successfully converted file to [{cnv_img_file_with_path}] ...")
        return cnv_img_file_with_path
    except Exception as e:
        # raise Exception(f"{funcs.get_method_name()}::Error occurred [{e}]")
        raise e


"""
Internal class to handle
"""
class MyImageConverter:
    def convert_to_nonjpeg(self, img_file_with_path, in_ext, cnv_img_file_with_path):
        funcs.log_debug_message (f"{funcs.get_method_name()}::img_file_with_path [{img_file_with_path}], cnv_img_file_with_path [{cnv_img_file_with_path}], quality% [{None}] ...")
        rgb_im = Image.open(img_file_with_path)
        save_img_file(rgb_im, cnv_img_file_with_path, const.DEFAULT_JPEG_QUALITY_IN_PERCENT)

    def convert_to_jpeg(self, img_file_with_path, in_ext, cnv_img_file_with_path):
        funcs.log_debug_message (f"{funcs.get_method_name()}::img_file_with_path [{img_file_with_path}], cnv_img_file_with_path [{cnv_img_file_with_path}], quality% [{const.JPEG_QUALITY_IN_PERCENT}] ...")
        """
        Need to perform one extra step when converting from .png to .jpg
        """
        rgb_im = Image.open(img_file_with_path).convert('RGB')
        save_img_file(rgb_im, cnv_img_file_with_path, const.JPEG_QUALITY_IN_PERCENT)

    # def convert_heic_to_png(self, img_file_with_path, in_ext, cnv_img_file_with_path, target_ext):
    #     funcs.log_debug_message (f"{funcs.get_method_name()}::img_file_with_path [{img_file_with_path}], cnv_img_file_with_path [{cnv_img_file_with_path}], target_ext [{target_ext}], quality% [{const.JPEG_QUALITY_IN_PERCENT}] ...")
    #     import pillow_heif
    #     pillow_heif.register_heif_opener()

    #     if img_file_with_path.endswith(('.heic', '.heif', '.HEIC', '.HEIF')):
    #         img = Image.open(img_file_with_path)
    #         img.format(target_ext.replace('.','')) # type: ignore
    #         # img.save('c:\image_name.png', format('png'))
    #         save_img_file(img, img_file_with_path, in_ext, cnv_img_file_with_path, const.JPEG_QUALITY_IN_PERCENT if target_ext in ["jpg","jpeg"] else const.DEFAULT_JPEG_QUALITY_IN_PERCENT)

    def convert_heic_to_format(self, img_file_with_path, in_ext, cnv_img_file_with_path, target_ext):
        funcs.log_debug_message (f"{funcs.get_method_name()}::img_file_with_path [{img_file_with_path}], cnv_img_file_with_path [{cnv_img_file_with_path}], target_ext [{target_ext}], quality% [{const.JPEG_QUALITY_IN_PERCENT}] ...")
        from wand.image import Image

        supported_extensions=('.heic', '.heif', '.HEIC', '.HEIF')
        if img_file_with_path.endswith(supported_extensions):
            funcs.log_debug_message (f"{funcs.get_method_name()}::img_file_with_path [{img_file_with_path}] endswith [{supported_extensions}] ...")
            """Convert HEIC file to JPG."""
            with Image(filename=img_file_with_path) as img:
                img.format = target_ext.replace('.','')
                """Convert image's """
                if target_ext in ('jpg', 'jpeg', '.jpg', '.jpeg'):
                    funcs.log_debug_message (f"{funcs.get_method_name()}::target_ext [{target_ext}] is in [('jpg', 'jpeg', '.jpg', '.jpeg'] ...")
                    img.convert('RGB')
                    img.compression_quality = const.JPEG_QUALITY_IN_PERCENT

                funcs.log_debug_message (f"{funcs.get_method_name()}::Before calling img.save(filename=cnv_img_file_with_path) with [{cnv_img_file_with_path}] ...")
                img.save(filename=cnv_img_file_with_path)
        else:
            raise funcs.CustomError(f"Source file extension is not in {supported_extensions} - {funcs.get_method_name()}::img_file_with_path [{img_file_with_path}], cnv_img_file_with_path [{cnv_img_file_with_path}], target_ext [{target_ext}], quality% [{const.JPEG_QUALITY_IN_PERCENT}] ...")

