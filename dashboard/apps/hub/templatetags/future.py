# templatetags/future.py
from django.template import Library
from django.template.defaulttags import url as _url

register = Library()


@register.tag
def url(*args, **kwargs):
    """
    A stub to get Django Admin Bootstrapped to work since `url` tag
    has been moved from `future` to `defaulttags`.
    """
    return _url(*args, **kwargs)
