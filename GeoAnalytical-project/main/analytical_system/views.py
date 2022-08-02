from django.shortcuts import redirect, render
from .models import testtable
from .forms import testtableForm
import analysis
import json

def index(request):
    return render(request, 'analytical_system/index.html')

def analysis_module(request):
    if 'Standardized_Report' in request.POST:
        # Выбранный пользователем отчет
        SelectedReport = request.POST['SelectedReport']
        print(SelectedReport)

        if SelectedReport == 'Report_1':
            postgreSQLConnection = analysis.connectPostgreSQL()
            DataFrame = analysis.report_1(postgreSQLConnection)
            analysis.disconnectPostgreSQL(postgreSQLConnection)
        elif SelectedReport == 'Report_2':
            pass
        elif SelectedReport == 'Report_3':
            pass
        # DataFrame = analysis.populationData(SelectedReport)
        # columns = []
        # columns = DataFrame.columns.to_list()
        # DataFrame2 = DataFrame.to_json(orient='records')
        # arr = []
        # arr = json.loads(DataFrame2)
        # print(arr,"\n", columns)
        # content2 = {
        #     'Columns': columns,
        #     'DataFrame2': arr,
        #     'DataFrame': DataFrame.to_html()
        # }
        return render(request, 'analytical_system/analysis_module.html')
    elif 'Customer_Report' in request.POST:
        # Массив выбранных регионов
        Regions = []
        for i in range(85):
            Regions.append(request.POST.get(f'reg{i}', None))
        # удаляем None значения
        Regions = [int(x) for x in Regions if x]
        
        SelectedTableName = request.POST['TableName']
        
        
        SelectedYear = request.POST.getlist('Years')
        # SelectedYear = "\'" + "\', \'".join(SelectedYear)
        SelectedYear = [int(i) for i in SelectedYear]
        SelectedYear.append(1)
        print(f"{Regions=}")
        print(f"{SelectedTableName=}")
        print(f"{SelectedYear=}")
        # Подключение к БД Postgres
        postgreSQLConnection = analysis.connectPostgreSQL()
        # Запуск метода анализа
        DataFrame = analysis.read_data(Regions, SelectedTableName,SelectedYear, postgreSQLConnection)
        DataFrame2 = DataFrame.copy()
        # DataFrame2 = DataFrame2.T
        chart = analysis.get_plot_bar(DataFrame2)
        chart2 = analysis.get_plot_pie(DataFrame2)
        # chart2 = analysis.GeoAnalyticsMethod(DataFrame2)
        # columns = []
        # columns = DataFrame.columns.to_list()
        # analysis.drow_data(DataFrame)
        analysis.disconnectPostgreSQL(postgreSQLConnection)
        content2 = {
            # 'Columns': columns,
            'DataFrame2': DataFrame,
            'DataFrame': DataFrame.to_html(),
            'chart': chart,
            'chart2': chart2
        }
        return render(request, 'analytical_system/analysis_module.html', content2)
    else:
        return render(request, 'analytical_system/analysis_module.html')


# def test_html(request):
#     error = ''
#     if request.method == 'POST':
#         # создаем объект класса "testtableForm" с параметром (что мы получили от пользователя в POST)
#         form = testtableForm(request.POST)
#         if form.is_valid():
#             # сохраняем полученные данные в новую строку таблицы БД
#             form.save()
#             # переадресация на главную страницу
#             # return redirect('home')
#         else:
#             error = 'Ошибка в форме'
#     else:
#         form = testtableForm()
#         data = testtable.objects.order_by('-index')[:]
#         content = {
#             'form': form,
#             'data': data,
#             'error': error
#         }
#         return render(request, 'analytical_system/test_html.html', content)






