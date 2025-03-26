"""
Error Codes Module

This module defines a set of error codes that can occur during automation script execution.
Each error code is categorized by severity level and module type.

Constants:
    - Error Severity Levels: MINOR, MODERATE, CRITICAL
    - Module Prefixes: SELENIUM, EXPERITY, DATABASE
    - Contact Information: CONTACT
    - Specific Error Codes for Selenium, Experity, and Database operations
"""

# Error Severity Levels
MINOR = 1
MODERATE = 2
CRITICAL = 3

# Module Prefixes
SELENIUM = "SEL"
EXPERITY = "EXP"
DATABASE = "DB"

# Contact Information
CONTACT = "BI Automation Team - bi@graphxsys.com"

# Selenium Error Codes - MINOR
UNSUPPORTED_BROWSER = f"{SELENIUM}_{MINOR}_001"

# Selenium Error Codes - CRITICAL
BROWSER_INSTANCE_ISSUE = f"{SELENIUM}_{CRITICAL}_001"
NAVIGATION_FAILURE = f"{SELENIUM}_{CRITICAL}_002"

# Experity Error Codes - MINOR
PORTAL_ISSUE = f"{EXPERITY}_{MINOR}_001"
INVALID_CREDENTIALS = f"{EXPERITY}_{MINOR}_002"
LOGOUT_ISSUE = f"{EXPERITY}_{MINOR}_003"

# Experity Error Codes - MODERATE
DATA_FETCH_ISSUE = f"{EXPERITY}_{MODERATE}_001"
REPORT_FILTER_SELECTION_ERROR = f"{EXPERITY}_{MODERATE}_002"

# Database Error Codes - CRITICAL
DB_CONNECTION = f"{DATABASE}_{CRITICAL}_001"
DATA_LOAD_ISSUE = f"{DATABASE}_{CRITICAL}_002"
