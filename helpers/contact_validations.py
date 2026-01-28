import re
# --- Helper Validation Functions ---
def validate_full_name(name: str = "") -> tuple[bool, str]:
    """
    Validates the user_name based on:
    - Only latin alphabetic letters and spaces.
    - No leading spaces.
    - No special characters.
    - Length: 2 > l <= 30
    :param str name:
    :return tuple[bool, str]:
    """
    if not name:
        return False, "Name cannot be empty."

    # 1. Check for leading or trailing spaces
    if name != name.strip():
        return False, "Name cannot contain leading or trailing spaces."

    # 2. Regex: ^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$
    # This allows Latin letters (including accents and ñ) and spaces only.
    pattern = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$"
    if not re.match(pattern, name):
        return False, "Name can only contain Latin letters and spaces (no special characters)."

    # 3. Length validation
    if len(name) <= 2 or len(name) > 30:
        return False, "Invalid Name name cannot contain less than 2 characters or more than 30 characters."

    return True, ""

def validate_email(email: str = "") -> tuple[bool, str]:
    """
    Validates the email input based on:
    - No leading or trailing spaces.
    - Must contain '@'.
    - Must contain a valid domain structure (e.g., domain.com).
    - Length: 2 > l <= 30
    :param str email:
    :return tuple[bool, str]:
    """
    if not email:
        return False, "Email cannot be empty."

    # 2. Check for leading or trailing spaces
    if email != email.strip():
        return False, "Email address cannot contain leading or trailing spaces."

    # 3. Robust Regex for email structure:
    # - Start with alphanumeric/common symbols
    # - Must have @
    # - Must have a domain with at least one dot
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_pattern, email):
        return False, "Please enter a valid email address with a domain (e.g., user@example.com)."

    # 3. Length validation
    if not ( 2 <= len(email) <= 30):
        return False, "Invalid Name name cannot contain less than 2 characters or more than 30 characters."

    return True, ""

def validate_phone(phone: str) -> tuple[bool, str]:
    """
    Validates the phone input based on:
    - No leading or trailing spaces.
    - Must only number, empty spaces and special characters "(", ")" and "-"
    - Length: 10 > l <= 12
    :param phone:
    :return tuple[bool, str]:
    """
    if not phone:
        return False, "Phone number cannot be empty."

    # 1. Check for leading or trailing spaces
    if phone != phone.strip():
        return False, "Phone number cannot contain leading or trailing spaces."

    # 2. Check for allowed characters only (numbers, spaces, (, ), -, +)
    # Pattern: ^[0-9\s\(\)\-]+$
    if not re.match(r"^[0-9\s\(\)\-\+]+$", phone):
        return False, "Phone contains invalid characters. Only numbers, spaces, and ()- are allowed."

    # 3. Validate length of actual digits (excluding formatting characters)
    digits_only = re.sub(r"\D", "", phone) # Remove everything that isn't a digit
    if not (10 <= len(digits_only) <= 12):
        return False, "Phone number must contain between 10 and 12 digits."

    return True, ""

def validate_service_type_selector(service_type: str) -> tuple[bool, str]:
    """
    - Validates that the selected service type is one of the allowed options.
    - Matches the 'value' attributes in the HTML select element.
    :param service_type:
    :return tuple[bool, str]:
    """
    allowed_services = [
        "Web App",
        "Android App",
        "iOS App",
        "Embedded System App",
        "QA Services"
    ]

    if not service_type:
        return False, "Please select a service type."

    if service_type not in allowed_services:
        return False, "Invalid service type selected. Please choose from the provided options."

    return True, ""

def validate_project_name(project_name: str) -> tuple[bool, str]:
    """
    Validates the project name based on:
    - Letters a-z, A-Z and numbers 0-9
    - Length 5 > l <= 30
    :param project_name:
    :return tuple[bool, str]:
    """
    if not project_name:
        return False, "Project name cannot be empty."

    pattern = r"^[a-zA-Z0-9 ]+$"
    if not re.match(pattern, project_name):
        return False, "Project name must contain only standard Latin letters, numbers, and spaces. Special characters or non-Latin alphabets are not allowed."

    if not ( 5 <= len(project_name) <= 30):
        return False, "Project name must contain between 5 and 30 characters."

    return True, ""

def validate_project_description(project_description: str) -> tuple[bool, str]:
    """
    Validates the project description based on:
    - Letters a-z, A-Z and numbers 0-9
    - Length l <= 100
    :param project_description:
    :return tuple[bool, str]:
    """
    if not project_description:
        return False, "Project description cannot be empty."

    if not ( 1 <= len(project_description) <= 101):
        return False, "Project name must contain between 5 and 10 characters."

    return True, ""
