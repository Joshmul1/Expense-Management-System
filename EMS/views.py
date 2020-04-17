import base64
import json
import os
import re
from datetime import datetime, timedelta
import piexif
import pytesseract as pytesseract
from django.contrib.auth.decorators import login_required

import django_excel as excel
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render, redirect
from EMS.addTodo import TodoForm
from EMSAttempt import settings
from .addExpense import *
from EMS import addTodo
from PIL import Image
import cv2

# TODO CHANGE THIS PATH TO TESSERACT ON THAT DEVICE / SERVER. SHOULD I JUST INCLUDE IT IN THIS PROJECT?
# This sets the path of tesseract within the wrapper pytesseract.
# If launched on server this MUST be changed to the install path of
# tesseract on the server
# pytesseract.pytesseract.tesseract_cmd = (
#     r'C:\Program Files\Tesseract-OCR\tesseract'
# )


pytesseract.pytesseract.tesseract_cmd = (
    os.path.join(settings.BASE_DIR, 'Tesseract-OCR/tesseract')

)

excel_objects = []


# Create your views here.

@login_required()
def mainPageView(request):
    if request.user.is_authenticated:
        return redirect('main')


    else:

        return redirect('accounts/login')


@login_required
def mainUserPage(request):
    if request.user_agent.is_mobile:
        return render(request, 'mobile_page.html')
    query_results = Expense.objects.all().filter(has_been_changed=True)

    return render(request, 'mainUserPage.html', locals())


def ajaxTestPage(request):
    return render(request, 'ajaxTestPage.html')


def toDo(request):
    return render(request, 'todo.html')


def createNoInput(request):
    return render(request, 'createNoInput.html')


@login_required
def createExpense(request, object_id):
    object_id = object_id
    try:
        query_results = Expense.objects.get(pk=object_id)
    except Expense.DoesNotExist:
        return redirect('createNoInput')
    else:
        form = ExpenseForm
        all_categories = Category.objects.all()[1:]
        return render(request, 'createExpense.html', locals(), {'form': form})


@login_required
def viewExpense(request, object_id):
    object_id = object_id
    try:
        query_results = Expense.objects.get(pk=object_id)
    except Expense.DoesNotExist:
        return redirect('createNoInput')
    else:
        return render(request, 'viewExpense.html', locals())


def createSubmit(request, object_id):
    if request.method == 'POST':
        submit_value = request.POST['submit']
        if submit_value == 'Save':
            form = ExpenseForm(request.POST, request.FILES)
            query_results = Expense.objects.get(pk=object_id)
            query_results.name = form['name'].value()
            query_results.price = form['price'].value()
            query_results.date = form['date'].value()
            query_results.time = form['time'].value()

            if form['has_been_paid'].value():
                query_results.has_been_paid = True
            else:
                query_results.has_been_paid = False

            query_results.has_been_changed = True

            category_before_change = query_results.category_name
            category_name = form['category_name'].value()
            category = Category.objects.get_or_create(category_name=category_name)[0]
            query_results.category_name = category
            query_results.save()

            check_category_in_use(category_before_change)

            return redirect('view', object_id=object_id)

        elif submit_value == 'Delete':
            delete_object(object_id)
            return redirect('main')



@login_required
def createTodo(request):
    query_results = Todo.objects.all()
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES)
        if form.is_valid():
            # instance = form.save(commit=False) if you want to add stuff later to it.
            form.save()
            return render(request, 'todo.html', locals())
    else:
        form = addTodo.TodoForm
    return render(request, 'todo.html', locals(), {'form': form})


