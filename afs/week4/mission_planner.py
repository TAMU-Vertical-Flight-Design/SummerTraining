DROP_ALTITUDE_M = 18
SEARCH_PATTERN = "lawnmower"
FAILSAFE_MODE = "LOITER"


def choose_drop_zone(detections):
    """Return the highest-confidence drop zone candidate."""
    if not detections:
        return None
    return max(detections, key=lambda d: d.get("confidence", 0))

def is_candidate_usable(candidate):
    if candidate is None:
        return False
    return candidate.get("confidence", 0) >= 0.75


def mission_summary():
    return f"pattern={SEARCH_PATTERN}, drop_altitude_m={DROP_ALTITUDE_M}, failsafe={FAILSAFE_MODE}"


if __name__ == "__main__":
    print("AFS mission planner sanity check")
    print(mission_summary())

"""Return if drop zone is usable."""