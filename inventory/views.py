from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView,UpdateView, DeleteView
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterationForm, ItemForm
from .models import Item, Category
from inventoryManagement.settings import LOW_QUANTITY
from django.contrib import messages
class Index(TemplateView):
    template_name = 'inventory/index.html'

class SignUpView(View):
    def get(self,request):
        form = UserRegisterationForm()
        return render(request, 'inventory/signup.html', {'form':form})
    def post(self, request):
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'], 
                                password=form.cleaned_data['password1'])
            login(request,user)
            return redirect('index')
        return render(request, 'inventory/signup.html', {'form':form})
    
class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        low_inventory = Item.objects.filter(user=self.request.user.id,quantity__lte=LOW_QUANTITY)

        if low_inventory.count() > 0:
            if low_inventory.count() > 1:
                messages.error(request, f'{low_inventory.count()} items have low inventory')
            else:
                messages.error(request, '1 item has low inventory')

        low_inventory_ids = Item.objects.filter(user=self.request.user.id,quantity__lte=LOW_QUANTITY).values_list('id', flat=True)

        items = Item.objects.filter(user=self.request.user.id).order_by('id')
        return render(request, 'inventory/dashboard.html',{'items':items, 'low_inventory_ids': low_inventory_ids})
    
class AddItem(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class EditItem(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

class DeleteItem(LoginRequiredMixin, DeleteView):
    model= Item
    template_name = 'inventory/delete_item.html'
    success_url = reverse_lazy('dashboard')
    context_object_name= 'item'
