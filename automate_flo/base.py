"""
Base classes shared across every .flo block type: the common statement
header (Block), the two branch shapes every Automate statement uses
(Action: onComplete; Decision: onPositive/onNegative), their
"with a continuity field" variants (IntermittentAction/
IntermittentDecision), the further-specialized LevelDecision (adds
minLevel/maxLevel/varLevel), and the four expression wrapper types used
for literal/variable-reference fields (StringExpr/VariableExpr/
DoubleExpr/BooleanExpr).

Each level's write_fields/read_fields calls super() first, then appends
its own piece -- mirroring the real Automate class hierarchy traced in
automate_flo/format.py's module docstring and the wiki's
Reverse-Engineering-Notes.md page. Concrete per-block classes built on
top of these live in automate_flo/blocks/.
"""

TYPE_STRING_EXPR = 106      # K3.W: string literal expression wrapper
TYPE_DOUBLE_EXPR = 104      # K3.J: double literal expression wrapper
TYPE_VARIABLE_EXPR = 102    # I3.l: mutable-variable reference (plain UTF name)
TYPE_BOOLEAN_EXPR = 1       # Q3.g$j: boxed java.lang.Boolean, single 0/1 byte, no length prefix


class Block:
    """Base: every block has a statement id, a (cellX, cellY) grid position,
    and (for Action subclasses) an onComplete pointer to the next block.

    cell_x/cell_y are editor grid coordinates (each unit is one small grid
    square in the flowchart view), not pixels, and there is no auto-layout:
    packing blocks at consecutive integers (0, 1, 2, ...) draws their cards
    overlapping in the editor. Leave a gap of ~6 units between sequential
    blocks (see the flow built in tests/test_format.py) for a readable
    layout."""
    type_id = None

    def __init__(self, stmt_id, cell_x=0, cell_y=0, on_complete=None):
        self.stmt_id = stmt_id
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.on_complete = on_complete

    def dedup_key(self):
        """Identity-based by default -- every block is a distinct graph
        node. Only the value-typed expression wrappers below override
        this, to intern by value (so e.g. the same package name passed to
        two different blocks collapses to one back-referenced object,
        matching real Automate-exported flows)."""
        return ("id", id(self))

    def write_fields(self, writer):
        """AbstractStatement fields, common to every block."""
        writer.w.write_svarint(self.stmt_id)
        writer.w.write_svarint(self.cell_x)
        writer.w.write_svarint(self.cell_y)

    def read_fields(self, reader):
        self.stmt_id = reader.r.read_svarint()
        self.cell_x = reader.r.read_svarint()
        self.cell_y = reader.r.read_svarint()

    def describe(self):
        return f"{type(self).__name__}(id={self.stmt_id})"


class Action(Block):
    """Adds onComplete: OBJECT ref to the next block, or null."""

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.on_complete)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.on_complete = reader.read_object()


class Decision(Block):
    """Adds onPositive/onNegative instead of onComplete -- NOT an Action.
    Used directly (no continuity field) by ExpressionDecision, AccountPick
    and ActivityStartResult; every other Decision-family block in this
    library goes through IntermittentDecision below instead."""

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.on_positive)
        writer.write_object(self.on_negative)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.on_complete = None
        self.on_positive = reader.read_object()
        self.on_negative = reader.read_object()


class IntermittentAction(Action):
    """Adds continuity (boxed Integer, null = default) after onComplete."""

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.continuity)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.continuity = reader.read_object()


class IntermittentDecision(Decision):
    """Adds continuity after onPositive/onNegative."""

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.continuity)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.continuity = reader.read_object()


class LevelDecision(IntermittentDecision):
    """Adds minLevel/maxLevel/varLevel after continuity. Used by
    BatteryLevel (no further fields) and ScreenBrightness (adds its own
    scale/auto/varAuto/varAdjustment on top)."""

    def write_fields(self, writer):
        super().write_fields(writer)
        writer.write_object(self.min_level)
        writer.write_object(self.max_level)
        writer.write_object(self.var_level)

    def read_fields(self, reader):
        super().read_fields(reader)
        self.min_level = reader.read_object()
        self.max_level = reader.read_object()
        self.var_level = reader.read_object()


class StringExpr:
    """K3.W -- string literal expression wrapper, type id 106."""
    type_id = TYPE_STRING_EXPR

    def __init__(self, value: str):
        self.value = value

    def dedup_key(self):
        return ("str", self.value)

    def write_fields(self, writer):
        writer.w.write_utf(self.value)

    def read_fields(self, reader):
        self.value = reader.r.read_utf()

    def describe(self):
        return f"StringExpr({self.value!r})"


class VariableExpr:
    """I3.l -- mutable-variable reference, type id 102. Plain UTF name, same
    wire shape as StringExpr but a distinct type used specifically for
    variable name fields (e.g. VariableAssign.variable, *.varXxx fields)."""
    type_id = TYPE_VARIABLE_EXPR

    def __init__(self, name: str):
        self.name = name

    def dedup_key(self):
        return ("var", self.name)

    def write_fields(self, writer):
        writer.w.write_utf(self.name)

    def read_fields(self, reader):
        self.name = reader.r.read_utf()

    def describe(self):
        return f"VariableExpr({self.name!r})"


class DoubleExpr:
    """K3.J -- double literal expression wrapper, type id 104. Raw 8-byte
    big-endian double, no length prefix."""
    type_id = TYPE_DOUBLE_EXPR

    def __init__(self, value: float):
        self.value = float(value)

    def dedup_key(self):
        return ("dbl", self.value)

    def write_fields(self, writer):
        writer.w.write_double(self.value)

    def read_fields(self, reader):
        self.value = reader.r.read_double()

    def describe(self):
        return f"DoubleExpr({self.value!r})"


class BooleanExpr:
    """Q3.g$j -- boxed java.lang.Boolean, type id 1. Single 0/1 byte, no
    length prefix. This is the generic boxed-object wire type (not a
    dedicated boolean-literal *expression* wrapper like StringExpr/
    DoubleExpr are for their types), but Automate accepts a raw boxed
    Boolean directly wherever a boolean-valued expression field is
    expected (e.g. SetStateAction.state, Delay.wakeup)."""
    type_id = TYPE_BOOLEAN_EXPR

    def __init__(self, value: bool):
        self.value = bool(value)

    def dedup_key(self):
        return ("bool", self.value)

    def write_fields(self, writer):
        writer.w.write_bool(self.value)

    def read_fields(self, reader):
        self.value = reader.r.read_bool()

    def describe(self):
        return f"BooleanExpr({self.value!r})"
