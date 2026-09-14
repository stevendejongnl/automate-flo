"""Thin adb wrapper for driving a real Automate install during tests.

Not a general-purpose adb library -- just the handful of operations the
emulator-backed import test needs (push a file, fire the FlowImportActivity
VIEW intent, read back what dialog it shows via a uiautomator dump).
"""

import re
import shutil
import subprocess
import time

AUTOMATE_PACKAGE = "com.llamalab.automate"
IMPORT_ACTIVITY = f"{AUTOMATE_PACKAGE}/.FlowImportActivity"
DEVICE_DIR = "/sdcard/Download"


class AdbError(RuntimeError):
    pass


def adb_available() -> bool:
    return shutil.which("adb") is not None


def _run(serial, *args, check=True):
    cmd = ["adb", "-s", serial, *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise AdbError(f"{' '.join(cmd)} failed: {result.stderr.strip()}")
    return result.stdout


def device_online(serial: str) -> bool:
    if not adb_available():
        return False
    out = subprocess.run(["adb", "devices"], capture_output=True, text=True).stdout
    for line in out.splitlines()[1:]:
        parts = line.split()
        if len(parts) == 2 and parts[0] == serial and parts[1] == "device":
            return True
    return False


def automate_installed(serial: str) -> bool:
    out = _run(serial, "shell", "pm", "list", "packages", AUTOMATE_PACKAGE, check=False)
    return AUTOMATE_PACKAGE in out


def ensure_storage_permission(serial: str):
    """FlowImportActivity needs MANAGE_EXTERNAL_STORAGE to read files from
    /sdcard on modern Android; grant it once via appops (no UI interaction
    needed, unlike the runtime permission dialog)."""
    _run(serial, "shell", "appops", "set", AUTOMATE_PACKAGE,
         "MANAGE_EXTERNAL_STORAGE", "allow", check=False)


def import_flow(serial: str, local_path, device_name: str = None, settle_seconds: float = 2.0) -> str:
    """Push a .flo file to the device and fire the same VIEW intent a file
    manager would use to open it, which routes to Automate's
    FlowImportActivity (see AndroidManifest.xml intent-filter for
    android.intent.action.VIEW + *.flo / application/octet-stream).

    Returns the text of whatever dialog Automate shows in response, read via
    a uiautomator UI dump -- this is the ground-truth signal for whether the
    file was accepted ('Import "<name>" flow?') or rejected ('Failed to read
    flow', or similar), straight from the real app, not from our own parser.
    """
    device_name = device_name or local_path.name
    device_path = f"{DEVICE_DIR}/{device_name}"

    _run(serial, "push", str(local_path), device_path)
    try:
        _run(serial, "shell", "am", "start",
             "-a", "android.intent.action.VIEW",
             "-d", f"file://{device_path}",
             "-t", "application/octet-stream",
             "-n", IMPORT_ACTIVITY)
        time.sleep(settle_seconds)

        _run(serial, "shell", "uiautomator", "dump", "/sdcard/automate_flo_test_ui.xml")
        dump = _run(serial, "shell", "cat", "/sdcard/automate_flo_test_ui.xml")

        # Dismiss whatever dialog is up so the next test starts clean.
        _run(serial, "shell", "input", "keyevent", "KEYCODE_BACK", check=False)

        texts = re.findall(r'text="([^"]*)"', dump)
        return "\n".join(t for t in texts if t)
    finally:
        _run(serial, "shell", "rm", "-f", device_path, check=False)
        _run(serial, "shell", "rm", "-f", "/sdcard/automate_flo_test_ui.xml", check=False)
