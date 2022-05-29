from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from mainapp.models import Accommodation
from mainapp.models import ListOfCountries
from authapp.models import TravelUser
from authapp.forms import TravelUserRegisterForm
from adminapp.forms import TravelUserAdminEditForm
from adminapp.forms import AccommodationEditForm


# from adminapp.forms import ListOfCountriesEditForm


# админка - список пользователей
class TravelUsersListView(ListView):
    model = TravelUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# админка - создание пользователя
@user_passes_test(lambda u: u.is_superuser)
def travel_user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = TravelUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = TravelUserRegisterForm()

    content = {
        'title': title,
        'update_form': user_form,
    }

    return render(request, 'adminapp/user_update.html', content)


# админка - редактирование пользователя
@user_passes_test(lambda u: u.is_superuser)
def travel_user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(TravelUser, pk=pk)

    if request.method == 'POST':
        edit_form = TravelUserAdminEditForm(request.POST,
                                            request.FILES, instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_update',
                                                args=[edit_user.pk]))
    else:
        edit_form = TravelUserAdminEditForm(instance=edit_user)

    content = {
        'title': title,
        'update_form': edit_form,
    }

    return render(request, 'adminapp/user_update.html', content)


# админка - удаление пользователя
@user_passes_test(lambda u: u.is_superuser)
def travel_user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(TravelUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {
        'title': title,
        'user_to_delete': user,
    }

    return render(request, 'adminapp/user_delete.html', content)


# админка - список стран
@user_passes_test(lambda u: u.is_superuser)
def countries(request):
    title = 'админка/страны'

    countries_list = ListOfCountries.objects.all()

    content = {
        'title': title,
        'objects': countries_list
    }

    return render(request, 'adminapp/countries.html', content)


# админка - создание страны
class CountryCreateView(CreateView):
    model = ListOfCountries
    template_name = 'adminapp/country_update.html'
    success_url = reverse_lazy('admin:countries')
    fields = '__all__'


# админка - редактирование страны
class CountryUpdateView(UpdateView):
    model = ListOfCountries
    template_name = 'adminapp/country_update.html'
    success_url = reverse_lazy('admin:countries')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'страны/редактирование'

        return context


# админка - удаление страны
class CountryDeleteView(DeleteView):
    model = ListOfCountries
    template_name = 'adminapp/country_delete.html'
    success_url = reverse_lazy('admin:countries')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


# админка - список предложений компании
@user_passes_test(lambda u: u.is_superuser)
def accommodations(request, pk):
    title = 'админка/размещение'

    country = get_object_or_404(ListOfCountries, pk=pk)
    accommodation_list = Accommodation.objects.filter(
        country__id=pk).order_by('name')

    content = {
        'title': title,
        'country': country,
        'objects': accommodation_list,
    }

    return render(request, 'adminapp/accommodations.html', content)


# админка - создание нового предложения
@user_passes_test(lambda u: u.is_superuser)
def accommodation_create(request, pk):
    title = 'размещение/создание'
    country = get_object_or_404(ListOfCountries, pk=pk)

    if request.method == 'POST':
        pass
        accommodation_form = AccommodationEditForm(request.POST, request.FILES)
        if accommodation_form.is_valid():
            accommodation_form.save()
            return HttpResponseRedirect(reverse('admin:accommodations',
                                                args=[pk]))

    else:

        accommodation_form = AccommodationEditForm(
            initial={'country': country})
    content = {
        'title': title,
        'update_form': accommodation_form,
        'country': country,
    }
    return render(request, 'adminapp/accommodation_update.html', content)


# админка - редактирование предложения
@user_passes_test(lambda u: u.is_superuser)
def accommodation_update(request, pk):
    title = 'размещение/редактирование'
    edit_accommodation = get_object_or_404(Accommodation, pk=pk)

    if request.method == 'POST':
        accommodation_edit_form = AccommodationEditForm(
            request.POST, request.FILES, instance=edit_accommodation)
        if accommodation_edit_form.is_valid():
            accommodation_edit_form.save()
            return HttpResponseRedirect(
                reverse('admin:accommodation_update',
                        args=[edit_accommodation.pk]))
    else:
        accommodation_edit_form = AccommodationEditForm(
            instance=edit_accommodation)
    content = {
        'title': title,
        'update_form': accommodation_edit_form,
        'country': edit_accommodation.country,
    }
    return render(request, 'adminapp/accommodation_update.html', content)


# админка - карточка предложения компании
class AccommodationDetailView(DetailView):
    model = Accommodation
    template_name = 'adminapp/accommodation_read.html'


# админка - удаление предложения
@user_passes_test(lambda u: u.is_superuser)
def accommodation_delete(request, pk):
    title = 'размещение/удаление'
    accommodation = get_object_or_404(Accommodation, pk=pk)

    if request.method == 'POST':
        accommodation.is_active = False
        accommodation.save()
        return HttpResponseRedirect(reverse('admin:accommodations',
                                            args=[accommodation.country.pk]))
    content = {
        'title': title,
        'accommodation_to_delete': accommodation,
    }
    return render(request, 'adminapp/accommodation_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def travel_user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(TravelUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {
        'title': title,
        'user_to_delete': user,
    }

    return render(request, 'adminapp/user_delete.html', content)
