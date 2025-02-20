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
UNSUPPORTED_BROWSER = f"{SELENIUM}_{MINOR}001"

# Selenium Error Codes - CRITICAL
BROWSER_INSTANCE_ISSUE = f"{SELENIUM}_{CRITICAL}001"

# Experity Error Codes - MINOR
INVALID_CREDENTIALS = f"EXP_{MINOR}"

# Database Error Codes - CRITICAL
DB_CONNECTION = f"DB_{CRITICAL}"

# 
