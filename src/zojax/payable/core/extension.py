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
from zope import interface
from BTrees.OOBTree import OOBTree
from zope.location import LocationProxy
from zope.publisher.interfaces import NotFound
from z3c.traverser.interfaces import ITraverserPlugin
import interfaces
from rwproperty import getproperty, setproperty
from zope.proxy import removeAllProxies

class BaseExtension(object):

    marker = None

    @getproperty
    def enabled(self):
        return self.marker.providedBy(self.context)

    @setproperty
    def enabled(self, value):
        context = removeAllProxies(self.context)
        if value:
            interface.alsoProvides(context, self.marker)
        else:
            if self.marker in interface.directlyProvidedBy(context):
                interface.noLongerProvides(context, self.marker)

class BuyableExtension(object):
    interface.implements(interfaces.IBuyableExtension)
    marker = interfaces.IBuyableMarker

class DonatableExtension(object):
    interface.implements(interfaces.IDonatableExtension)
    marker = interfaces.IDonatableMarker

class PremiumExtension(object):
    interface.implements(interfaces.IPremiumExtension)
    marker = interfaces.IPremiumMarker

class ShippableExtension(object):
    interface.implements(interfaces.IShippableExtension)
    marker = interfaces.IShippableMarker

class TraverserPlugin(object):
    interface.implements(ITraverserPlugin)

    def __init__(self, container, request):
        self.context = container
        self.request = request

    def publishTraverse(self, request, name):
        try:
            subob = self.context.payments.get(name)
        except:
            subob = None

        if subob is None:
            raise NotFound(self.context, name, request)

        return LocationProxy(subob, self.context, name)
