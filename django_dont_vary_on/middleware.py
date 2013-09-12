# encoding: utf-8
import re

cc_delim_re = re.compile(r'\s*,\s*')


class RemoveUnneededVaryHeadersMiddleware(object):
    """
    Middleware that modifies the Vary header to optionally remove some values
    from the Vary header.

    This middleware should be used in conjunction with dont_vary_on or
    only_vary_on decorators. It should be just underneath the
    UpdateCacheMiddleware, so that the UpdateCacheMiddleware will use the new Vary header.

    Some pages/views don't depend on some vary headers that might be added
    (e.g. if you know a view don't Vary on the cookie). This allows much more
    finegrained control, on a view by view basis, of the Vary header, allowing
    for better cache performance.
    """

    def process_response(self, request, response):
        if len(getattr(response, 'only_vary_on', [])) > 0:
            response['Vary'] = ", ".join(sorted(set(response.only_vary_on)))
        elif len(getattr(response, 'dont_vary_on', [])) > 0:
            remove_vary_headers(response, response.dont_vary_on)
        else:
            # Nothing to do here
            pass

        return response


def remove_vary_headers(response, headers_to_remove):
    """
    Removes (if present) the "Vary" header in the given HttpResponse object.
    headers_to_remove is a list of header names that should not be in "Vary". Existing
    headers in "Vary" aren't removed.

    This is copied from, and inspired by, django.utils.cache.patch_vary_headers
    """
    # Note that we need to keep the original order intact, because cache
    # implementations may rely on the order of the Vary contents in, say,
    # computing an MD5 hash.
    if response.has_header('Vary'):
        vary_headers = cc_delim_re.split(response['Vary'])
    else:
        # This response has no vary header, so don't change anything
        return response

    new_headers = []

    # Use .lower() here so we treat headers as case-insensitive.
    headers_to_remove = [x.lower() for x in headers_to_remove]
    for existing_header in vary_headers:
        if existing_header.lower() not in headers_to_remove:
            new_headers.append(existing_header)
        else:
            # this existing header should not be included
            pass
    if len(new_headers) > 0:
        response['Vary'] = ', '.join(new_headers)
    else:
        del response['Vary'] # Remove header so that we're not left with blank header

