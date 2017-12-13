from django import forms
from django.template.defaultfilters import striptags
from django.utils.translation import ugettext_lazy as _


class DictErrorMixin(forms.BaseForm):
    def __init__(self, *args, **kwargs):
        super(DictErrorMixin, self).__init__(*args, **kwargs)
        if hasattr(self, 'required_fields'):
            for field in self.required_fields:
                self.fields[field].required = True

    def dict_errors(self, strip_tags=True):
        errors = {}
        flag = False
        if self.prefix:
            self.prefix += "-"
        for error in self.errors.iteritems():
            prefix_key = self.prefix if self.prefix else ""
            errors[prefix_key + error[0]] = _(
                striptags(error[1]) if strip_tags else error[1]
            )
            if error[0] == '__all__':
                flag = True
        if not flag:
            errors['error_message'] = self.get_general_error_message()
        return errors

    def get_general_error_message(self):
        return _('Check the fields for errors.')

    def form_id(self):
        return self.__class__.__name__.lower()

    def form_btn_id(self):
        return "{0}-btn".format(self.form_id())
