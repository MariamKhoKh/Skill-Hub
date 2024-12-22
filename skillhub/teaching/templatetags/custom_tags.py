from django import template

register = template.Library()


@register.filter
def range_from(value):
    try:
        # Convert float to int for the range
        return range(int(value))
    except (TypeError, ValueError):
        return range(0)


@register.filter
def remaining_stars(value):
    try:
        # Calculate remaining stars (5 minus the rounded value)
        return range(5 - int(float(value)))
    except (TypeError, ValueError):
        return range(5)
