from django.db import models
from django.db.models import Q
import csv
import io


class Deal(models.Model):
    customer = models.CharField(max_length=128)  # логин покупателя
    item = models.CharField(max_length=128)  # наименование товара
    total = models.PositiveIntegerField()  # сумма сделки
    quantity = models.PositiveIntegerField()  # количество товара, шт
    date = models.DateTimeField()  # дата и время регистрации сделки

    def PostUpdateDeals(self):  # загрузка csv-файла
        # чтение файла
        data_set = self.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        deal_bulk_list = list()
        for columm in csv.reader(io_string, delimiter=','):
            # добавление записей из файла в список
            deal_bulk_list.append((Deal(customer=columm[0],
                                        item=columm[1],
                                        total=columm[2],
                                        quantity=columm[3],
                                        date=columm[4])))
        # cохранение в БД списка новых записей
        Deal.objects.bulk_create(deal_bulk_list)

        return


class TopClients(models.Model):
    username = models.CharField(max_length=128)  # логин клиента
    spent_money = models.PositiveIntegerField()  # сумма потраченных средств за весь период
    gems = models.TextField(
        max_length=512)  # список названий камней, которые купили как минимум двое из списка топ клиентов

    def GetTopClientsList(self):  # получить список из 5 клиентов, потративших наибольшую сумму за весь период
        all_deal_list = Deal.objects.all().order_by('customer')  # получаем все объекты в БД, отсортированные по имени
        if all_deal_list.count() > 0:  # если БД не пустая
            self = list()
            while all_deal_list.count() > 0:
                deal = all_deal_list.first()  # берем верхнего клиента в списке
                # берем записи с текущим именем клиента
                temp_deal_list = all_deal_list.filter(customer=deal.customer)
                # исключаем использованное имя клиента
                all_deal_list = all_deal_list.exclude(customer=deal.customer)
                temp_sum = 0
                for asd in temp_deal_list:
                    temp_sum += asd.total  # вычисляем сумму потраченных денег клиентом
                # получили список всех клиентов и суммы потраченных денег каждым из них
                self.append(TopClients(None, deal.customer, temp_sum, ''))

            # пузырьковая сортировка
            for i in range(len(self) - 1):
                for j in range(len(self) - i - 1):
                    if self[j].spent_money < self[j + 1].spent_money:
                        self[j], self[j + 1] = self[j + 1], self[j]

            self = self[:5]  # оставляем 5 клиентов с наибольшей суммой потраченных денег
            temp_deal_list = Deal.objects.all().order_by('customer')
            # получаем список всех покупок топовых покупателей
            temp_deal_list = temp_deal_list.filter(Q(customer=self[0].username) |
                                                   Q(customer=self[1].username) |
                                                   Q(customer=self[2].username) |
                                                   Q(customer=self[3].username) |
                                                   Q(customer=self[4].username))

            while temp_deal_list.count() > 0:
                deal = temp_deal_list.first()
                # проверяем количество покупок камня в списке, в котором исключен логин клиента
                if temp_deal_list.exclude(customer=deal.customer).filter(item=deal.item).count() > 0:
                    self[0].gems += deal.item + ', '
                # исключаем проверенный камень
                temp_deal_list = temp_deal_list.exclude(item=deal.item)

            self[0].gems = self[0].gems[:len(self[0].gems) - 2] + \
                           self[0].gems[len(self[0].gems) - 2:].replace(',', '.')
            return self
        else:
            return None
