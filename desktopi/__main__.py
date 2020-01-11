import argparse
from utils import *

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='sub-command help')

# CHANGE WALLPAPER
parser_wallpaper = subparsers.add_parser('wp')
parser_wallpaper.add_argument('image_path')
parser_wallpaper.set_defaults(func=change_background)

# TIMED WALLPAPER
parser_timed_wallpaper = subparsers.add_parser('time-wp')
parser_timed_wallpaper.add_argument('--image_list', '-i', nargs="*", required=True)
parser_timed_wallpaper.add_argument('--seconds', '-s', required=True, type=int)
parser_timed_wallpaper.set_defaults(func=start_timed_wallpaper)

# Stop Timed Wallpaper
parser_stop_timed_wallpaper = subparsers.add_parser('stop-wp', help='stop-wp help')
parser_stop_timed_wallpaper.set_defaults(func=stop_timed_wallpaper)

# Watermark Image
parser_watermark = subparsers.add_parser('watermark', help="watermark help")
parser_watermark.add_argument('image_path')
parser_watermark.add_argument('text')
parser_watermark.add_argument('--pos', help="Postion of watermark", default="topleft")
parser_watermark.add_argument('--img_frac', '-f', help="Fraction of image width the watermark takes", type=float, default=0.20)
parser_watermark.add_argument('--padding', '-p', help="Padding from the borders", type=int, default=3)
parser_watermark.add_argument('--coords', '-c', nargs=2, help="custom coordinates for watermark", type=float, default=None)
parser_watermark.set_defaults(func=watermark_image)

args = parser.parse_args()
kwargs = {key: value for key, value in vars(args).items()}
del kwargs["func"]
args.func(**kwargs)
