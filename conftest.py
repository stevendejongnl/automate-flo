"""Shared pytest fixtures for real-device verification against a live
Automate install, available to every test in the repo (per-block tests in
automate_flo/blocks/ and the cross-cutting flow tests in tests/).

See tests/emulator.py for the low-level adb helpers this wraps, and
README.md -> "Testing against the real app" for how to set a device up.

Set AUTOMATE_FLO_DEVICE_SERIAL to the adb serial to test against, e.g.:

    AUTOMATE_FLO_DEVICE_SERIAL=emulator-5554 uv run pytest
"""

import os

import pytest

from tests.emulator import (
    automate_installed,
    device_online,
    ensure_storage_permission,
    import_flow,
)

SERIAL = os.environ.get("AUTOMATE_FLO_DEVICE_SERIAL")


@pytest.fixture(scope="session")
def device_serial():
    if not SERIAL:
        pytest.skip(
            "set AUTOMATE_FLO_DEVICE_SERIAL to an adb device serial to run "
            "these tests against a real Automate install"
        )
    if not device_online(SERIAL):
        pytest.skip(f"device {SERIAL!r} not online (check `adb devices`)")
    if not automate_installed(SERIAL):
        pytest.skip(
            "Automate is not installed on this device. Download the APK "
            "yourself (LlamaLab does not permit redistribution) and: "
            f"adb -s {SERIAL} install -r Automate_<version>.apk"
        )
    ensure_storage_permission(SERIAL)
    return SERIAL


@pytest.fixture
def import_flow_fn(device_serial):
    """Returns a callable(local_path) -> dialog_text, bound to the device
    under test. Each per-block test calls this with its own fixture path."""

    def _import(local_path):
        return import_flow(device_serial, local_path)

    return _import
