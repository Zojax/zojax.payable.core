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
Paid Content Support

$Id$
"""

from zope import interface, component
from zope.app.intid.interfaces import IIntIds

from getpaid.core import interfaces, item
from getpaid.core import options

from interfaces import IDonationLevel, IPayableMarker
import sessions
from zope.security.proxy import getObject

class LineItemFactory( object ):
    """
    adapts to cart and content (payable marker marked), and creates a line item
    from said item for cart.
    """

    def __init__( self, cart, content ):
        self.cart = cart
        self.content = content

    def create( self, quantity=1 ):

        if self.checkIncrementCart( self.content, quantity=quantity ):
            return

        payable = self.checkPayable( self.content )
        nitem = self.createLineItem( payable, quantity)
        self.cart[ nitem.item_id ] = nitem
        #not being able to set the came from does not seem a good reason to explode
        try:
            sessions.set_came_from_url(self.content)
        except:
            pass
        return nitem

    def checkIncrementCart( self, content, quantity=1 ):
        item_id = content.UID()
        if item_id in self.cart:
            self.cart[ item_id ].quantity += quantity
            return True

    def checkPayable( self, content):
        if not IPayableMarker.providedBy( content ):
            raise RuntimeError("Invalid Context For Cart Add")
        return interfaces.IPayable( content )

    def createLineItem( self, payable, quantity ):
        nitem = item.PayableLineItem()
        nitem.item_id = self.content.UID() # archetypes uid

        # we use intids to reference content that we can dereference cleanly
        # without access to context.
        nitem.uid = component.getUtility( IIntIds ).register( self.content )

        def getUnicodeString( s ):
            """Try to convert a string to unicode from utf-8, as this is what Archetypes uses"""
            if type( s ) is type( u'' ):
                # this is already a unicode string, no need to convert it
                return s
            elif type( s ) is type( '' ):
                # this is a string, let's try to convert it to unicode
                try:
                    return s.decode( 'utf-8' )
                except UnicodeDecodeError, e:
                    # not utf-8... return as is and hope for the best
                    return s

        # copy over information regarding the item
        nitem.name = getUnicodeString( self.content.Title() )
        nitem.description = getUnicodeString( self.content.Description() )
        nitem.cost = payable.price
        nitem.quantity = int( quantity )
        nitem.product_code = payable.product_code

        return nitem

class ShippableItemFactory( LineItemFactory ):

    def createLineItem( self, payable, quantity ):

        nitem = item.PayableShippableLineItem()
        nitem.item_id = self.content.UID() # archetypes uid

        # we use intids to reference content that we can dereference cleanly
        # without access to context.
        nitem.uid = component.getUtility( IIntIds ).register( self.content )

        # copy over information regarding the item
        nitem.name = self.content.Title()
        nitem.description = self.content.Description()
        nitem.cost = payable.price
        nitem.quantity = int( quantity )
        nitem.product_code = payable.product_code
        nitem.weight = float( payable.weight )

        return nitem


class BaseContentExtensionAdapter(object):

    def __init__(self, context):
        self.context = getObject(context.context)

#################################
# Buyable Content

"""
when buyable content is deleted, we still want to be able to keep a reference to it
for those who have paid, or at least replace any shopping cart / transaction references
with information.
"""

BuyableContentStorage = options.PersistentOptions.wire( "BuyableContentStorage", "getpaid.content.buyable", interfaces.IBuyableContent )

class BuyableContentAdapter( BuyableContentStorage ):
    """
    Default Adapter between Content and IBuyable. This implementation stores attributes
    of a buyable in an annotation adapter
    """
    interface.implements( interfaces.IBuyableContent )

    def __init__( self, context ):
        self.context = context

class BuyableContentExtensionAdapter(BaseContentExtensionAdapter, BuyableContentAdapter):
    pass

#################################
# Shippable Content
"""
shippable deletions need to track orders not shipped
"""

ShippableContentStorage = options.PersistentOptions.wire( "ShippableContentStorage", "getpaid.content.shippable", interfaces.IShippableContent )

class ShippableContentAdapter( ShippableContentStorage ):

    interface.implements( interfaces.IShippableContent )

    def __init__( self, context ):
        self.context = context

class ShippableContentExtensionAdapter(BaseContentExtensionAdapter, ShippableContentAdapter):
    pass

#################################
# Premium Content

PremiumContentStorage = options.PersistentOptions.wire( "PremiumContentStorage", "getpaid.content.buyable", interfaces.IPremiumContent )

class PremiumContentAdapter( PremiumContentStorage ):

    interface.implements( interfaces.IPremiumContent )

    def __init__( self, context ):
        self.context = context

class PremiumContentExtensionAdapter(BaseContentExtensionAdapter, PremiumContentAdapter):
    pass

#################################
# Donatable Content

"""
"""

DonatableContentStorage = options.PersistentOptions.wire( "DonatableContentStorage", "getpaid.content.donate", interfaces.IDonationContent )

class DonationLevel( object ):

    interface.implements( IDonationLevel )

    title = ''
    amount = 0

class DonatableContentAdapter( DonatableContentStorage ):
    """
    Default Adapter between Content and IDonationContent. This implementation stores attributes
    of a donate-able in an annotation adapter
    """
    interface.implements( interfaces.IDonationContent )

    def __init__( self, context ):
        self.context = context

class DonatableContentExtensionAdapter(BaseContentExtensionAdapter, DonatableContentAdapter):
    pass
