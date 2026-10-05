def normalize_confidence(raw_score):
    """Convert a percent-style confidence value into a 0.0 to 1.0 score."""
    return max(0.0, min(raw_score / 100.0, 1.0))

def confidence_is_valid(score):    
    """Return True when normalized confidence is high enough for payload logic."""    
    return score >= 0.75
