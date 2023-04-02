from django.http import HttpResponse
from django.shortcuts import render  # NOQA : F401
from django.urls import reverse_lazy
from django.views.generic import CreateView
from webargs import fields, validate
from webargs.djangoparser import use_kwargs

from accounts.forms import UserRegistrationForm
from accounts.tasks import accounts_generator_task


@use_kwargs(
    {
        'count': fields.Int(required=True, validate=[validate.Range(min=1, max=100)]),
        'user_type': fields.Int(required=True, validate=[validate.Range(min=0, max=1)]),
    },
    location='query',
)
def generate_accounts_view(request, count, user_type):
    accounts_generator_task.delay(count=count, user_type=user_type)

    return HttpResponse("Task is started")


class UserRegistration(CreateView):
    template_name = "accounts/registration/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("index")
