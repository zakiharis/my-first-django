from django import forms

from .models import Voucher, VoucherHistory


class VoucherForm(forms.Form):

    code = forms.CharField(label="code")

    def __init__(self, *args, **kwargs):
        self.redirect = False
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean(self):
        if not self.user.id:
            self.redirect = True
            raise forms.ValidationError("please login")

        cleaned_data = super().clean()
        code = cleaned_data.get("code")

        try:
            voucher = Voucher.objects.get(code=code)
        except Voucher.DoesNotExist:
            raise forms.ValidationError("Voucher does not exists")

        voucher_usage_count = 0

        try:
            voucher_usage_count = VoucherHistory.objects.filter(voucher_id=voucher.id,
                                                                used_by_id=self.user.id).count()
        except VoucherHistory.DoesNotExist:
            pass

        if voucher_usage_count >= 3:
            raise forms.ValidationError("Voucher usage exceeded. Please use different voucher!")

        return cleaned_data
