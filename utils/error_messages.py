"""
Error Codes: Specifies a list of error codes which can typically occur during automation script exectution.
"""
# Error Severity
MINOR = 1
MODERATE = 2
CRITICAL = 3

# Module Prefix
SELENIUM = "SEL"
EXPERITY = "EXP"

# Contact Message
CONTACT = "BI Automation Team - bi@graphxsys.com"

# Selenium Error Codes - MINOR
UNSUPPORTED_BROWSER = f"{SELENIUM}_{MINOR}_001"

# Selenium Error Codes - CRITICAL
BROWSER_INSTANCE_ISSUE = f"{SELENIUM}_{CRITICAL}_001"
NAVIGATION_FAILURE = f"{SELENIUM}_{CRITICAL}_002"

# Experity Error Codes - MINOR
PORTAL_ISSUE = f"{EXPERITY}_{MINOR}_001"
INVALID_CREDENTIALS = f"EXP_{MINOR}"
LOGOUT_ISSUE = f"{EXPERITY}_{MINOR}_002"

# Experity Error Codes - MODERATE
DATA_FETCH_ISSUE = f"{EXPERITY}_{MODERATE}_001"
REPORT_FILTER_SELECTION_ERROR = f"{EXPERITY}_{MODERATE}_002"

# Database Error Codes - CRITICAL
DB_CONNECTION = f"DB_{CRITICAL}"
