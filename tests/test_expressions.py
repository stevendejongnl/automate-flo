"""Self-consistency tests for the expression node types in
automate_flo/expressions.py, decoded from two real .flo exports.

No byte-exact .flo fixtures here: fixtures in this repo are
device-verified artifacts, and these classes were decoded from real
exports instead (round-tripped byte-exactly against them in
tests/test_real_flows.py, env-gated). What these tests pin down is the
writer/reader pair being inverse to each other, plus the two subtle
encodings that byte-exactness depends on:

- ConcatExpr's marker chain: N operands are N-1 consecutive type-119
  markers followed by the operands, and every marker occupies a
  back-reference slot.
- Object identity: the writer dedups every node by identity, so a slot
  reusing an already-written object must parse back as the same
  instance.
"""

from automate_flo import (
    ConcatExpr,
    DoubleExpr,
    EnumDoubleExpr,
    ExpressionDecision,
    FlowBeginning,
    GreaterExpr,
    IndexExpr,
    IntExpr,
    LengthExpr,
    MatchesExpr,
    MinusExpr,
    NumberFormatExpr,
    ReplaceAllExpr,
    SliceExpr,
    SortExpr,
    SplitExpr,
    StorageExpr,
    StringExpr,
    TernaryExpr,
    VariableExpr,
    parse_flow,
    write_flow,
)


def flow_with(expr):
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ed = ExpressionDecision(stmt_id=2, expression=expr, cell_x=0, cell_y=6)
    begin.on_complete = ed
    data = write_flow([begin, ed], next_id=2)
    return parse_flow(data)["blocks"][0].on_complete.expression


def test_matches_expr_round_trip():
    v = flow_with(MatchesExpr(VariableExpr("t"), StringExpr("a.*")))
    assert type(v).__name__ == "MatchesExpr"
    assert v.text.name == "t"
    assert v.pattern.value == "a.*"


def test_index_and_length_round_trip():
    v = flow_with(IndexExpr(VariableExpr("arr"), DoubleExpr(0.0)))
    assert v.container.name == "arr"
    assert v.index.value == 0.0

    v = flow_with(LengthExpr(VariableExpr("arr")))
    assert v.operand.name == "arr"


def test_greater_minus_ternary_round_trip():
    cond = GreaterExpr(LengthExpr(VariableExpr("a")), DoubleExpr(3.0))
    expr = TernaryExpr(cond, MinusExpr(LengthExpr(VariableExpr("a")),
                                        DoubleExpr(3.0)), DoubleExpr(0.0))
    v = flow_with(expr)
    assert type(v).__name__ == "TernaryExpr"
    assert v.if_false.value == 0.0
    assert v.condition.right.value == 3.0


def test_function_exprs_round_trip():
    v = flow_with(NumberFormatExpr(VariableExpr("n"), StringExpr("000")))
    assert v.format.value == "000"

    v = flow_with(ReplaceAllExpr(VariableExpr("s"), StringExpr("[x]"),
                                 StringExpr("_")))
    assert v.replacement.value == "_"

    v = flow_with(SplitExpr(VariableExpr("s"), StringExpr("/")))
    assert v.pattern.value == "/"

    v = flow_with(SortExpr(VariableExpr("a")))
    assert v.array.name == "a"
    assert v.second is None and v.third is None

    v = flow_with(SliceExpr(VariableExpr("a"), DoubleExpr(0.0),
                            DoubleExpr(3.0)))
    assert v.end.value == 3.0


def test_storage_and_int_and_enum_double_round_trip():
    v = flow_with(StorageExpr())
    assert v.first is None and v.second is None

    v = flow_with(IntExpr(1))
    assert v.value == 1

    v = flow_with(EnumDoubleExpr(16777216.0))
    assert v.value == 16777216.0


def test_concat_chain_marker_encoding():
    """A 3-operand ++ chain is 2 consecutive type-119 markers followed
    by 3 operands; every marker occupies a back-reference slot."""
    expr = ConcatExpr([StringExpr("a"), StringExpr("b"), StringExpr("c")])
    v = flow_with(expr)
    assert type(v).__name__ == "ConcatExpr"
    assert [p.value for p in v.parts] == ["a", "b", "c"]

    # Long chain (7 operands, as in the real exports).
    parts = [StringExpr(f"p{i}") for i in range(7)]
    v = flow_with(ConcatExpr(parts))
    assert [p.value for p in v.parts] == [f"p{i}" for i in range(7)]

    # Byte-level: exactly len(parts)-1 markers land in the output.
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    ed = ExpressionDecision(stmt_id=2, expression=ConcatExpr(parts),
                            cell_x=0, cell_y=6)
    begin.on_complete = ed
    data = write_flow([begin, ed], next_id=2)
    marker = bytes([0xEE, 0x01])  # zigzag varint for type id 119
    assert data.count(marker) == len(parts) - 1


def test_shared_object_backrefs_resolve_to_same_instance():
    """Slots reusing one already-written object must parse back as that
    same instance -- regression for the seen-slot bookkeeping that the
    concat markers also participate in."""
    shared = VariableExpr("shared")
    begin = FlowBeginning(stmt_id=1, cell_x=0, cell_y=0, title="")
    first = ExpressionDecision(
        stmt_id=2,
        expression=ConcatExpr([shared, StringExpr("x")]),
        cell_x=0, cell_y=6)
    # The second decision reuses `shared` *after* a concat chain, where
    # marker-inflated seen indexes previously went out of sync.
    second = ExpressionDecision(
        stmt_id=3,
        expression=MatchesExpr(shared, StringExpr("a.*")),
        on_positive=None, on_negative=None, cell_x=0, cell_y=12)
    first.on_positive = second
    begin.on_complete = first

    data = write_flow([begin, first, second], next_id=3)
    parsed = parse_flow(data)["blocks"][0].on_complete
    v1 = parsed.expression.parts[0]
    v2 = parsed.on_positive.expression.text
    assert v1 is v2
    assert v1.name == "shared"
