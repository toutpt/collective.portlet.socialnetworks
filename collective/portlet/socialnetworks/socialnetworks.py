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
    facebook_icon = schema.Choice(title=_(u"Facebook icon"),
                          vocabulary="collective.socialicons.facebook",
                          default="classic-3d-graphics-vibe/facebook-64px.png")
    googlep = schema.URI(title=_(u"Google + URL"), required=False)
    googlep_icon = schema.Choice(title=_(u"googlep icon"),
                          vocabulary="collective.socialicons.googleplus",
                          default="classic-3d-graphics-vibe/google-64px.png")
    linkedin = schema.URI(title=_(u"Linkedin URL"), required=False)
    linkedin_icon = schema.Choice(title=_(u"linkedin icon"),
                          vocabulary="collective.socialicons.linkedin",
                          default="classic-3d-graphics-vibe/linkedin-64px.png")
    twitter = schema.URI(title=_(u"Twitter URL"), required=False)
    twitter_icon = schema.Choice(title=_(u"twitter icon"),
                          vocabulary="collective.socialicons.twitter",
                          default="classic-3d-graphics-vibe/twitter-64px.png")
    youtube = schema.URI(title=_(u"Youtube URL"), required=False)
    youtube_icon = schema.Choice(title=_(u"youtube icon"),
                          vocabulary="collective.socialicons.youtube",
                          default="classic-3d-graphics-vibe/youtube-64px.png")
    rss = schema.URI(title=_(u"RSS URL"), required=False)
    rss_icon = schema.Choice(title=_(u"rss icon"),
                          vocabulary="collective.socialicons.rss",
                          default="classic-3d-graphics-vibe/rss-64px.png")


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ISocialNetworks)

    def __init__(self, header=u"",
                 facebook="",
                 facebook_icon="",
                 googlep="",
                 googlep_icon="",
                 linkedin="",
                 linkedin_icon="",
                 twitter="",
                 twitter_icon="",
                 youtube="",
                 youtube_icon="",
                 rss="",
                 rss_icon=""):
        self.header = header
        self.facebook=facebook
        self.facebook_icon=facebook_icon
        self.googlep=googlep
        self.googlep_icon=googlep_icon
        self.linkedin=linkedin
        self.linkedin_icon=linkedin_icon
        self.twitter=twitter
        self.twitter_icon=twitter_icon
        self.youtube=youtube
        self.youtube_icon=youtube_icon
        self.rss=rss
        self.rss_icon=rss_icon

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
