
import os
import sys
import shutil

from esky import bdist_esky
from distutils.core import setup

def adjust_frozen_app(dist):
    """Callback for customizing the frozen application."""

    # On OSX, we need to copy some additional resources
    # into the bootstrapping environment.  It would be good
    # for this logic to move into esky itself at some point,
    # e.g. as a list of configurable 'extra resources'.
    if sys.platform == "darwin":
        sys_res_dir = os.path.join(sys.prefix,
                                   "../../../../../Contents/Resources/")
        app_res_dir = os.path.join(dist.freeze_dir, "trayicondemo.app",
                                   "Contents", "Resources")
        shutil.copytree(os.path.join(sys_res_dir, "qt_menu.nib"),
                        os.path.join(app_res_dir, "qt_menu.nib"))


esky_opts = {}
esky_opts["pre_zip_callback"] = adjust_frozen_app

if sys.platform == "darwin":
    # Tweak the freeze process on OSX.
    # We want the app to run without an icon in the dock.
    esky_opts["freezer_module"] = "py2app"
    esky_opts["freezer_options"] = {
        "argv_emulation": False,
        "plist": {"LSUIElement": 1},
    }

elif sys.platform == "win32":
    esky_opts["freezer_module"] = "py2exe"

else:
    esky_opts["freezer_module"] = "cxfreeze"


setup(
  name = "trayicondemo",
  version = "0.1",
  scripts = ["trayicon.py"],
  data_files = [("", ["trayicon.png"])],
  options = {
      "bdist_esky": esky_opts,
  }
)

