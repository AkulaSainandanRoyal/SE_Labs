import json
from  pathlib import Path

# Global state
class_capacity = {"Yoga": 3, "HIIT": 2, "Spin": 4}
rosters = {}

def book_class(member_id, class_name, attendance_log=None):
    """Book a member into a class if capacity permits."""
    if attendance_log is None:
        attendance_log = []
    if class_name not in rosters:
        rosters[class_name] = []
    if len(rosters[class_name]) >= class_capacity.get(class_name, 0):
        print("Class full:", class_name)
        return False
    rosters[class_name].append(member_id)
    attendance_log.append("%s -> %s" % (member_id, class_name))
    return True

def cancel_booking(member_id, class_name):
    """Cancel a member booking if it exists."""
    try:
        rosters[class_name].remove(member_id)
    except (KeyError, ValueError):
        print("Nothing to cancel")

def set_capacity(class_name, seats):
    """Set a positive capacity for a class."""
    if seats <= 0:
        raise ValueError("Capacity must be positive")
    """Set a positive capacity for a class."""
    if seats <= 0:
        raise ValueError("Capacity must be positive")
    class_capacity[class_name] = seats

def add_members(class_name, count):
    """Add a specified number of guest bookings."""
    for i in range(count):
        book_class("GUEST-" + str(i), class_name)

def export_roster(file="gym_schedule.json"):
    """Export class rosters as JSON."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(rosters, f, indent=2)

def clear_old_exports(prefix="old_"):
    """Delete matching old JSON exports in the current directory."""
    for path in Path(".").glob(f"{prefix}*.json"):
        if path.is_file():
            path.unlink()

def show_rosters():
    """Print all current class rosters."""
    """Print all current class rosters."""
    for c in rosters:
        print(c, ":", ", ".join(str(m) for m in rosters[c]))

def main():
    """Run the booking ledger demonstration."""
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
    n = input("How many walk-in guests for HIIT? (Enter for 1): ") or "1"
    add_members("HIIT", int(n))
    clear_old_exports()
    export_roster()
    show_rosters()

main()
