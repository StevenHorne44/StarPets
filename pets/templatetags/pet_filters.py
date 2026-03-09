from django import template
from django.utils.safestring import mark_safe

#registering the template library
register = template.Library()

@register.filter(name='draw_stars')
def draw_stars(stars):
    #try to convert the input to an integer, if it fails, default to 0
    try:
        stars = int(stars)
    except (ValueError, TypeError):
        stars = 0
    #ensure stars is between 0 and 5
    stars = max(0, min(stars, 5))
    
    empty = 5 - stars
    
    #create the HTML for filled and empty stars
    filled_html = "⭐" * stars
    empty_html = f'<span style="color:#e5e7eb">{"⭐" * empty}</span>'
    
    #combine the filled and empty stars into a single HTML string
    html = f'''
        <strong style="color: #374151;">Rating:</strong> 
        <span style="color: #f59e0b; letter-spacing: 2px;">{filled_html}{empty_html}</span> 
        <span style="color: #6b7280; font-weight: bold; margin-left: 5px;">({stars}/5)</span>
    '''
    
    return mark_safe(html)