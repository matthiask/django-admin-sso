from django.contrib import admin

from django_sso import settings
from django_sso.models import Assignment, OpenIDUser


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'username', 'username_mode', 'domain',
                    'user', 'weight')
    list_editable = ('username', 'username_mode', 'domain', 'user', 'weight')

admin.site.register(Assignment, AssignmentAdmin)


class OpenIDUserAdmin(admin.ModelAdmin):
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url
        from django_sso.views import StartOpenIDView, FinishOpenIDView
        urls = super(OpenIDUserAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.module_name
        my_urls = patterns('',
            url(r'^start/$', StartOpenIDView.as_view(),
                name='%s_%s_start' % info),
            url(r'^end/$', FinishOpenIDView.as_view(),
                name='%s_%s_return' % info),
        )
        return my_urls + urls

admin.site.register(OpenIDUser, OpenIDUserAdmin)

if settings.DJANGO_SSO_ADD_LOGIN_BUTTON:
    admin.site.login_template = 'django_sso/login.html'
