from django.views.generic import TemplateView


class MeView(TemplateView):
    """
    Представление страницы пользователя.

    Основная логика:
    - Рендерит страницу профиля с учетом группы admin, для отображения кнопки на админ. панель

    Шаблон:
        accounts/me.html
    """

    template_name = "accounts/me.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user_is_admin"] = user.is_superuser
        return context
