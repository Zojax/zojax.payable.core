##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import time
from zope import interface
from zope.location import Location, LocationProxy
from zope.component import getUtility, getMultiAdapter
from zope.interface.common.mapping import IEnumerableMapping

from zope.datetime import rfc1123_date
from zope.datetime import time as timeFromDateTimeString

from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import IBrowserPublisher

from zojax.payable.core.interfaces import IPayableExtension


class Payments(BrowserView, Location):
    interface.implements(IBrowserPublisher, IEnumerableMapping)

    __name__ = u'attachments'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.payments = IPayableExtension(context).payments

    def publishTraverse(self, request, name):
        attach = self.payments.get(name.lower())

        if attach is None:
            raise NotFound(self, name, request)

        return LocationProxy(attach, self, name)

    def browserDefault(self, request):
        return empty, ()

    def keys(self):
        return self.payments.keys()

    def __iter__(self):
        return iter(self.payments)

    def values(self):
        return self.payments.values()

    def items(self):
        return self.payments.items()

    def __len__(self):
        return len(self.payments)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __getitem__(self, name):
        configlet = IPayableExtension(self.context)

        attach = configlet.payments.get(name)

        if resource is None:
            raise KeyError(name)

        return LocationProxy(attach, self, name)
