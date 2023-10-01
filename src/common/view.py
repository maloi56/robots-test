from django.core.exceptions import PermissionDenied


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class RoleMixin:
    role = None

    def get(self, request, *args, **kwargs):
        if request.user.role != self.role:
            raise PermissionDenied
        return super().get(request, *args, **kwargs)
