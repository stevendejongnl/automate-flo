# automate-flo

[![test](https://github.com/stevendejongnl/automate-flo/actions/workflows/test.yml/badge.svg)](https://github.com/stevendejongnl/automate-flo/actions/workflows/test.yml)

Reverse-engineered reader/writer for [LlamaLab Automate](https://llamalab.com/automate/)
`.flo` flow files, in pure Python (no dependencies).

No public spec or parser for this format exists. It was reverse-engineered by
decompiling the Automate APK (1.53.2) with `jadx`, tracing the serializer
classes (`Q3.c`/`Q3.d`/`Q3.g`), and cross-checking the result against real
`.flo` files exported from the app and against the live block-editor UI on an
Android 17 emulator.

## Status

Supports 13 block types. Every one below has a fixture in `tests/fixtures/`
that was pushed to a real Automate install on an Android emulator via adb and
confirmed accepted by the app itself (see "Testing against the real app"):

- `FlowBeginning`
- `AppKill`
- `ActivityStart` ("App start" in the UI)
- `Delay`
- `CarModeEnabled` ("Car mode enabled?" — also the mechanism Automate uses to
  detect Android Auto connecting; there is no dedicated Android Auto block)
- `ToastShow` ("Show toast message")
- `NotificationShow` ("Show notification")
- `SmsSend` ("Send SMS")
- `VariableAssign` ("Assign variable")
- `WifiNetworkConnected` ("Wifi network connected?")
- `BluetoothDeviceConnected` ("Bluetooth device connected?")
- `BatteryLevel` ("Battery level")
- `HttpRequest` ("HTTP request")

`android-auto-app-toggle.flo` (`FlowBeginning` → `ActivityStart` → `Delay`
→ `CarModeEnabled`) was additionally confirmed to run correctly end-to-end,
not just import cleanly, on a real device.

Automate has several hundred block types in total (see `Q3/g.java` in the
decompiled sources for the full registry). Extending coverage means repeating
the same process per block: read the decompiled field-serialization order,
build it in the real app to confirm UI field order, and verify the generated
file against a real Automate install (see below).

## Format summary

```
int32 BE   magic = 0x4c41466c ("LAFl")
int16 BE   version (observed: 114)
varint     next statement id (signed zigzag LEB128)
uvarint    block count N
N x OBJECT top-level blocks
```

Object encoding: `svarint type_id`, where `0` = null, negative = back-reference
into the flat list of previously-written objects (supports the flow's DAG
shape — blocks can loop back to earlier blocks), positive = first-seen, then
dispatch to that type's field writer. Fixed-width ints/doubles are raw
big-endian, not varint. Strings are `uvarint length + UTF-8 bytes`.

Full details and per-block field layouts are documented in the
`automate_flo/format.py` module docstring, including confidence levels
(byte-exact device-verified vs. source-derived-and-UI-corroborated) per block.

## Usage

```python
from automate_flo import FlowBeginning, ActivityStart, Delay, CarModeEnabled, AppKill, write_flow

begin = FlowBeginning(stmt_id=1)
start = ActivityStart(stmt_id=2, package_name="com.example.targetapp", cell_y=6)
delay = Delay(stmt_id=3, seconds=2.0, cell_y=12)
car = CarModeEnabled(stmt_id=4, cell_y=18)
kill = AppKill(stmt_id=5, package_name="com.example.targetapp", cell_x=4, cell_y=24)

begin.on_complete = start
start.on_complete = delay
delay.on_complete = car
car.on_positive = delay   # still connected -> keep polling
car.on_negative = kill    # disconnected -> stop the app

data = write_flow([begin, start, delay, car, kill], next_id=5)
open("my-flow.flo", "wb").write(data)
```

Import the resulting file in Automate via Flows → Import.

## Tests

```
uv run pytest
```

Includes a byte-exact round-trip test against a real Automate-exported sample,
and a self-consistency test for the 5-block Android Auto flow.

### Testing against the real app

`tests/test_emulator_import.py` pushes every fixture `.flo` to a real
Automate install via adb and fires the same `VIEW` intent a file manager
uses to open one, then reads back whatever dialog Automate shows (`Import
"<name>" flow?` = accepted, `Failed to read flow` = rejected) via a
`uiautomator` dump. This is ground truth from the actual app, not our own
parser agreeing with itself.

The Automate APK is LlamaLab's proprietary app and isn't included or
downloaded by anything here -- get it yourself (Play Store on a device, or
an APK mirror for a headless emulator) and install it:

```
adb -s <serial> install -r Automate_<version>.apk
```

Then point the tests at that device:

```
AUTOMATE_FLO_DEVICE_SERIAL=<serial> uv run pytest tests/test_emulator_import.py
```

Without `AUTOMATE_FLO_DEVICE_SERIAL` set, these tests are skipped
automatically -- `uv run pytest` alone never requires a device. CI (see
`.github/workflows/test.yml`) runs the pure round-trip tests only, for this
reason -- the emulator tests need a real Automate install and are meant to
be run locally when adding or changing a block.

## Keeping the wiki in sync

The [wiki](https://github.com/stevendejongnl/automate-flo/wiki)'s Format
Specification and Block Reference pages are written by hand from
`automate_flo/format.py`'s module docstring, which is the real source of
truth. Two things help catch drift:

- **`.github/workflows/wiki-sync-check.yml`** runs on any PR touching
  `format.py` and posts a warning (non-blocking) if a block type in the
  file's type-id table isn't mentioned anywhere in the wiki's
  `Block-Reference.md`.
- **A local pre-push hook** (`.githooks/pre-push`) does the same reminder
  locally, before you even push. Enable it once per clone:

  ```bash
  git config core.hooksPath .githooks
  ```

Neither check blocks a push or merge -- they're reminders, since verifying
the wiki's *prose* is accurate (not just that a name appears somewhere)
isn't something either can automate.
