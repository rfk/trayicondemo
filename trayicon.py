 
import os
import sys
import socket
import threading

from PySide import QtCore, QtGui


def find_resource(filenm):
    """Find a resource file, relative to the installed applicaiton.

    This function tries a variety of different locations where a resource file
    might be found, such as right next to the frozen executable (py2exe) or
    in a special Resources directory (OSX).
    """
    # Find the right directory to look in for resource files.
    # This will depend on the platform, and whether we're frozen.
    if getattr(sys, "frozen", False):
        if sys.platform == "darwin":
            resdir = os.path.dirname(os.path.dirname(sys.executable))
            resdir = os.path.join(resdir, "Resources")
        else:
            resdir = os.path.dirname(sys.executable)
    else:
        resdir = os.path.dirname(os.path.abspath(__file__))
    # The target path will be relative to the resource directory.
    filenm = os.path.normpath(filenm)
    return os.path.join(resdir, filenm)
        


class DaemonWithTrayIcon(QtGui.QApplication):
    """Example QApplication with a tray icon and socket handling.

    This is a simple example QApplication that displays a tray icon in th
    UI, and runs a background thread listening on a socket.  When running
    you should see the following behaviours:

        * tray icon appears at startup
        * clicking tray icon gives context menu with "quit" option
        * double-clicking tray icon brings up a message window where supported
        * connecting to localhost:8080 will echo an example message

    """

    def __init__(self, argv=None):
        self.running = False
        QtGui.QApplication.__init__(self, argv or sys.argv)

        # This is necessary to let the app become a daemon,
        # since it must stay alive with no active windows.
        self.setQuitOnLastWindowClosed(False)

        # Set a nice icon, which we'll reuse for the tray display.
        icon_file = find_resource("trayicon.png")
        self.setWindowIcon(QtGui.QIcon(icon_file))

    def start(self):
        self.running = True
        self.start_socket_handlers()
        self.create_gui()
        # This enters the Qt event loop, blocking until the app exits.
        self.exec_()

    def stop(self, exit_code=0):
        self.running = False
        self.destroy_gui()
        self.stop_socket_handlers()
        # This causes the app to exit, unblocking the self.exec_() call above.
        self.exit(exit_code)

    def create_gui(self):
        # Create a message window, but don't show it straight away.
        # In a real app this might be e.g. the configuration UI.
        self.main_window = QtGui.QLabel("Hello Example!")

        # Re-use the window icon as the system tray icon.
        # On Ubuntu, it appears this will only work if the icon is
        # the correct size, so scale it accordingly.
        icon = self.windowIcon()
        smaller_icon = QtGui.QIcon(icon.pixmap(32, 32))

        # Create the tray icon, and hook up double-click event.
        self.tray_icon = QtGui.QSystemTrayIcon(smaller_icon, self)
        self.tray_icon.setToolTip("AN EXAMPLE DAEMON")
        self.tray_icon.activated.connect(self._on_tray_icon_activated)
        self.tray_icon.show()

        # Create a context menu to go along with the tray icon.
        # In a real app you would have more options in here.
        self.tray_menu = QtGui.QMenu()
        self.tray_icon.setContextMenu(self.tray_menu)
        act = self.tray_menu.addAction("Open")
        act.triggered.connect(self.main_window.show)
        act = self.tray_menu.addAction("Quit")
        act.triggered.connect(self.stop)

    def destroy_gui(self):
        self.main_window.hide()
        self.main_window.deleteLater()
        self.tray_icon.deleteLater()

    def _on_tray_icon_activated(self,reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.main_window.show()

    def start_socket_handlers(self):
        # Bind to the socket from the main thread.
        # This lets any exceptions propagate back to the caller.
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(("127.0.0.1", 8080))
        # Start a background thread to handle all activity on the socket.
        self._handler_thread = threading.Thread(target=self._socket_handler)
        self._handler_thread.start()

    def stop_socket_handlers(self):
        # Close and bounce the socket.
        # This interrupts the accept() call and allows the
        # background thread to exit cleanly.  Ugly, but useful.
        self._sock.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            s.connect(("127.0.0.1", 8080))
        except socket.error:
            pass

    def _socket_handler(self):
        self._sock.listen(10)
        while self.running:
            try:
                conn, addr = self._sock.accept()
            except socket.error:
                pass
            else:
                conn.sendall("EXAMPLE!\n")
                conn.close()


if __name__ == "__main__":
    DaemonWithTrayIcon().start()
