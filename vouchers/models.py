from django.db import models

from .users.models import User


class Voucher(models.Model):

    code = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    desc = models.CharField(max_length=100, default="")
    voucher_type = models.CharField(max_length=1, choices=[('a', 'absolute'), ('b', 'percentage')], default='a')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class VoucherHistory(models.Model):

    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    used_by = models.ForeignKey(User, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Voucher id: {}".format(str(self.voucher.id))
