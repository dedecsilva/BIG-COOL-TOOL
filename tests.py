import ctypes

user32 = ctypes.WinDLL("user32.dll")

hwnd_desktop = user32.GetDesktopWindow()
user32.TileWindows(hwnd_desktop, 0x0001, None, 0, None)
user32.TileWindows(hwnd_desktop, 0x0002, None, 0, None)
