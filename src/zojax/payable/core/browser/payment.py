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
"""

$Id$
"""
import os.path
from zope import schema, interface, event
from zope.lifecycleevent import ObjectCreatedEvent
from zope.dublincore.interfaces import ICMFDublinCore
from zope.app.pagetemplate import ViewPageTemplateFile

from zojax.layoutform import button, Fields, PageletAddForm, PageletEditForm
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.extensions.browser.extension import EditExtension

from zojax.payable.core.i18n import _
from zojax.payable.core.interfaces import PayableMarkerMap
from zojax.payable.core.payment import Payment
from zojax.table import table, column

class Extension(EditExtension):

    @property
    def fields(self):
        return Fields(self.context.__schema__, PayableMarkerMap[self.context.marker], omitReadOnly=True)

class PaymentForm(PageletAddForm):

    label = _(u'Payment Form')

    @button.buttonAndHandler(_(u'Checkout'))
    def handle_payment(self, data):
        data, errors = self.extractData()

        if errors:
            IStatusMessage(self.request).add(self.formErrorsMessage, 'error')
        else:
            context = self.context

            IStatusMessage(self.request).add(
                _(u'Payment has been done.'))
            self.redirect('index.html')

class NameColumn(column.Column):
    name = 'name'
    title = _(u'Name')
    weight = 100

    def query(self, default=None):
        return self.content.__name__

class Payments(table.Table):

    def initDataset(self):
        self.dataset = self.context.payments
