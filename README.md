# automate-flo

Reverse-engineered reader/writer for [LlamaLab Automate](https://llamalab.com/automate/)
`.flo` flow files, in pure Python (no dependencies).

No public spec or parser for this format exists. It was reverse-engineered by
decompiling the Automate APK (1.53.2) with `jadx`, tracing the serializer
classes (`Q3.c`/`Q3.d`/`Q3.g`), and cross-checking the result against real
`.flo` files exported from the app and against the live block-editor UI on an
Android 17 emulator.

## Status

Supports 5 block types — enough to build a real working flow (see
`tests/fixtures/android-auto-flitsmeister.flo`, confirmed imported and
executed successfully on a real device):

- `FlowBeginning`
- `AppKill`
- `ActivityStart` ("App start" in the UI)
- `Delay`
- `CarModeEnabled` ("Car mode enabled?" — also the mechanism Automate uses to
  detect Android Auto connecting; there is no dedicated Android Auto block)

Automate has several hundred block types in total (see `Q3/g.java` in the
decompiled sources for the full registry). Extending coverage means repeating
the same process per block: read the decompiled field-serialization order,
build it in the real app to confirm UI field order, and ideally export a real
sample to byte-diff against.

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
start = ActivityStart(stmt_id=2, package_name="nl.flitsmeister", cell_y=6)
delay = Delay(stmt_id=3, seconds=2.0, cell_y=12)
car = CarModeEnabled(stmt_id=4, cell_y=18)
kill = AppKill(stmt_id=5, package_name="nl.flitsmeister", cell_x=4, cell_y=24)

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
and a self-consistency test for the 5-block Android Auto flow (device-verified
separately, see status above).
