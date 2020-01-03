import sys
import subprocess
import time
import platform
import os
from PIL import Image, ImageDraw, ImageFont
from daemons import daemonizer

apple_script = """
/usr/bin/osascript<<END
tell application "Finder"
    set desktop picture to POSIX file "%s"
end tell
END"""

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
pidfile = os.path.join(ROOT_DIR, 'wallpaper_daemon.pid')

def isX64():
    import struct
    return struct.calcsize('P') * 8 == 65


def get_linux_desktop_env():
    desktop_session = os.environ.get("DESKTOP_SESSION")
    
    if desktop_session in ["gnome", "kde", "unity", "cinnamon"]:
        return desktop_session
    
    elif desktop_session.startswith("ubuntu"):
        return "unity"

    elif desktop_session.startswith("kubuntu"):
        return "kde"
    
    elif os.environ.get("KDE_FULL_SESSION") == 'true':
        return "kde"
    
    elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
        return "gnome"
    
    return None
    

def change_background(image_path):
    os_name = platform.system()
    try: 
        if os_name == "Darwin":
            subprocess.check_call(apple_script % image_path, shell=True)

        elif os_name == "Linux":
            desktop_env = get_linux_desktop_env()
            uri = "file://%s" % image_path

            if desktop_env in ["gnome", "unity"]:
                args = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri]
                subprocess.check_call(args)
            
            elif desktop_env == "cinnamon":    
                args = ["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", uri]
                subprocess.check_call(args)

            elif desktop_env == "kde":
                script = """
                string: 
                var allDesktops = desktops();
                print (allDesktops);
                for (i=0;i<allDesktops.length;i++) {
                    d = allDesktops[i];
                    d.wallpaperPlugin = "org.kde.image";
                    d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
                    d.writeConfig("Image", "file://%s")
                } 
                """ % uri
                
                # If this doesn't work try the other args
                args = ["dbus-send", "--session", "--dest=org.kde.plasmashell", "--type=method_call", "/PlasmaShell", "org.kde.PlasmaShell.evaluateScript", "%s" % script]
                # args = ["qdbus", "org.kde.plasmashell", "/PlasmaShell", "evaluateScript", "%s" % script]
                subprocess.check_call(args)
                
            else:
                raise Exception("Linux Desktop Environment Not Supported")

        elif os_name == "Windows":
            import ctypes
            SPI_SETDESKWALLPAPER = 20
            if isX64():
                ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 0)
            else:
                ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, image_path, 0)
    
    except:
        raise Exception("Could Not Change Background")


@daemonizer.run(pidfile=pidfile)
def wallpaper_daemon(image_list, seconds):
    num_images = len(image_list)
    idx = 0
    while True:
        change_background(image_list[idx])
        idx = (idx + 1) % num_images
        time.sleep(seconds)


def start_timed_wallpaper(image_list, seconds):
    os_name = platform.system()
    if os_name in ["Darwin", "Linux"]:
        wallpaper_daemon(image_list, seconds)
    else:
        # Windows service
        pass


def stop_timed_wallpaper():
    os_name = platform.system()
    if os_name in ["Darwin", "Linux"]:
        wallpaper_daemon.stop()
    else:
        # Stop Windows Service
        pass


# pos argument takes values: 
# topleft(default), topright, bottomleft, bottomright, center
def watermark_image(image_path, text, pos="topleft"):
    try:
        base = Image.open(image_path).convert('RGBA')
        base_width, base_height = base.size
                
        # watermark width = img_fraction * base_width
        img_fraction = 0.20
        font_size = 1
        font_path = os.path.join(ROOT_DIR, "Montserrat-Regular.ttf")
        font = ImageFont.truetype(font_path, font_size)
        while font.getsize(text)[0] < img_fraction * base_width:
            font_size += 1
            font = ImageFont.truetype(font_path, font_size)
        
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)
        font_width, font_height = font.getsize(text)
        
        padding = 3
        coords = (padding, padding)
        if pos == "topright":
            coords = (base_width - font_width - padding, padding)
        elif pos == "bottomleft":
            coords = (padding, base_height - font_height - padding)
        elif pos == "bottomright":
            coords = (base_width - font_width - padding,
                      base_height - font_height - padding)
        elif pos == "center":
            coords = (base_width / 2 - font_width / 2, base_height / 2 - font_height / 2)
        
        watermark = Image.new('RGBA', base.size, (255, 255, 255, 0))
        drawing = ImageDraw.Draw(watermark)
        drawing.text(coords, text, fill=(255, 255, 255, 128), font=font)
        out = Image.alpha_composite(base, watermark)
        out = out.convert("RGB")
        out.save(image_path)
    
    except Exception as e:
        raise Exception("Could Not Watermark Image.")

