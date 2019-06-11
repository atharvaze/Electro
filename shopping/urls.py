"""shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from product.views import HomeView, ProductDetailView, store,check,add_to_cart,remove_from_cart,OrderSummaryView,remove_single_from_cart,add_single_from_cart,checkout,finalorder,search
from django.conf import settings
from django.conf.urls.static import static
app_name = 'product'
urlpatterns = [
    path('search/',search, name='search'),
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(),name='home'),
    path('accounts/', include('allauth.urls')),
    path('order-summary/',OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ProductDetailView.as_view(), name='p-detail'),
    path('store/', store),
    path('checkout/',checkout, name="checkout"),
   
    path('final-order/', finalorder, name='final_order'),
    path('checkout/',check ,name='checkout'),
    path('add-to-cart/<slug>/',add_to_cart ,name='add_to_cart'),
    path('remove-single-item-from-cart/<slug>/',remove_single_from_cart ,name='remove_single_from_cart'),
    path('add-single-item-to-cart/<slug>/',add_single_from_cart ,name='add_single_from_cart'),
    path('remove-from-cart/<slug>/',remove_from_cart ,name='remove_from_cart')
]

if settings.DEBUG:
	urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 