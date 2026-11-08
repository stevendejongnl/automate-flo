"""Expression node types beyond the four literal wrappers in base.py:
boxed-value wrappers, operators, and function calls.

Decoded from two real Automate exports (format versions 114 and 115 of
the same flow, one before and one after an in-app edit), cross-verified
between them, and byte-exact round-trip tested (tests/test_real_flows.py,
env-gated). The app's UI never shows node names (the expression editor
displays source text), so class names here describe the operation, not
Automate's internal class names. See format.py's module docstring for
the type-id index.

Automate back-references an expression only when the app reuses one
operand *object*, never because two expressions are equal: a real
export contains two distinct split(...) nodes with identical arguments,
and the same string literal written out twice as separate objects. Every
class here therefore dedups by identity, exactly like blocks.
"""


class _ExprNode:
    """Shared base: identity-based dedup (see module docstring)."""

    def dedup_key(self):
        return ("id", id(self))


class IntExpr(_ExprNode):
    """id 16, boxed java.lang.Integer. Single signed-zigzag varint, no
    length prefix. Observed carrying the proceed/continuity enum
    (0 = Immediately, 1 = When changed / Inexact) and picked integers."""

    type_id = 16

    def __init__(self, value: int):
        self.value = value

    def write_fields(self, writer):
        writer.w.write_svarint(self.value)

    def read_fields(self, reader):
        self.value = reader.r.read_svarint()

    def describe(self):
        return f"IntExpr({self.value})"


class EnumDoubleExpr(_ExprNode):
    """id 101, an 8-byte big-endian double with no length prefix -- the
    same wire shape as DoubleExpr (104) but a distinct type, observed
    only carrying picker/enum option values (AppList flagsExclude
    16777216.0, FileList contentType 2.0, ZipCompress compression method
    0.0). Its real class name is unknown; it is kept distinct from
    DoubleExpr so round trips preserve which wrapper the app wrote."""

    type_id = 101

    def __init__(self, value: float):
        self.value = float(value)

    def write_fields(self, writer):
        writer.w.write_double(self.value)

    def read_fields(self, reader):
        self.value = reader.r.read_double()

    def describe(self):
        return f"EnumDoubleExpr({self.value})"


class ConcatExpr(_ExprNode):
    """id 119, the `++` text-concatenation operator, as a chain.

    Wire encoding: N consecutive type-119 markers followed by N+1
    operand objects -- the app's serializer flattens the left-nested
    binary chain it builds for `a ++ b ++ c` into marker, marker, a, b,
    c. EVERY marker is a first-seen object occupying a back-reference
    slot (observed N = 2, 3, 6 and 7 in real files), so the N-1 markers
    after the node's own are stored in the reader's seen list as empty
    ConcatExpr instances -- writing an empty ConcatExpr emits exactly a
    bare marker, which is its wire form. Construct with the operand
    list; a real chain has len(parts) >= 2 (0 and 1 are only reachable
    as wire artifacts)."""

    type_id = 119

    def __init__(self, parts):
        self.parts = list(parts)

    def write_fields(self, writer):
        # A chain of N operands carries N-1 markers in total; the node's
        # own marker (written by write_object) is the first of them, so
        # only N-2 further bare markers are emitted here.
        for _ in range(len(self.parts) - 2):
            writer.write_object(ConcatExpr([]))
        for part in self.parts:
            writer.write_object(part)

    def read_fields(self, reader):
        extra = 0
        while True:
            save = reader.r.pos
            if reader.r.read_svarint() == self.type_id:
                marker = ConcatExpr.__new__(ConcatExpr)
                marker.parts = []
                reader.seen.append(marker)
                extra += 1
            else:
                reader.r.pos = save
                break
        # Total markers = extra + 1 (the node's own, consumed by
        # read_object, plus the peeked ones); operands = markers + 1.
        self.parts = [reader.read_object() for _ in range(extra + 2)]

    def describe(self):
        return "ConcatExpr(" + " ++ ".join(_d(p) for p in self.parts) + ")"


class TernaryExpr(_ExprNode):
    """id 120, the `? :` conditional operator: condition, then-value,
    else-value."""

    type_id = 120

    def __init__(self, condition, if_true, if_false):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def write_fields(self, writer):
        writer.write_object(self.condition)
        writer.write_object(self.if_true)
        writer.write_object(self.if_false)

    def read_fields(self, reader):
        self.condition = reader.read_object()
        self.if_true = reader.read_object()
        self.if_false = reader.read_object()

    def describe(self):
        return f"TernaryExpr({_d(self.condition)} ? {_d(self.if_true)} : {_d(self.if_false)})"


class GreaterExpr(_ExprNode):
    """id 124, the `>` comparison operator."""

    type_id = 124

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def write_fields(self, writer):
        writer.write_object(self.left)
        writer.write_object(self.right)

    def read_fields(self, reader):
        self.left = reader.read_object()
        self.right = reader.read_object()

    def describe(self):
        return f"GreaterExpr({_d(self.left)} > {_d(self.right)})"


class LengthExpr(_ExprNode):
    """id 126, the `#` length operator (array element count / text
    length)."""

    type_id = 126

    def __init__(self, operand):
        self.operand = operand

    def write_fields(self, writer):
        writer.write_object(self.operand)

    def read_fields(self, reader):
        self.operand = reader.read_object()

    def describe(self):
        return f"LengthExpr(#{_d(self.operand)})"


class IndexExpr(_ExprNode):
    """id 137, the `[]` index operator: container, index."""

    type_id = 137

    def __init__(self, container, index):
        self.container = container
        self.index = index

    def write_fields(self, writer):
        writer.write_object(self.container)
        writer.write_object(self.index)

    def read_fields(self, reader):
        self.container = reader.read_object()
        self.index = reader.read_object()

    def describe(self):
        return f"IndexExpr({_d(self.container)}[{_d(self.index)}])"


