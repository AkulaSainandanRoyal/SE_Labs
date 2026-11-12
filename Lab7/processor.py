import json
import math


def calculate_dimensional_weight(dimensions_str):
    """Calculate dimensional weight (kg) from an LxWxH string in cm.

    Invalid, non-positive, non-finite, or malformed dimensions return 0.0.
    """
    try:
        if not isinstance(dimensions_str, str):
            return 0.0

        parts = dimensions_str.strip().lower().split("x")
        if len(parts) != 3:
            return 0.0

        length, width, height = (float(part.strip()) for part in parts)
        if not all(math.isfinite(value) and value > 0
                   for value in (length, width, height)):
            return 0.0

        volume = length * width * height
        if not math.isfinite(volume):
            return 0.0

        result = round(volume / 5000.0, 2)
        return result if math.isfinite(result) else 0.0
    except (TypeError, ValueError, OverflowError):
        return 0.0


def format_tracking_label(raw_code):
    """Format an ASCII-letter + ASCII-digits tracking code.

    Invalid codes return the stable sentinel 'INVALID-000000'.
    """
    if not isinstance(raw_code, str) or len(raw_code) < 2:
        return "INVALID-000000"

    prefix, number = raw_code[0], raw_code[1:]
    if not prefix.isascii() or not prefix.isalpha():
        return "INVALID-000000"
    if not number.isascii() or not number.isdigit():
        return "INVALID-000000"

    try:
        tracking_num = int(number)
        return f"{prefix.upper()}-{tracking_num:06d}"
    except (TypeError, ValueError, OverflowError):
        return "INVALID-000000"


def parse_package_manifest(json_payload):
    """Return a valid non-negative finite manifest weight, else 0.0."""
    try:
        if not isinstance(json_payload, str):
            return 0.0

        data = json.loads(json_payload)
        if not isinstance(data, dict) or "weight" not in data:
            return 0.0

        raw_weight = data["weight"]
        if isinstance(raw_weight, bool):
            return 0.0

        weight = float(raw_weight)
        if not math.isfinite(weight) or weight < 0:
            return 0.0

        return weight
    except (json.JSONDecodeError, TypeError, ValueError, OverflowError):
        return 0.0


def main():
    print("==== Running calculate_dimensional_weight ====")
    dims_input = input("Enter dimensions LxWxH in cm (e.g. 20x30x10): ")
    print("Dimensional Weight (kg):", calculate_dimensional_weight(dims_input))

    print("\n==== Running format_tracking_label ====")
    code_input = input("Enter raw code (e.g. E123): ")
    print("Formatted Label:", format_tracking_label(code_input))

    print("\n==== Running parse_package_manifest ====")
    json_input = input('Enter manifest JSON (e.g. {"weight": 12.5}): ')
    print("Manifest Weight:", parse_package_manifest(json_input))


if __name__ == "__main__":
    main()
