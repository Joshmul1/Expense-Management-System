import datetime
import EMS.views
from EMS.views import getObjectsFromDaysAgo
import EMS.views
from django.test import TestCase
from EMS.models import Expense, Category
from EMS import addExpense


# Create your tests here.
def get_today():
    return datetime.datetime.now()


class DateFinder(TestCase):

    def test_objects_from_days_ago(self):
        today = get_today()
        within_week = today - datetime.timedelta(days=2)
        more_than_week_ago = today - datetime.timedelta(days=14)
        self.assertEqual(1, 1)
        self.assertEqual(len(getObjectsFromDaysAgo(0)), 0)

        category_obj = Category("None")
        category_obj.save()
        Expense.objects.create(name="within week", date=today, time="00:00", price=0, has_been_changed=True,
                               category_name=category_obj)
        self.assertEqual(len(getObjectsFromDaysAgo(7)), 1)

        Expense.objects.create(name="within week", date=within_week, time="00:00", price=0, has_been_changed=True,
                               category_name=category_obj)

        self.assertEqual(len(getObjectsFromDaysAgo(7)), 2)

        Expense.objects.create(name="within week", date=more_than_week_ago, time="00:00", price=0,
                               has_been_changed=True,
                               category_name=category_obj)

        self.assertEqual(len(getObjectsFromDaysAgo(7)), 2)
        self.assertEqual(len(getObjectsFromDaysAgo(14)), 3)


class TextExtraction(TestCase):

    def test_find_price(self):
        text = ['£12.50', 'random', 'words', '14.75', 'Total £100.0']
        price = EMS.views.find_price(text)
        self.assertEqual(price, '100.0')

        text = ['Total £150', '120909', 'amount is probably 576.90']
        price = EMS.views.find_price(text)
        self.assertEqual(price, '576.90')

        text = ['there', 'is' 'no', 'price']
        price = EMS.views.find_price(text)
        self.assertEqual(price, None)

    def test_find_time(self):
        text = ['time', 'random', 'words', '12:30', 'time is 7']
        time = EMS.views.find_time(text)
        self.assertEqual(time, '12:30')

        text = ['12:', ':20', 'word', '11:27', 'time is 7']
        time = EMS.views.find_time(text)
        self.assertEqual(time, '11:27')

        text = ['time', 'random', 'words', '', 'time is 7']
        time = EMS.views.find_time(text)
        self.assertEqual(time, None)

    def test_find_date(self):
        text = ['date', 'random', 'words', '17/11/19', '']
        date = EMS.views.find_date(text)
        self.assertEqual(date, '2019-11-17')

        text = ['date', 'random', 'words', '17-11-19', '']
        date = EMS.views.find_date(text)
        self.assertEqual(date, '2019-11-17')

        text = ['date', 'random', 'words', '17/11/2020', '']
        date = EMS.views.find_date(text)
        self.assertEqual(date, '2020-11-17')

        text = ['date', 'random', 'words', '2020/11/17', '']
        date = EMS.views.find_date(text)
        self.assertEqual(date, '2020-11-17')

        text = ['date', 'random', 'words', '2020-11-17', '']
        date = EMS.views.find_date(text)
        self.assertEqual(date, '2020-11-17')

        text = ['date', 'random', 'words', '17 11 ', '']
        date = EMS.views.find_date(text)
        self.assertEqual(date, None)

    def test_format_date(self):
        date = '17-11-2020'
        date = EMS.views.format_date(date)
        self.assertEqual(date, '2020-11-17')

        date = '2020-11-17'
        date = EMS.views.format_date(date)
        self.assertEqual(date, '2020-11-17')

        date = '2020/11/17'
        date = EMS.views.format_date(date)
        self.assertEqual(date, '2020-11-17')

        date = '17-11-20'
        date = EMS.views.format_date(date)
        self.assertEqual(date, '2020-11-17')

    def test_check_valid_date(self):
        today = get_today()
        year = today.year
        month = today.month
        day = today.day

        date = '17-11-2025'
        date_expected = date[0:6] + str(year)
        date = EMS.views.check_valid_date(date)
        self.assertEqual(date, date_expected)

        date = '17-33-2020'
        date_expected = date[:3] + str(month) + date[5:]
        date = EMS.views.check_valid_date(date)
        self.assertEqual(date, date_expected)

        date = '55-11-2020'
        date_expected = str(day) + date[2:]
        date = EMS.views.check_valid_date(date)
        self.assertEqual(date, date_expected)


class TotalSpending(TestCase):
    def test_total_spending(self):
        category_obj = Category("None")
        category_obj.save()
        total_spending = 0
        Expense.objects.create(name="name", date='2020-01-01', time="00:00", price=100, has_been_changed=True,
                               category_name=category_obj)
        total_spending += 100

        self.assertEqual(EMS.views.totalSpending(Expense.objects.all()), total_spending)

        Expense.objects.create(name="name", date='2020-01-01', time="00:00", price=100, has_been_changed=True,
                               category_name=category_obj)
        total_spending += 100
        self.assertEqual(EMS.views.totalSpending(Expense.objects.all()), total_spending)

        Expense.objects.create(name="name", date='2020-01-01', time="00:00", price=500, has_been_changed=True,
                               category_name=category_obj)
        total_spending += 500
        self.assertEqual(EMS.views.totalSpending(Expense.objects.all()), total_spending)

        Expense.objects.create(name="name", date='2020-01-01', time="00:00", price=0, has_been_changed=True,
                               category_name=category_obj)

        total_spending += 0
        self.assertEqual(EMS.views.totalSpending(Expense.objects.all()), total_spending)
