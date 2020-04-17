from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from EMS.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainPageView, name='home'),
    path('main/', mainUserPage, name='main'),
    path('todo/', createTodo, name='todo'),
    path('create/', createNoInput, name='createNoInput'),
    path('view/', createNoInput, name='createNoInput'),
    path('takeImage/', takeImage, name='takeImage'),
    path('create/<int:object_id>', createExpense, name='create'),
    path('view/<int:object_id>', viewExpense, name='view'),
    path('images', uploadedImages, name='images'),
    path('createSubmit/<int:object_id>', createSubmit, name='createSubmit'),
    # path('uploadImage/', uploadImageChoice, name='uploadImageChoice'),
    path('uploadImageFile', uploadImageFile, name='uploadImageFile'),
    path('ajaxStats', ajax_stats, name='ajaxStats'),
    path('ajax_pdf', ajax_pdf, name='ajax_pdf'),
    path('rotate_image', rotate_image, name='rotate_image'),
    path('excelTest', excelExport, name='excelExport'),
    path('stats', statistics, name='statistics'),
    path('delete_object', delete_object, name = 'delete_object'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('store_values', store_values, name='store_values'),



              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()


