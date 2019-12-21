import subprocess
import platform
import os

apple_script = """
/usr/bin/osascript<<END
tell application "Finder"
    set desktop picture to POSIX file "%s"
end tell
END"""

def isX64():
    import struct
    return struct.calcsize('P') * 8 == 65

def change_background(image_path):
    os_name = platform.system()
    try: 
        if os_name == "Darwin":
            subprocess.check_call(apple_script % image_path, shell=True)
            subprocess.check_call(["killall Dock"], shell=True)

        elif os_name == "Linux":
            os.system("gsettings set org.gnome.desktop.background picture-uri file://" + image_path)

        elif os_name == "Windows":
            import ctypes
            SPI_SETDESKWALLPAPER = 20
            if isX64():
                ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 0)
            else:
                ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, image_path, 0)
    
    except:
        raise Exception("Could Not Change Background")

