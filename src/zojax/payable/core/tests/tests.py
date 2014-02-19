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
import unittest, os.path
from zojax.portal.instance import Portal
from zope.app.component.site import LocalSiteManager
from zope.testing import doctest
from zope.app.testing import functional
from zope.app.rotterdam import Rotterdam
from zope.app.component.hooks import setSite
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.catalog.catalog import Catalog, ICatalog
from zojax.personal.space.manager import PersonalSpaceManager, IPersonalSpaceManager
from zope import interface, event
from zojax.folder.folder import Folder
from zojax.folder.interfaces import IFolder
from zope.lifecycleevent import ObjectCreatedEvent
from zojax.content.space.content import ContentSpace


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


payableLauer = functional.ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'payableLauer', allow_teardown=True)


class TestFolder(Folder):
    interface.implements(IFolder)



def setUp(test):
    root = functional.getRootFolder()
    setSite(root)
    root['intids'] = IntIds()
    root['intids'].register(root)
    root.getSiteManager().registerUtility(root['intids'], IIntIds)

    catalog = Catalog()
    root['catalog'] = catalog
    root.getSiteManager().registerUtility(root['catalog'], ICatalog)

    manager = PersonalSpaceManager()
    root['people'] = manager
    root.getSiteManager().registerUtility(root['people'], IPersonalSpaceManager)

    folder = Folder('Folder')
    event.notify(ObjectCreatedEvent(folder))
    root['folder'] = folder

    portal = Portal()
    event.notify(ObjectCreatedEvent(portal))
    root['portal'] = portal
    root['portal'].setSiteManager(LocalSiteManager(portal))

    space = ContentSpace(title=u'Space')
    event.notify(ObjectCreatedEvent(space))
    root['space'] = space



def FunctionalDocFileSuite(*paths, **kw):
    if 'layer' in kw:
        layer = kw['layer']
        del kw['layer']
    else:
        layer = functional.Functional

    globs = kw.setdefault('globs', {})
    globs['http'] = functional.HTTPCaller()
    globs['getRootFolder'] = functional.getRootFolder
    globs['sync'] = functional.sync

    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')
    def setUp(test):
        functional.FunctionalTestSetup().setUp()

        if kwsetUp is not None:
            kwsetUp(test)
    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        if kwtearDown is not None:
            kwtearDown(test)
        functional.FunctionalTestSetup().tearDown()
    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old
                             | doctest.ELLIPSIS
                             | doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = layer
    return suite


def test_suite():
    return unittest.TestSuite((
            FunctionalDocFileSuite(
                './tests.txt', setUp=setUp, layer = payableLauer),))
