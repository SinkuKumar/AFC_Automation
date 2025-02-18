"""
Error Codes: Specifies a list of error codes which can typically occur during automation script exectution.
"""

# Error Severity
MINOR = 1 # Can be fixed by user
MODERATE = 2 # L1/L2 Supervision required
CRITICAL = 3 # L3 Supervision required

# Selenium Error Codes
NO_BROWSER_INSTANCE = f"SEL_{CRITICAL}"

# Experity Error Codes
INVALID_CREDENTIALS = f"EXP_{MODERATE}"
PASSWORD_EXPIRY_FUTURE = f"EXP_{MINOR}"

# Database Error Codes
DB_CONNECTION = f"DB_{CRITICAL}"

# 
