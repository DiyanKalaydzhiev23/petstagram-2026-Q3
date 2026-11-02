from django.contrib.auth.mixins import UserPassesTestMixin


class DisabledFormMixin:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['disabled'] = True
            field.widget.attrs['readonly'] = True


class CheckIsOwnerMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user == self.get_object().user
