from django.contrib import messages
from django.shortcuts import render
from deal.models import *


def deals(request):
    if request.method == 'POST':
        # получаем csv-файл из POST запроса
        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Ошибка! Это не csv-файл.')
        else:
            Deal.PostUpdateDeals(csv_file)
            messages.success(request, 'Успешная загрузка.')
        return render(request, 'deal/errors_notification.html', locals())


    elif request.method == 'GET':
        # выдаем список топ клиентов
        top_clients = TopClients
        top_clients = TopClients.GetTopClientsList(top_clients)
        return render(request, 'deal/deals.html', {'top_clients': top_clients})


    else:
        messages.error(request, 'Ошибка! Неизвестный тип запроса.')
        return render(request, 'deal/errors_notification.html', locals())
