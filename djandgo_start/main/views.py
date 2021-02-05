from django.shortcuts import render
from .models import Purchase, Customer
from django_pandas.io import read_frame
from matplotlib import pyplot as plt
from io import StringIO
import pandas as pd


def create_line():
    qs_purchases = Purchase.objects.order_by('pay_date')
    df_purchases = read_frame(qs_purchases, fieldnames=['amount', 'pay_date', 'payer_id__id'])
    plt.switch_backend('Agg')
    df_purchases.plot(
        x='pay_date',
        y='amount',
        xlabel='Дата',
        ylabel='Сумма',
        label='Сумма',
        title='График зависимости суммы покупот от даты.'
    )
    imgdata = StringIO()
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)
    return imgdata.getvalue()


def create_bar():
    qs_purchases = Purchase.objects.order_by('pay_date')
    qs_customer = Customer.objects.all()
    df_purchases = read_frame(qs_purchases, fieldnames=['amount', 'pay_date', 'payer_id__id'])
    df_customer = read_frame(qs_customer, fieldnames=['id', 'first_name', 'last_name'])
    new_df = pd.merge(df_purchases, df_customer, how='inner', left_on='payer_id__id', right_on='id')
    new_df['full_name'] = new_df[['first_name', 'last_name']].apply(lambda x: ' '.join(x), axis=1)
    plt.switch_backend('Agg')
    new_df.plot.bar(
        x='full_name',
        y='amount',
        label='Сумма',
        title='Гистограмма',
        xlabel='Покупатель',
        ylabel='Сумма платежа',
        rot=0
    )
    imgdata = StringIO()
    plt.savefig(imgdata, format='svg')
    imgdata.seek(0)
    return imgdata.getvalue()


def index(request):
    data = create_line()
    plot = 'bar'
    if request.method == 'POST':
        if request.POST.get('plot', '') == 'bar':
            data = create_bar()
            plot = 'line'
        else:
            data = create_line()
            plot = 'bar'

    context = {
        'data': data,
        'plot': plot,
    }
    return render(request, 'main/index.html', context)

