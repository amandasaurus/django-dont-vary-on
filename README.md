django-dont-vary-on is a library to give you more control over Django's caching, and improving you cache hits and performance.

It gives you the ability to remove the ``Vary`` header part added by a django middleware.

Motivation and use cases
========================

For example, if you use [Django's Internationalization](https://docs.djangoproject.com/en/dev/topics/i18n/) to translate your pages, you need to add the 
[``django.middleware.locale.LocaleMiddleware``](https://docs.djangoproject.com/en/dev/ref/middleware/#django.middleware.locale.LocaleMiddleware) middleware, which will add ``Accept-Language`` to the ``Vary`` header of all your responses.

If you use Django's authorisation and session support (which everyone does), then ``Cookie`` will be added to your ``Vary`` header. If you have pages that don't change based on who is logged in, then you will get subpar cache performance.

Django include a [``vary_on_headers`` function](https://docs.djangoproject.com/en/dev/topics/cache/#using-vary-headers) which adds to the Vary header. This library is the compliment, it reduces the Vary header.

The ``Vary`` header
===================

The ``Vary`` HTTP response header is used by caching systems to know what HTTP request headers to cache this page based on. A typical Vary header might look like this: ``Vary: Accept-Language, Cookie``, which means that requests to that URL with the same ``Accept-Language`` and ``Cookie`` field can use the cached value. In this example, we say that "The page varies on 'Cookie' and 'Accept-Language'. It does not vary on 'User-Agent'".

Installation
============

    pip install django-dont-vary-on

To use it you *must* put ``RemoveUnneededVaryHeadersMiddleware`` in your ``MIDDLEWARE_CLASSES`` and it must be below ``UpdateCacheMiddleware`` and above other middleware classes. Ideally put it straight under ``UpdateCacheMiddleware``.

    MIDDLEWARE_CLASSES = ( 
        ….
        'django.middleware.cache.UpdateCacheMiddleware',
        'django_dont_vary_on.middleware.RemoveUnneededVaryHeadersMiddleware',
        …
    )

By default it does nothing unless you specifiy the views.

Usage
=====

By default it does nothing. You must manually mark views using decorators.

dont vary on
------------

This decorator will remove that key from the ``Vary`` header, so that this response 'won't vary on that'.


    from django_dont_vary_on.decorators import dont_vary_on

    @dont_vary_on("Accept-Language")
    def myview(request):
        …

You can specify multiple values

    @dont_vary_on("Accept-Language", "User-Agent")
    def myview(request):
        …


only vary on
------------

This is a more nuclear option, and the response will *only* vary the headers you mention. Any other vary header values will not be included, even if other middleware classes might add them.

    from django_dont_vary_on.decorators import only_vary_on

    @only_vary_on("Cookie")
    def myview(request):
        …

This view will have a ``Vary: Cookie`` header, nothing else in there. It will cache things based only on the 'Cookie' request header, no other request header.

You can specify multiple values:

    @only_vary_on("Accept-Language", "Cookie")
    def myview(request):
        …

Example use cases
=================

If you have a page that is the same for all logged in users and anonymous users, then you can use ``@dont_vary_on('Cookie')`` to cache that page for all users, and only generate it once.

If you have a page that generates JSON data, and it doesn't matter what language the user has, you can use ``@dont_vary_on('Accept-Language')`` to cache that page regardless of the language.


Caveats
=======

Sending an incorrect cached page can be very embarassing. People might be able to see other people's logged in and personal details. Ensure you know what you're doing.


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/rory/django-dont-vary-on/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

