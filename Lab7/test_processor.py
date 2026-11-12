import math

from hypothesis import given, settings, strategies as st

from processor import (
    calculate_dimensional_weight,
    format_tracking_label,
    parse_package_manifest,
)


# Property-based fuzz tests: arbitrary text and None must never crash.
@settings(max_examples=200)
@given(st.one_of(st.text(), st.none()))
def test_calculate_dimensional_weight_no_crash(value):
    result = calculate_dimensional_weight(value)
    assert isinstance(result, float)
    assert math.isfinite(result)
    assert result >= 0


@settings(max_examples=200)
@given(st.one_of(st.text(), st.none()))
def test_format_tracking_label_safe(value):
    result = format_tracking_label(value)
    assert isinstance(result, str)
    assert result == "INVALID-000000" or (
        len(result.split("-")) == 2
        and result[0].isalpha()
        and result[1].isdigit()
    )


@settings(max_examples=200)
@given(st.one_of(st.text(), st.none()))
def test_parse_package_manifest_safe(value):
    result = parse_package_manifest(value)
    assert isinstance(result, float)
    assert math.isfinite(result)
    assert result >= 0


# Valid-input regression tests.
def test_valid_dimensional_weight():
    assert calculate_dimensional_weight("20x30x10") == 1.2


def test_dimensions_allow_spaces_and_uppercase_x():
    assert calculate_dimensional_weight(" 20 X 30 X 10 ") == 1.2


def test_valid_tracking_label():
    assert format_tracking_label("E123") == "E-000123"


def test_tracking_label_uppercases_prefix():
    assert format_tracking_label("e123") == "E-000123"


def test_valid_manifest():
    assert parse_package_manifest('{"weight": 12.5}') == 12.5


def test_manifest_accepts_numeric_string():
    assert parse_package_manifest('{"weight": "12.5"}') == 12.5


# Explicit malformed and boundary cases.
def test_invalid_dimensions_return_zero():
    for value in (
        None, "", "20x30", "20x30x10x5", "a x b x c",
        "0x30x10", "-1x30x10", "nanx30x10", "infx30x10",
    ):
        assert calculate_dimensional_weight(value) == 0.0


def test_invalid_tracking_codes_return_sentinel():
    for value in (None, "", "E", "E12A", "12", "É123", "E１２３"):
        assert format_tracking_label(value) == "INVALID-000000"


def test_invalid_manifests_return_zero():
    for value in (
        None, "", "not json", "[]", "null", "{}", '{"other": 1}',
        '{"weight": true}', '{"weight": -1}', '{"weight": "heavy"}',
        '{"weight": NaN}', '{"weight": Infinity}',
    ):
        assert parse_package_manifest(value) == 0.0
