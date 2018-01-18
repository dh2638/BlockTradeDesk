from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator


class AjaxableResponseMixin(object):
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        data = {
            'errors': form.dict_errors()
        }
        return JsonResponse(data, status=400)

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        data = {
            'message': self.get_success_message()
        }
        if hasattr(self, 'get_success_url') or hasattr(self, 'success_url'):
            data.update({'redirect_url': self.get_success_url()})
        return JsonResponse(data, status=200)

    def get_success_message(self):
        return self.success_message

    def get_success_url(self):
        if hasattr(self, 'success_url') and self.success_url:
            return self.success_url
        return super(AjaxableResponseMixin, self).get_success_url()


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


def groupby_queryset_with_fields(queryset, fields):
    fields_qs = {}
    from itertools import groupby

    for field in fields:
        queryset = queryset.order_by(field)

        def getter(obj):
            related_names = field.split('__')
            for related_name in related_names:
                try:
                    obj = getattr(obj, related_name)
                except AttributeError:
                    obj = None
            return obj

        fields_qs[field] = [{'grouper': key, 'list': list(group)} for key, group in
                            groupby(queryset, lambda x: getattr(x, field)
                            if '__' not in field else getter(x))]
    return fields_qs
