##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
""" zojax.payable.core interfaces

$Id$
"""
from zope import schema, interface
from zope.app.container.interfaces import IContainer

from i18n import _
from getpaid.core import interfaces as igetpaid

class IPayableProduct(interface.Interface):
    """ product """

    methods = schema.List(
        title = _(u'Payment methods'),
        description = _(u'Active payment methods.'),
        required = True,
        default = [],
        value_type = schema.Choice(title = _(u'Payment method'),
                                   vocabulary="zojax.payable.core.PaymentMethods")
                                   )

class IPayment(interface.Interface):
    """ attachment """

    title = schema.TextLine(
        title = _(u'Title'),
        description = _(u'Attachment title.'),
        default = u'',
        missing_value = u'',
        required = False)

    description = schema.Text(
        title = _(u'Description'),
        description = _(u'Attachment description.'),
        default = u'',
        missing_value = u'',
        required = False)

class IBaseExtension(interface.Interface):
    """ payable extension """

    enabled = schema.Bool(
        title = _(u'Enable'),
        description = _(u'Enable extension for this object.'),
        default = False,
        required = False)

class IBuyableExtension(IBaseExtension):
    """ buyable extension """

class IDonatableExtension(IBaseExtension):
    """ donatable extension """

class IPremiumExtension(IBaseExtension):
    """ premiumable extension """

class IShippableExtension(IBaseExtension):
    """ shippable extension """

class IShoppingUtilityCartType(interface.Interface):
    """ shopping cart utility type """

class IPayableMarker(interface.Interface):
    """ marker interface added to any payable content """

class IBuyableMarker(IPayableMarker):
    """ marker interface added to buyable content """

class IPremiumMarker(IPayableMarker):
    """ marker interface added to premium content """

class IShippableMarker(IPayableMarker):
    """ shippable interface added to shippable content """

class IDonatableMarker(IPayableMarker):
    """ donate-able interface added to shippable content """

class IDonationLevel(interface.Interface):

    title = schema.TextLine( title=_(u"Donation Level Name"))
    amount = schema.Int( title=_(u"Amount"))

class IEnhancedDonation(igetpaid.IDonationContent):

    donation_levels  = schema.List( title=_(u"Donation Levels"),
                                    value_type=schema.Object(IDonationLevel),
                                    required=False,
                                    default=list() )

PayableMarkers = [IBuyableMarker, IPremiumMarker, IShippableMarker, IDonatableMarker]

PayableMarkerMap = dict(
     (
      (IBuyableMarker, igetpaid.IBuyableContent),
      (IPremiumMarker, igetpaid.IPremiumContent),
      (IShippableMarker, igetpaid.IShippableContent),
      (IDonatableMarker, igetpaid.IDonationContent)
    )
)
