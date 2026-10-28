from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from apps.orders.models import Order

from .forms import LoginForm, ProfileForm, RegisterForm, UserInfoForm
from .models import Profile


class StoreLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class StoreLogoutView(LogoutView):
    pass


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Te damos la bienvenida, {user.first_name}. Tu cuenta está lista.")
        next_url = request.GET.get("next", "")
        if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        return redirect("accounts:profile")
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    user_form = UserInfoForm(request.POST or None, instance=request.user, prefix="u")
    profile_form = ProfileForm(request.POST or None, instance=profile_obj, prefix="p")
    if request.method == "POST":
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Guardamos tus datos.")
            return redirect("accounts:profile")
        messages.error(request, "Revisa los campos marcados para guardar los cambios.")
    orders = request.user.orders.prefetch_related("items")
    stats = orders.exclude(status=Order.Status.CANCELADO).aggregate(spent=Sum("total"))
    return render(
        request,
        "accounts/profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "orders": orders,
            "open_orders": orders.exclude(status__in=[Order.Status.ENTREGADO, Order.Status.CANCELADO]).count(),
            "spent": stats["spent"] or 0,
            "editing": request.method == "POST" or request.GET.get("editar") == "1",
        },
    )


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related("items__product"), pk=pk, user=request.user)
    return render(request, "accounts/order_detail.html", {"order": order})
