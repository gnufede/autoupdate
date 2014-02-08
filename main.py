import os
import sys
import wx

TRAY_TOOLTIP = 'System Tray Demo'
TRAY_ICON = './icon.png'


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        image = wx.Image(TRAY_ICON, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(image)
        self.SetIcon(icon)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        self.parent_win = None

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Say Hello', self.on_hello)
        menu.AppendSeparator()
        if os.path.isfile('main2.py'):
            create_menu_item(menu, 'Update', self.on_update)
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        print('Tray icon was left-clicked.')

    def on_hello(self, event):
        print('Hello, world!')

    def on_update(self, event):
        os.rename('main2.py','main.py')
        self.on_exit(event)
        restart()

    def on_exit(self, event):
        self.parent_win.Destroy()
        wx.CallAfter(self.Destroy)

def restart():
    args = sys.argv[:]
    print('Re-spawning %s' % ' '.join(args))
    args.insert(0, sys.executable)
    if sys.platform == 'win32':
        args = ['"%s"' % arg for arg in args]
    os.chdir(os.getcwd())
    os.execv(sys.executable, args)

def main():
    app = wx.App()
    tb = TaskBarIcon()
    frame = wx.Frame(None, -1, 'simple.py')
    tb.parent_win = frame
    app.MainLoop()


if __name__ == '__main__':
    main()