@login_required
def takeImage(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            image_data = request.POST['image']

            if len(image_data) == 0:
                return render(request, 'takeImage.html')
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            image = ContentFile(base64.b64decode(imgstr), "picture.png")
            file_name = "'myphoto." + ext
            instance = setDefaults(form)
            instance.image = image
            instance.save()
            object_id = instance.id
            perform_OCR(object_id)

            return redirect('create', object_id=object_id)

    else:
        form = ExpenseForm

    return render(request, 'takeImage.html', {'form': form})


@login_required
def uploadedImages(request):
    query_results = Expense.objects.all()
    query_results = query_results.filter(has_been_changed=False)
    return render(request, 'uploadedImages.html', locals())


@login_required
def uploadImageChoice(request):
    return render(request, 'uploadImageChoice.html')


@login_required
def uploadImageFile(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            instance = setDefaults(form)
            instance.save()
            object_id = instance.id

            perform_OCR(object_id)
            # return render(request, 'createExpense.html', locals())

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            fullpath = BASE_DIR + instance.image.url
            img = Image.open(fullpath)

            if "exif" in img.info:
                exif_dict = piexif.load(img.info["exif"])

                if piexif.ImageIFD.Orientation in exif_dict["0th"]:
                    orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
                    exif_bytes = piexif.dump(exif_dict)

                    if orientation == 2:
                        img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 3:
                        img = img.rotate(180)
                    elif orientation == 4:
                        img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 5:
                        img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 6:
                        img = img.rotate(-90, expand=True)
                    elif orientation == 7:
                        img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 8:
                        img = img.rotate(90, expand=True)
                    img.save(fullpath, exif=exif_bytes)

            return redirect('create', object_id=object_id)

        # return render(request, 'uploadImageFile.html', locals())
    else:
        form = ExpenseForm
    return render(request, 'uploadImageFile.html', {'form': form})


def excelExport(request):
    if request.method == 'POST':
        # object_ids = request.POST.get('object_ids', None)
        # question = Expense.objects.all()
        question = excel_objects
        query_sets = question
        # query_sets = question.filter(has_been_changed=True)
        column_names = ['name', 'date', 'time', 'price', 'category_name_id']
        return excel.make_response_from_query_sets(
            query_sets,
            column_names,
            'xls',
            file_name="custom"
        )
    else:
        return render(request, 'excelExportTest.html')


@login_required
def statistics(request):
    all_categories = Category.objects.all()[1:]
    return render(request, 'statistics.html', locals())


def rotate_image(request):
    if request.is_ajax() and request.method == 'POST':
        id = int(request.POST.get('id', None))
        direction = request.POST.get('direction', None)
        object = Expense.objects.get(id=id)
        # path = 'media' + object.image.url
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fullpath = BASE_DIR + object.image.url
        image = Image.open(fullpath)
        image = image.rotate(90, expand=True)
        image.save(fullpath, overwrite=True)
        data = {

        }
        return JsonResponse(data)
    else:
        return render(request, "mainUserPage.html")


def delete_object(object_id):
    obj = Expense.objects.all().filter(id=object_id)
    obj = obj[0]
    if obj is not None:
        obj.delete()
        category = obj.category_name
        check_category_in_use(category)
        return True

    return False


def check_category_in_use(category):
    if category.category_name == 'None':
        return False
    remaining_expenses = Expense.objects.all().filter(category_name=category)
    if len(remaining_expenses) == 0:
        category.delete()
        return True


def get_receipt_details(extracted_split):
    date = find_date(extracted_split)
    price = find_price(extracted_split)
    time = find_time(extracted_split)

    return date, time, price


def setDefaults(form):
    default_category = Category.objects.get_or_create(category_name='None')[0]
    instance = form.save(commit=False)
    instance.date = datetime.now()
    instance.time = '00:00'
    instance.price = 0
    instance.category_name = default_category
    return instance


def perform_OCR(obj_id):
    # Get Object
    obj = Expense.objects.get(id=obj_id)

    # Error check here

    # Get image
    image = cv2.imread(obj.image.path, cv2.IMREAD_GRAYSCALE)
    retval, thresh1 = cv2.threshold(image, 125, 255, cv2.THRESH_BINARY)
    extracted_text_normal = pytesseract.image_to_string(image, lang='eng')
    extracted_split_normal = extracted_text_normal.splitlines()

    extracted_text_thresh = pytesseract.image_to_string(thresh1, lang='eng')
    extracted_split_thresh = extracted_text_thresh.splitlines()

    date, time, price = get_receipt_details(extracted_split_normal)

    if date is None:
        date = find_date(extracted_split_thresh)
    if time is None:
        time = find_time(extracted_split_thresh)
    if price is None:
        price = find_price(extracted_split_thresh)

    if date is not None:
        obj.date = date
    if time is not None:
        obj.time = time
    if price is not None:
        obj.price = price
    obj.save()


def find_time(text):
    regex = [r"\d{1,2}:\d{2}"]
    time_no_keyword = []

    for x in text:
        x = x.lower()
        for exp in regex:
            match = re.search(exp, x)
            if match is not None:
                if "time" in x:
                    return match.group(0)
                else:
                    time_no_keyword.append(match.group(0))
    if len(time_no_keyword) >= 1:
        return time_no_keyword[0]
    else:
        return None


def find_price(text):
    regex = [r"([£]\d{1,10}\.\d{1,2})", r"(\d{1,10}\.\d{1,2})"]
    prices_keyword = []
    prices_no_keyword = []

    # for x in text:
    #     x = x.lower()
    #     if "total" in x or "amount":
    #         for exp in regex:
    #             match = re.search(exp, x)
    #             if match is not None:
    #                 result = match.group(0)
    #                 if '£' in result:
    #                     return result[1:]
    #                 else:
    #                     return result

    for x in text:
        x = x.lower()
        keyword = False
        for exp in regex:
            match = re.search(exp, x)
            if match is not None:
                if "total" in x or "amount" in x:
                    keyword = True
                result = match.group(0)
                if '£' in result:
                    result = result[1:]
                if keyword:
                    prices_keyword.append(result)
                else:
                    prices_no_keyword.append(result)
    if len(prices_keyword) >= 1:
        return max(prices_keyword)
    elif len(prices_no_keyword) >= 1:
        return max(prices_no_keyword)
    else:
        return None

    #
    #     if "total" in x or "amount" in x:
    #         for exp in regex:
    #             match = re.search(exp, x)
    #             if match is not None:
    #                 result = match.group(0)
    #                 if '£' in result:
    #                     prices_keyword.append(result[1:])
    #                 else:
    #                     prices_keyword.append(result)
    # if len(prices) >= 1:
    #     return max(prices)
    # else:
    #     for x in text:
    #         for exp in regex:
    #             match = re.search(exp, x)
    #             if match is not None:
    #                 result = match.group(0)
    #                 if '£' in result:
    #                     prices.append(result[1:])
    #                 else:
    #                     prices.append(result)
    # if len(prices) >= 1:
    #     return max(prices)
    # else:
    #     return None


def find_date(text):
    regexps = [r"(\d{4}/\d{2}/\d{2})", r"(\d{4}-\d{2}-\d{2})", r"(\d{2}/\d{2}/\d{4})", r"(\d{2}-\d{2}-\d{4})",
               r"(\d{2}/\d{2}/\d{2})", r"(\d{2}-\d{2}-\d{2})", r'(\d+[.]\d+[.]\d+)']
    for x in text:
        for exp in regexps:
            match = re.search(exp, x)
            if match is not None:
                return format_date(match.group(0))
    return None


def check_valid_date(date):
    # 01-34-6789
    now = datetime.now()
    current_year = datetime.now().year
    year_given = int(date[6:])
    month_given = int(date[3:5])
    day_given = int(date[:2])
    if year_given > current_year or year_given < 2000:
        # date = date[0:6] + str(current_year)
        date = date[0:6] + str(now.year)
    if month_given > 12:
        date = date[:3] + str(now.month) + date[5:]
    if day_given > 31:
        date = str(now.day) + date[2:]
    return date


def format_date(date):
    pattern_1 = re.compile(r"(\d{4}/\d{2}/\d{2})")
    pattern_2 = re.compile(r"(\d{4}-\d{2}-\d{2})")
    # If matches YYYY-MM-DD or YYYY/MM/DD
    if pattern_1.match(date) or pattern_2.match(date):
        # Convert to full year ( with dashes) and reverse
        # date = date[8:] + date[4:8] + date[0:4]
        if '-' not in date:
            date = date[:4] + '-' + date[5:7] + '-' + date[8:]
        return date
    # Find out what format the date is

    # Presume DD-MM-YYYY format for receipts
    pattern_1 = re.compile(r"(\d{2}/\d{2}/\d{4})")
    pattern_2 = re.compile(r"(\d{2}-\d{2}-\d{4})")

    # If matches DD-MM-YYYY or DD/MM/YYYY
    if pattern_1.match(date) or pattern_2.match(date):
        # Convert to dashes and reverse
        date = date[0:2] + '-' + date[3:5] + '-' + date[6:]
        date = check_valid_date(date)
        date = date[6:] + date[2:6] + date[0:2]
        return date

    pattern_1 = re.compile(r"(\d{2}/\d{2}/\d{2})")
    pattern_2 = re.compile(r"(\d{2}-\d{2}-\d{2})")

    # If matches DD-MM-YY or DD/MM/YY
    if pattern_1.match(date) or pattern_2.match(date):
        # Convert to full year ( with dashes) and reverse
        date = date[0:2] + '-' + date[3:5] + '-' + "20" + date[6:]
        date = check_valid_date(date)
        date = date[6:] + date[2:6] + date[0:2]
        return date


def getObjectsFromDaysAgo(days):
    if days == 0:
        objects = Expense.objects.all().filter(has_been_changed=True)
    else:
        date_delta = datetime.today() - timedelta(days=days)
        objects = Expense.objects.all().filter(date__gte=date_delta).filter(has_been_changed=True)
    return objects


def getPieChart(objects):
    labels = []
    data = []
    for x in objects:
        # labels.append(x.name)
        labels.append("ID : " + str(x.id) + "-" + x.name)
        data.append(x.price)
    chart = {
        'labels': labels,
        'data': data
    }
    return chart


def totalSpending(objects):
    # date_delta = datetime.today() - timedelta(days=days)
    #
    # objects = Expense.objects.all().filter(date__gte=date_delta).filter(has_been_changed=True)
    total = 0
    for x in objects:
        total += x.price
    return total


def store_values(request):
    global excel_objects
    data = {}
    if request.is_ajax() and request.method == 'POST':
        object_ids = request.POST.get('object_ids')
        object_ids = json.loads(object_ids)
        objects = []
        for id in object_ids:
            try:
                obj = Expense.objects.get(id=id)
                objects.append(obj)
            except ObjectDoesNotExist:
                pass
        excel_objects = objects
        return JsonResponse(data)

    else:
        return JsonResponse(data)


def ajax_pdf(request):
    data = {}
    if request.is_ajax() and request.method == 'POST':
        if request.POST.get('object_ids', None):
            object_ids = request.POST.get('object_ids', None)
            objects = []
            for id in object_ids:
                try:
                    obj = Expense.objects.get(id=id)
                    objects.append(obj)
                except ObjectDoesNotExist:
                    pass

            data = {'objects': objects}

    return JsonResponse(data)


def ajax_stats(request):
    if request.is_ajax() and request.method == 'POST':
        query_results = "Test data worked"
        # time_choice = request.POST.get('time_choice', None)
        time_choice = request.POST.get('time_choice', None)
        category_choice = request.POST.get('category_choice', None)
        if time_choice == 'all':
            days = 0
        elif time_choice == "week":
            days = 7
        elif time_choice == "month":
            days = 31
        elif time_choice == "year":
            days = 365
        else:
            days = 365

        objects = getObjectsFromDaysAgo(days)
        if category_choice != 'None':
            category_obj = Category.objects.get(category_name=category_choice)
            objects = objects.filter(category_name=category_obj)
        total_spend = totalSpending(objects)

        chart = getPieChart(objects)

        data = {
            "total_spend": total_spend,
            "labels": chart['labels'],
            "data": chart['data']
        }
        return JsonResponse(data)
    else:
        return render(request, "mainUserPage.html")
