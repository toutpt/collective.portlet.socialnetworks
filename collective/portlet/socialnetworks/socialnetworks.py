from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.portlet.socialnetworks import SocialNetworksMessageFactory as _


class ISocialNetworks(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    header = schema.TextLine(title=_(u"Header"),
                             required=True)

    facebook = schema.URI(title=_(u"Facebook page URL"), required=False)
    googlep = schema.URI(title=_(u"Google + URL"), required=False)
    linkedin = schema.URI(title=_(u"Linkedin URL"), required=False)
    twitter = schema.URI(title=_(u"Twitter URL"), required=False)
    youtube = schema.URI(title=_(u"Youtube URL"), required=False)
    rss = schema.URI(title=_(u"RSS URL"), required=False)

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ISocialNetworks)

    def __init__(self, header=u"",
                 facebook="",
                 googlep="",
                 linkedin="",
                 twitter="",
                 youtube="",
                 rss=""):
        self.header = header
        self.facebook=facebook
        self.googlep=googlep
        self.linkedin=linkedin
        self.twitter=twitter
        self.youtube=youtube
        self.rss=rss

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return self.header


class Renderer(base.Renderer):
    """Portlet renderer.
    """

    render = ViewPageTemplateFile('socialnetworks.pt')

    def site_url(self):
        if not hasattr(self, '_site_url'):
            self._site_url = self.context.portal_url()
        return self._site_url


class AddForm(base.AddForm):
    """Portlet add form.
    """
    form_fields = form.Fields(ISocialNetworks)

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form.
    """
    form_fields = form.Fields(ISocialNetworks)
