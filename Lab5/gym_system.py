"""Manage fitness club class bookings and roster exports."""

import json
from pathlib import Path

# Default capacity for each class.
class_capacity = {"Yoga": 3, "HIIT": 2, "Spin": 4}
rosters = {}


def book_class(member_id, class_name, attendance_log=None):
    """Book a member if the class has available capacity."""
    if attendance_log is None:
        attendance_log = []

    if class_name not in rosters:
        rosters[class_name] = []

    if len(rosters[class_name]) >= class_capacity.get(class_name, 0):
        print(f"Class full: {class_name}")
        return False

    rosters[class_name].append(member_id)
    attendance_log.append(f"{member_id} -> {class_name}")
    return True


def cancel_booking(member_id, class_name):
    """Cancel an existing booking."""
    try:
        rosters[class_name].remove(member_id)
    except (KeyError, ValueError):
        print("Nothing to cancel")


def set_capacity(class_name, seats):
    """Set a class capacity, requiring a positive number of seats."""
    if seats <= 0:
        raise ValueError("Capacity must be positive")
    class_capacity[class_name] = seats


def add_members(class_name, count):
    """Add the requested number of guest bookings."""
    if count < 0:
        raise ValueError("Guest count cannot be negative")

    for index in range(count):
        book_class(f"GUEST-{index}", class_name)


def export_roster(file="gym_schedule.json"):
    """Export all class rosters to a JSON file."""
    with open(file, "w", encoding="utf-8") as output_file:
        json.dump(rosters, output_file, indent=2)


def clear_old_exports(prefix="old_"):
    """Delete matching old JSON exports from the current directory."""
    if "/" in prefix or "\\" in prefix or ".." in prefix:
        raise ValueError("Prefix must not contain a path")

    for path in Path(".").glob(f"{prefix}*.json"):
        if path.is_file():
            path.unlink()


def show_rosters():
    """Print all class rosters."""
    for class_name, members in rosters.items():
        print(f"{class_name}: {', '.join(str(member) for member in members)}")


def main():
    """Run the booking ledger demonstration."""
    book_class("M1", "Yoga")
    book_class("M2", "Yoga")
    book_class("M3", "Yoga")
    book_class("M4", "Yoga")
    book_class(55, "HIIT")
    book_class("M5", "Pilates")

    set_capacity("Spin", 2)
    add_members("Spin", 3)
    cancel_booking("M9", "Boxing")

    guest_input = input(
        "How many walk-in guests for HIIT? (Enter for 1): "
    ).strip() or "1"

    try:
        guest_count = int(guest_input)
        add_members("HIIT", guest_count)
    except ValueError:
        print("Please enter a non-negative whole number.")

    clear_old_exports()
    export_roster()
    show_rosters()


if __name__ == "__main__":
    main()
