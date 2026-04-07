import bleach

'''
This module contains a function to clean HTML content.

It uses the bleach library to remove unsafe HTML elements and attributes.
And the strip parameter to remove any leading or trailing whitespace.
After all the cleaning is done, the function returns the cleaned HTML.
'''

# ================================================
# Clean HTML
# ================================================
async def clean_html(html):
    return bleach.clean(
        html,
        tags=[
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'p', 'b', 'i', 'ul', 'ol', 'li',
            'a', 'code', 'img'
        ],
        strip=True
    )