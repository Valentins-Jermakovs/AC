# =========================
# IMPORTS
# =========================
import bleach

# =========================
# MODULE DESCRIPTION
# =========================
"""
HTML Cleaning Utility

This module contains a helper function to sanitize HTML content.

Purpose:
- Remove unsafe HTML tags
- Prevent XSS attacks
- Allow only safe formatting tags
- Return cleaned HTML content

Library used:
- bleach → HTML sanitizing library
"""

# ================================================
# Clean HTML Function
# ================================================
# This function sanitizes HTML input.
# It removes unsafe tags and keeps only allowed ones.
#
# Parameters:
# html (str) → raw HTML content
#
# Returns:
# str → cleaned and safe HTML
# ================================================

async def clean_html(html):

    # Clean HTML using bleach
    # Only allowed tags will remain
    # Everything else will be removed
    return bleach.clean(
        html,

        # Allowed HTML tags
        tags=[
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',  # headings
            'p',                                 # paragraph
            'b', 'i',                            # basic formatting
            'ul', 'ol', 'li',                    # lists
            'a',                                 # links
            'code',                              # code blocks
            'img'                                # images
        ],

        # Remove disallowed tags completely
        strip=True
    )