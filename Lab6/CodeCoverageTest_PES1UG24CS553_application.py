import pytest
from shipping_quote import process_shipments, monitor_container_pressures


def test_invalid_shipments():
    with pytest.raises(ValueError):
        process_shipments("invalid", 10)


def test_negative_handling_fee():
    with pytest.raises(ValueError):
        process_shipments([], -1)


def test_unapproved_manifest_is_skipped():
    result = process_shipments(
        [{"manifest_approved": False, "packages": [{"weight_kg": 10}]}], 10
    )
    assert result == {"total_quote": 0.0, "status": "NO_CARGO"}


def test_air_shipment():
    result = process_shipments(
        [{"manifest_approved": True, "mode": "air",
          "packages": [{"weight_kg": 10}]}], 20
    )
    assert result["total_quote"] == 140.0


def test_unsupported_transport_mode():
    result = process_shipments(
        [{"manifest_approved": True, "mode": "sea"}], 10
    )
    assert result["status"] == "NO_CARGO"


def test_invalid_package_weight():
    result = process_shipments(
        [{"manifest_approved": True, "packages": [{"weight_kg": 0}]}], 10
    )
    assert result["status"] == "CLEARED"


def test_hazmat_non_fragile():
    result = process_shipments(
        [{"manifest_approved": True,
          "packages": [{"weight_kg": 10, "is_hazmat": True}]}], 20
    )
    assert result["total_quote"] == 70.0


def test_hazmat_fragile():
    result = process_shipments(
        [{"manifest_approved": True, "is_fragile": True,
          "packages": [{"weight_kg": 10, "is_hazmat": True}]}], 20
    )
    assert result["total_quote"] == 0.0


def test_heavy_package():
    result = process_shipments(
        [{"manifest_approved": True,
          "packages": [{"weight_kg": 40}]}], 20
    )
    assert result["total_quote"] == 260.0


def test_express_priority():
    result = process_shipments(
        [{"manifest_approved": True, "express_priority": True,
          "packages": [{"weight_kg": 10}]}], 20
    )
    assert result["total_quote"] == 75.0


def test_flagged_review_after_four_rejections():
    result = process_shipments(
        [{"manifest_approved": True,
          "packages": [{"weight_kg": 0} for _ in range(4)]}], 10
    )
    assert result["status"] == "FLAGGED_REVIEW"


def test_empty_pressure_logs():
    assert monitor_container_pressures([]) == "NO_DATA"


def test_stable_pressure_logs():
    assert monitor_container_pressures([[15.0, 16.0, 14.0]]) == "STABLE"


def test_single_low_pressure_is_not_a_leak():
    assert monitor_container_pressures([[13.0, 15.0]]) == "STABLE"


def test_consecutive_low_pressure_detects_leak():
    assert monitor_container_pressures([[13.0, 12.0]]) == "LEAK_DETECTED"
