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
from pytz import utc
from datetime import datetime

from zope import interface
from zojax.product.utils import registerUtility, unregisterUtility
from zojax.folder.folder import Folder
from getpaid.core.interfaces import IOrderManager, IStore, IShoppingCartUtility, StoreInstalled, StoreUninstalled
from getpaid.core.order import OrderManager
from cart import ShoppingCartUtility
from getpaid.core.payment import CREDIT_CARD_TYPES
from interfaces import IPayableProduct
from zope.event import notify

class PayableProduct(object):
    interface.implements(IPayableProduct)

    def install(self):
        super(PayableProduct, self).install()
        if self.__installed__:
            notify( StoreInstalled( self ) )

    def update(self):
        super(PayableProduct, self).update()
        if self.__installed__:
            folder = registerUtility('payable', Folder, [(IStore, '')])
            interface.alsoProvides(folder, IStore)
            orderManager = registerUtility('ordermanager', OrderManager, [(IOrderManager, '')], folder)
            cartutility = registerUtility('cartutility', ShoppingCartUtility, [(IShoppingCartUtility, '')], folder)


    def uninstall(self):
        super(PayableProduct, self).uninstall()
        unregisterUtility('cartutility', [(IShoppingCartUtility, '')])
        unregisterUtility('ordermanager', [(IOrderManager, '')])
        unregisterUtility('payable', [(IStore, '')])
        notify( StoreUninstalled( self ) )
