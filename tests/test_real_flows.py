"""Byte-exact round-trip against real Automate-exported .flo files.

The wire layouts in the block/expression classes added alongside this
test were decoded from two real device exports of the same flow, one
before and one after an in-app edit (format versions 114 and 115).
This test is the acceptance criterion for that decoding: parsing and
re-writing each file must reproduce it byte for byte, including the
3-byte trailing footer and every shared-object back-reference.

The flow files are private (they contain the owner's app list), so
they are NOT part of this repository. Point the environment variable
AUTOMATE_FLO_REAL_FLOWS at a comma-separated list of .flo paths to run:

    AUTOMATE_FLO_REAL_FLOWS=/path/to/a.flo,/path/to/b.flo pytest

Skipped entirely when the variable is unset (the usual CI case).
"""

import os
import pathlib

import pytest

from automate_flo import parse_flow, write_flow

REAL_FLOWS = [
    pathlib.Path(p)
    for p in os.environ.get("AUTOMATE_FLO_REAL_FLOWS", "").split(",")
    if p.strip()
]

pytestmark = pytest.mark.skipif(
    not REAL_FLOWS,
    reason="set AUTOMATE_FLO_REAL_FLOWS to a comma-separated list of "
           "real .flo exports to run the byte-exact round-trip tests",
)


@pytest.mark.parametrize("path", REAL_FLOWS, ids=lambda p: p.name)
def test_real_flow_round_trip_byte_exact(path):
    data = path.read_bytes()
    parsed = parse_flow(data)
    assert parsed["version"] in (114, 115)
    # The trailing footer (3 back-references, semantics not fully
    # understood) must be captured and re-emitted verbatim.
    assert len(parsed["trailing"]) == 3

    out = write_flow(
        parsed["blocks"],
        parsed["next_id"],
        version=parsed["version"],
        trailing=parsed["trailing"],
    )
    assert out == data, (
        f"{path.name}: re-write differs from the export at the first "
        f"differing byte {next(i for i, (a, b) in enumerate(zip(out, data)) if a != b)}"
    )
