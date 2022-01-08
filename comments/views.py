from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View
from rest_framework.generics import get_object_or_404


