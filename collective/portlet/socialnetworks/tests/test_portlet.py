import unittest2 as unittest

from zope.component import getUtility, getMultiAdapter

from plone.portlets import interfaces
from plone.app.portlets.storage import PortletAssignmentMapping

from collective.portlet.socialnetworks import socialnetworks
from collective.portlet.socialnetworks.tests.base import IntegrationTestCase


class IntegrationTestPortlet(IntegrationTestCase):

    def setUp(self):
        super(IntegrationTestPortlet, self).setUp()
        self.setRoles(('Manager', ))

    def test_portlet_type_registered(self):
        portlet = getUtility(
            interfaces.IPortletType,
            name='collective.portlet.socialnetworks.SocialNetworks')
        self.assertEquals(portlet.addview,
                          'collective.portlet.socialnetworks.SocialNetworks')

    def test_interfaces(self):
        # TODO: Pass any keyword arguments to the Assignment constructor
        portlet = socialnetworks.Assignment()
        self.assertTrue(interfaces.IPortletAssignment.providedBy(portlet))
        data = portlet.data
        self.assertTrue(interfaces.IPortletDataProvider.providedBy(data))

    def test_invoke_add_view(self):
        portlet = getUtility(
            interfaces.IPortletType,
            name='collective.portlet.socialnetworks.SocialNetworks')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        # TODO: Pass a dictionary containing dummy form inputs from the add
        # form.
        # Note: if the portlet has a NullAddForm, simply call
        # addview() instead of the next line.
        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0],
                                   socialnetworks.Assignment))

    def test_invoke_edit_view(self):
        # NOTE: This test can be removed if the portlet has no edit form
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = socialnetworks.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, socialnetworks.EditForm))

    def test_obtain_renderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(interfaces.IPortletManager,
                             name='plone.rightcolumn',
                             context=self.portal)

        # TODO: Pass any keyword arguments to the Assignment constructor
        assignment = socialnetworks.Assignment()

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment),
            interfaces.IPortletRenderer)
        self.failUnless(isinstance(renderer, socialnetworks.Renderer))


class IntegrationTestRenderer(IntegrationTestCase):

    def setUp(self):
        super(IntegrationTestRenderer, self).setUp()
        self.setRoles(('Manager', ))

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            interfaces.IPortletManager,
            name='plone.rightcolumn',
            context=self.portal)

        # TODO: Pass any default keyword arguments to the Assignment
        # constructor.
        assignment = assignment or socialnetworks.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment),
                               interfaces.IPortletRenderer)

    def test_render(self):
        # TODO: Pass any keyword arguments to the Assignment constructor.
        r = self.renderer(context=self.portal,
                          assignment=socialnetworks.Assignment())
        r = r.__of__(self.folder)
        r.update()
        #output = r.render()
        # TODO: Test output


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
