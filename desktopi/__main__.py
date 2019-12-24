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
            subprocess.check_call(["killall Dock"], shell=True)

        elif os_name == "Linux":
            desktop_env = get_linux_desktop_env()
            uri = f'"file://{image_path}"'

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

