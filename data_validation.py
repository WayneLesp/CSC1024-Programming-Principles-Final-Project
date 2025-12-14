# ---------- Data Validators ----------
def validate_id(input_id):
    """Ensure ID has no spaces and not empty."""
    return input_id.strip() != "" and " " not in input_id


def validate_email(email):
    """Basic email validation."""
    return "@" in email and "." in email and not email.endswith("@")


def validate_marks(marks):
    """Ensure Marks are numeric and within range."""
    try:
        m = float(marks)
        return 0 <= m <= 100
    except:
        return False
