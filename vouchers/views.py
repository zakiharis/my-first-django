import decimal
import json

from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from .forms import VoucherForm
from .models import Voucher, VoucherHistory
from .users.models import User


@require_http_methods(["POST"])
def submit_order(request):
    user_id = request.session.get("_auth_user_id", None)
    voucher = request.session.get("voucher", None)

    if user_id and voucher:
        voucher_dict = json.loads(voucher)
        voucher_id = voucher_dict.get("id")

        voucher = Voucher.objects.get(pk=voucher_id)
        user = User.objects.get(pk=user_id)

        voucher_history = VoucherHistory(voucher=voucher, used_by=user)
        voucher_history.save()

        # remove session
        request.session["voucher"] = None
        request.session["discount_value"] = None
        request.session["total_price"] = OrderView.subtotal

        messages.success(request, "Order received!")
    return redirect("/")


class OrderView(FormView):
    template_name = "pages/home.html"
    form_class = VoucherForm
    success_url = reverse_lazy("home")

    # hard code value since main assignment is for voucher functionality
    subtotal = 190.00

    def form_valid(self, form):
        code = form.cleaned_data["code"]
        voucher = Voucher.objects.get(code=code)
        voucher_dict = voucher.__dict__
        voucher_dict.pop("_state", None)
        discount_value = self.calculate_discount(voucher)

        self.request.session["voucher"] = json.dumps(voucher_dict, cls=DjangoJSONEncoder)
        self.request.session["discount_value"] = discount_value
        self.request.session["total_price"] = self.calculate_total(discount_value)

        return super().form_valid(form)

    def form_invalid(self, form):
        self.request.session["voucher"] = None
        self.request.session["discount_value"] = None
        self.request.session["total_price"] = self.subtotal

        if form.redirect:
            return redirect("account_login")

        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voucher = self.request.session.get("voucher", None)
        discount_value = self.request.session.get("discount_value", None)
        total_price = self.request.session.get("total_price", None)

        if voucher:
            context["voucher"] = json.loads(voucher)
            context["discount_value"] = discount_value

        if total_price:
            context["total_price"] = total_price
        else:
            context["total_price"] = self.subtotal

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def calculate_discount(self, voucher):
        if voucher.voucher_type == "a":
            return float(voucher.value)

        elif voucher.voucher_type == "b":
            return float(decimal.Decimal(self.subtotal) * (voucher.value / decimal.Decimal("100")))

        else:
            return 0

    def calculate_total(self, discount_value):
        return float(decimal.Decimal(self.subtotal) - decimal.Decimal(discount_value))
