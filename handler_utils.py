import os

from google.appengine.api import memcache
from google.appengine.ext.webapp import template

from django.utils import simplejson

import settings

def renderToResponse(handler_instance, template_name, context={}):
    rendered_page = None
    base_context = {
        'DEBUG'     : settings.DEBUG,
        'VERSION'   : settings.VERSION
    }
    if settings.CACHE:
        key = "%s-%s" % (settings.VERSION, template_name)
        cached_data = memcache.get(key)
        if cached_data is not None:
            rendered_page = cached_data

    if rendered_page is None:
        path = os.path.join(settings.TEMPLATE_DIR, template_name)
        base_context.update(context)
        rendered_page = template.render(path, base_context)

    if settings.CACHE:
        memcache.set(key, rendered_page, settings.CACHE_LIFE)

    handler_instance.response.out.write(rendered_page)

def jsonResponse(handler_instance, data):
    handler_instance.response.headers['Content-Type'] = 'application/javascript'
    handler_instance.response.out.write(simplejson.dumps(data))