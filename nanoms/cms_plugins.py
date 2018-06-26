from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from nanoms import views
from nanoms import forms

@plugin_pool.register_plugin
class BuildingPlugin(CMSPluginBase):
    module = 'NANO MS'
    render_template = "nanoms/building.html"
    name = 'Building Form'
    #cache = True

    def render(self, context, instance, placeholder):
        request = context['request']
        context.update({
            'form': forms.BuildingForm(),
        })
        return context

@plugin_pool.register_plugin
class ResidentPlugin(CMSPluginBase):
    module = 'NANO MS'
    render_template = "nanoms/resident.html"
    name = 'Resident Form'
    #cache = True

    def render(self, context, instance, placeholder):
        request = context['request']
        context.update({
            'form': forms.ResidentForm(),
        })
        return context

@plugin_pool.register_plugin
class DevicePlugin(CMSPluginBase):
    module = 'NANO MS'
    render_template = "nanoms/device.html"
    name = 'Device Form'
    #cache = True

    def render(self, context, instance, placeholder):
        request = context['request']
        context.update({
            'form': forms.DeviceForm(request=request),
        })
        return context