class MinusExpr(_ExprNode):
    """id 138, the `-` subtraction operator."""

    type_id = 138

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def write_fields(self, writer):
        writer.write_object(self.left)
        writer.write_object(self.right)

    def read_fields(self, reader):
        self.left = reader.read_object()
        self.right = reader.read_object()

    def describe(self):
        return f"MinusExpr({_d(self.left)} - {_d(self.right)})"


class MatchesExpr(_ExprNode):
    """id 322, the matches() function: text, regular expression (whole-
    string match)."""

    type_id = 322

    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern

    def write_fields(self, writer):
        writer.write_object(self.text)
        writer.write_object(self.pattern)

    def read_fields(self, reader):
        self.text = reader.read_object()
        self.pattern = reader.read_object()

    def describe(self):
        return f"MatchesExpr({_d(self.text)}, {_d(self.pattern)})"


class NumberFormatExpr(_ExprNode):
    """id 327, the numberFormat() function: number, format string, and a
    third slot observed null (grouping/locale option?)."""

    type_id = 327

    def __init__(self, number, format, third=None):
        self.number = number
        self.format = format
        self.third = third

    def write_fields(self, writer):
        writer.write_object(self.number)
        writer.write_object(self.format)
        writer.write_object(self.third)

    def read_fields(self, reader):
        self.number = reader.read_object()
        self.format = reader.read_object()
        self.third = reader.read_object()

    def describe(self):
        return f"NumberFormatExpr({_d(self.number)}, {_d(self.format)}, {_d(self.third)})"


class ReplaceAllExpr(_ExprNode):
    """id 329, the replaceAll() function: text, regular expression,
    replacement."""

    type_id = 329

    def __init__(self, text, pattern, replacement):
        self.text = text
        self.pattern = pattern
        self.replacement = replacement

    def write_fields(self, writer):
        writer.write_object(self.text)
        writer.write_object(self.pattern)
        writer.write_object(self.replacement)

    def read_fields(self, reader):
        self.text = reader.read_object()
        self.pattern = reader.read_object()
        self.replacement = reader.read_object()

    def describe(self):
        return f"ReplaceAllExpr({_d(self.text)}, {_d(self.pattern)}, {_d(self.replacement)})"


class SplitExpr(_ExprNode):
    """id 333, the split() function: text, regular expression."""

    type_id = 333

    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern

    def write_fields(self, writer):
        writer.write_object(self.text)
        writer.write_object(self.pattern)

    def read_fields(self, reader):
        self.text = reader.read_object()
        self.pattern = reader.read_object()

    def describe(self):
        return f"SplitExpr({_d(self.text)}, {_d(self.pattern)})"


class StorageExpr(_ExprNode):
    """id 347, the storage() function: two slots, both observed null."""

    type_id = 347

    def __init__(self, first=None, second=None):
        self.first = first
        self.second = second

    def write_fields(self, writer):
        writer.write_object(self.first)
        writer.write_object(self.second)

    def read_fields(self, reader):
        self.first = reader.read_object()
        self.second = reader.read_object()

    def describe(self):
        return "StorageExpr()"


class SortExpr(_ExprNode):
    """id 371, the sort() function: array, then two slots observed null
    (comparator / order options?). Arity 3, not 2 -- with arity 2 the
    same bytes still parse byte-complete but the following expression
    tree gets bucketed wrong (a ternary ends up displaced into an
    enclosing ForEach slot); arity 3 makes every ForEach in both real
    files decode consistently."""

    type_id = 371

    def __init__(self, array, second=None, third=None):
        self.array = array
        self.second = second
        self.third = third

    def write_fields(self, writer):
        writer.write_object(self.array)
        writer.write_object(self.second)
        writer.write_object(self.third)

    def read_fields(self, reader):
        self.array = reader.read_object()
        self.second = reader.read_object()
        self.third = reader.read_object()

    def describe(self):
        return f"SortExpr({_d(self.array)}, {_d(self.second)}, {_d(self.third)})"


class SliceExpr(_ExprNode):
    """id 383, the slice() function: array, start, end (an end of null
    means through-the-end; the real deletion-loop expression slices to
    an index computed with a ternary)."""

    type_id = 383

    def __init__(self, array, start, end):
        self.array = array
        self.start = start
        self.end = end

    def write_fields(self, writer):
        writer.write_object(self.array)
        writer.write_object(self.start)
        writer.write_object(self.end)

    def read_fields(self, reader):
        self.array = reader.read_object()
        self.start = reader.read_object()
        self.end = reader.read_object()

    def describe(self):
        return f"SliceExpr({_d(self.array)}, {_d(self.start)}, {_d(self.end)})"


def _d(obj):
    """Small shared describe helper for nested expression nodes."""
    if obj is None:
        return "null"
    if isinstance(obj, _ExprNode):
        return obj.describe()
    if isinstance(obj, float):
        return repr(obj)
    return repr(obj)


EXPRESSION_NODES = [
    IntExpr,
    EnumDoubleExpr,
    ConcatExpr,
    TernaryExpr,
    GreaterExpr,
    LengthExpr,
    IndexExpr,
    MinusExpr,
    MatchesExpr,
    NumberFormatExpr,
    ReplaceAllExpr,
    SplitExpr,
    StorageExpr,
    SortExpr,
    SliceExpr,
]

__all__ = [cls.__name__ for cls in EXPRESSION_NODES] + ["EXPRESSION_NODES"]
