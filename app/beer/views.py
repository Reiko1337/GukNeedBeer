from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Beer
from .forms import BeerForm, SortBeerForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.views.generic import UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator


def beer(request):
    beers = Beer.objects.all()
    search_query = request.GET.get('filter', '')
    page_number = request.GET.get('page', 1)
    form = SortBeerForm(request.GET)
    if search_query:
        try:
            user_id = User.objects.get(username__icontains=search_query).id
        except:
            user_id = None
        beers = beers.filter(
            Q(name__icontains=search_query) | Q(user=user_id))
        paginator = Paginator(beers, 10)
        page_beers = paginator.get_page(page_number)
    else:
        beers = beers.all()
        paginator = Paginator(beers, 10)
        page_beers = paginator.get_page(page_number)

    if form.is_valid():
        if form.cleaned_data['ordering']:
            beers = beers.order_by(form.cleaned_data['ordering'])
            paginator = Paginator(beers, 10)
            page_beers = paginator.get_page(page_number)


    data = {
        'beers': page_beers,
        'form': form,
    }
    return render(request, 'beer/beer.html', data)


@login_required
def beer_add(request):
    if request.method == 'POST':
        form = BeerForm(request.POST, request.FILES)
        if form.is_valid():
            beer = form.save(commit=False)
            beer.user = request.user
            beer.save()
            messages.success(request, 'Пиво добавлено')
            return redirect('list_beer')
    else:
        form = BeerForm()
    return render(request, 'beer/beer_add.html', {'form': form})


@login_required
def list_beer(request):
    beers = Beer.objects.filter(user=request.user.id)
    search_query = request.GET.get('filter', '')
    page_number = request.GET.get('page', 1)
    form = SortBeerForm(request.GET)
    if search_query:
        beers = beers.filter(name__icontains=search_query)
        paginator = Paginator(beers, 10)
        page_beers = paginator.get_page(page_number)
    else:
        beers = beers.all()
        paginator = Paginator(beers, 10)
        page_beers = paginator.get_page(page_number)

    if form.is_valid():
        if form.cleaned_data['ordering']:
            beers = beers.order_by(form.cleaned_data['ordering'])
            paginator = Paginator(beers, 10)
            page_beers = paginator.get_page(page_number)

    data = {
        'beers': page_beers,
        'form': form,
    }
    return render(request, 'beer/beer_list.html', data)


class DeleteBeer(DeleteView):
    model = Beer
    success_url = reverse_lazy('list_beer')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            success_url = self.get_success_url()
            try:
                self.object.delete()
                messages.success(self.request, 'Удаление прошло успешно')
            except:
                messages.error(self.request, 'Ошибка удаления')
            finally:
                return HttpResponseRedirect(success_url)
        else:
            messages.error(self.request, 'Отказано в доступе')
            return redirect('beer')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class UpdateBeer(UpdateView):
    model = Beer
    context_object_name = 'beer'
    template_name = 'beer/beer_edit.html'
    form_class = BeerForm
    success_url = reverse_lazy('list_beer')

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Обновления данных прошли успешно')
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == self.request.user:
            return super().get(request, *args, **kwargs)
        messages.error(self.request, 'Отказано в доступе')
        return redirect('beer')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)
