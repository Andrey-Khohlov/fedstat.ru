def combiner_51(data_dir = '/content/'):
    # Обработка таблицы №51 в Google Colab
    # Выполнил: Арьков Валентин
    import pandas as pd
    import numpy as np
    import os

    file_nr = 51 ## Таблица 51

    # Загружаем файл в Колаб, файл помещается по умолчанию в каталоге /content

    result = pd.DataFrame(columns=('Расшифровка', 'Обозреваемый период', 'Единица измерения', 'Единица физических величин', 'Значение', 
                                       'Дата обновления данных', 'Пол', 'Возраст', 'Тип населенного пункта', 'Частота предоставления данных', 
                                       'Регион', 'Номер файла', 'ссылка'))

    data_name = data_dir + 'data(' + str(file_nr) + ').xls'
    data_name

    # Загружаем без создания заголовка, чтобы сохранить нумерацию ячеек
    dict_df = pd.read_excel(data_name, sheet_name=None, header=None)

    df = dict_df['Данные']
    df.head()

    df.iloc[:,1].value_counts()

    # Пол: Заменяем Мужчины/Женщины на M / F
    sex = df.iloc[:,1] 
    sex[sex == "Мужчины"] = "M"
    sex[sex == "Женщины"] = "F"
    df.iloc[:,1] = sex
    df.head()

    df.iloc[:,1].value_counts()

    # Возраст: Заменяем Всего на _T
    age = df.iloc[:,2] 
    age[age == "Всего"] = "_T"
    df.iloc[:,2] = age
    df.head(10)

    df

    a1 = df.iloc[0,0] #Расшифровка
    a1

    a2 = df.T.iloc[1:, 1]
    a2

    df1 = dict_df['Паспорт']
    df1.head()

    # 'Единица физических величин'
    a4 = df1.iloc[2, 1][2:]
    a4

    # 'Частота предоставления данных': "1 раз в 2 года"
    # Первая строка ячейки
    # начиная с 3 знака и до символа перевода строки
    a10 = df1.iloc[3, 1].split('\n')[0][2:]
    a10

    # 'Дата обновления данных'
    a6 = df1.iloc[6, 1]

    a2 = df.iloc[3:,0].astype(int) #Обозреваемый период
    a2[:5]

    a2.shape

    # Род занятий
    zan = df.iloc[2, 3:]
    zan.iloc[0]

    length = len(a2)*len(zan) # число строк выходной таблицы
    length

    # Значения
    # Разворачиваем данные по столбцам в одну колонку
    a5 = np.ravel(np.transpose(df.iloc[3:,3:]))
    a5

    # Раздел - значение группирующего признака "род занятий"
    # Размножаем на каждую строку
    a13 = list(map(lambda x: [x] * len(a2), zan))

    len(zan)

    # Пол - размножаем для столбцов данных
    a7 = list(df.iloc[3:,1]) * len(zan)

    # Возраст - размножаем для столбцов данных
    a8 = list(df.iloc[3:,2]) * len(zan)

    length

    # формируем таблицу по шаблону:
    output = pd.DataFrame({'Расшифровка': [a1] * length,
                              'Обозреваемый период':list(a2) * len(zan),
                              'Единица измерения': [a4] * length,
                              'Единица физических величин': [a4] * length, 
                              'Значение':a5,
                              'Дата обновления данных': [a6] * length,
                              'Пол':a7,
                              'Возраст': a8,
                              'Тип населенного пункта': ['_T'] * length,
                              'Частота предоставления данных': [a10] * length,
                              'Регион': ['Российская Федерация'] * length,
                              'Номер файла': [file_nr] * length,
                              'Раздел': np.ravel(a13),
                              'ссылка': ['https://fedstat.ru/indicator/58673'] * length
                              })
    result = output

    return output

def combiner_12(data_dir = '/Users/m/Desktop/Data Analise/Стажировка/'):
    # Выполнила Мария
    import os
    import pandas as pd
    import numpy as np
    import openpyxl
    
    file_nr = 12
    #  загружаем файл:
    data_name = data_dir + 'data(' + str(file_nr) + ').xls'
    #  data_name = data_dir
    dict_df = pd.read_excel(data_name, sheet_name=None)
    #  выделим в отдельные датафреймы Данные и Паспорт: 
    df = dict_df['Данные']
    df1 = dict_df['Паспорт']
    #  выделим значения из таблицы Данные:
    a1 = df.columns[0] #  Расшифровка
    a2 = df.T.iloc[1:, 1]  #  Обозреваемый период
    a3=df.iloc[2:, ].iloc[0:,1:].values.ravel()# Числовые значения

    #  выставим значение для поля 'Единица физических величин':
    a4 = [df1.iloc[1, 1][2:]]
    length = len(a2)*len(df.iloc[2:, 1])# длина получаемой таблицы
    #  сформируем таблицу по шаблону:
    result = pd.DataFrame({'Расшифровка': [a1] * length,
                      'Обозреваемый период':np.tile(df.T.iloc[1:, 1].values.astype(int),int(length/len(a2))),
                      'Единица измерения': [df1.iloc[1, 1][2:]] * length,
                      'Единица физических величин': a4 * length, 
                      'Значение':a3,
                      'Дата обновления данных': [df1.iloc[5, 1]] * length,
                      'Пол':(df.iloc[0:, 0][2:]).repeat(len(a2)),
                      'Возраст': ['_T'] * length,
                      'Тип населенного пункта': ['_T'] * length,
                      'Частота предоставления данных': ['A' if df1.iloc[2, 1][:9] == '- Годовая' else df1.iloc[2, 1][2:16]] * length,
                      'Регион': ['Российская Федерация'] * length,
                      'Номер файла': [file_nr] * length,
                      'Раздел': ['_T'] * length,
                      'ссылка': ['https://fedstat.ru/indicator/58462'] * length
                      })
    result["Пол"] = np.where(result["Пол"]=="Всего","_T", result["Пол"])
    result["Пол"]=np.where(result["Пол"]=="Женщины","F", result["Пол"])
    result["Пол"]=np.where(result["Пол"]=="Мужчины","M", result["Пол"])
    result["Единица физических величин"]=np.where(result["Единица физических величин"]=="процент","РТ", result["Единица физических величин"])
    return result

def indicators_scrapper(first_ind = '58536', last_ind = '58468'):
    #  выполнил Андрей Хохлов
    import requests
    from bs4 import BeautifulSoup
    url = 'https://www.fedstat.ru/organizations/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    all_indicators = []
    for a in soup.find_all('a', href=True):
        all_indicators.append(a['href'])
    first = all_indicators.index('/indicator/' + first_ind)
    last = all_indicators.index('/indicator/' + last_ind)
    indicators = []
    for i in range(first, last + 1):
        text = all_indicators[i]
        if text != '#':
            indicators.append(text)
    return indicators

def fedstat_files_loader(indicators):
    #  выполнил Андрей Хохлов
    from selenium import webdriver
    from selenium.webdriver import Firefox
    driver = Firefox(executable_path='/home/dad/anaconda3/bin/geckodriver') # путь к geckodriver 
    url = 'https://fedstat.ru'
    for indicator in indicators:
        driver.get(url + indicator)
        driver.find_element_by_class_name("icon-download").click()
        driver.find_element_by_class_name("backgr-exel").click()
        driver.close()
    

def combiner_8(data_dir = '/home/dad/projects/tgu/test_task/data/'):
    #  выполнил Андрей Хохлов
    ''' Принимает на вход номера файлов для обработки и директорию где эти файлы находятся,
        записывает результрующий файл в директорию по умолчанию и возвращает этот файл как pd.DataFrame.
        Обрабатывает только указанные файлы:
        обработка файлов №№ 0, 32, 33, 19, 36, 38, 45
        индикаторов №№ 58536, 59141, 40552б, 59170, 57314, 60842, 60961
    '''
    import os
    import pandas as pd
    import numpy as np
    import openpyxl
    result = pd.DataFrame(columns=('Расшифровка', 'Обозреваемый период', 'Единица измерения', 'Единица физических величин', 'Значение', 
                                   'Дата обновления данных', 'Пол', 'Возраст', 'Тип населенного пункта', 'Частота предоставления данных', 
                                   'Регион', 'Номер файла', 'Раздел', 'ссылка'))
    for file_nr in [0, 32, 33, 19, 36, 38, 45]:
        #  загружаем файл:
        data_name = data_dir + 'data(' + str(file_nr) + ').xls'
        dict_df = pd.read_excel(data_name, sheet_name=None)
        #  выделим в отдельные датафреймы Данные и Паспорт: 
        df = dict_df['Данные']
        df1 = dict_df['Паспорт']
        # подгонка под стандарт 8 группы:
        if file_nr in (38, 45): 
            df.drop(index=2, inplace=True)          
        #  плавим исходную таблицу:
        if file_nr in (0, 33, 19, 36, 38, 45):
            df.iloc[1, 0:2] = (1, 2)
            df2 = df.rename(columns = df.iloc[1,:].astype(int))
            formatted_df = pd.melt(df2[2:], [1, 2], var_name="period", value_name="numbers")
        elif file_nr == 32:
            df.iloc[1, 0] = 1
            df2 = df.rename(columns = df.iloc[1,:].astype(int))
            formatted_df = pd.melt(df2[2:], [1], var_name="period", value_name="numbers")
        #  заменяем незначащие значения на _Т:
        mask = formatted_df[1].apply(lambda x: x == 'Всего')
        formatted_df[1][mask] = '_T'
        #  выделим значения из таблицы Данные:
        a1 = df.columns[0] #  Расшифровка
        a4 = ['PT' if df1.iloc[1, 1][2:] == 'процент' else df1.iloc[1, 1][2:]] #  выставим значение для поля 'Единица физических величин'
        if file_nr in (36, 38, 45):    #  выставим значение для поля 'Раздел'
            a13 = ['_T'] * len(formatted_df['period'])
        else:
            mask = formatted_df[1].apply(lambda x: x == 'Всего по обследуемым видам экономической деятельности')
            formatted_df[1][mask] = '_T'
            a13 = formatted_df[1].apply(lambda x: x.lstrip()) 
       
        switch_dict = { 
            0: '58536', 
            32: '59141', 
            33: '40552', 
            19: '59170', 
            36: '57314', 
            38: '60842', 
            45: '60961'
        }
        a14 = switch_dict.get(file_nr)
        
        length = len(formatted_df['period']) # длина получаемой таблицы
        #  сформируем таблицу по шаблону:
        output = pd.DataFrame({'Расшифровка': [a1] * length,
                          'Обозреваемый период': formatted_df['period'],
                          'Единица измерения': a4 * length,
                          'Единица физических величин': a4 * length, 
                          'Значение': formatted_df['numbers'],
                          'Дата обновления данных': [df1.iloc[5, 1]] * length,
                          'Пол': ['_T'] * length,
                          'Возраст': ['_T'] * length,
                          'Тип населенного пункта': ['_T'] * length,
                          'Частота предоставления данных': ['A' if df1.iloc[2, 1][:9] == '- Годовая' else df1.iloc[2, 1][2:16]] * length,
                          'Регион': formatted_df[2].apply(lambda x: x.lstrip()) if file_nr == 0 else ['Российская Федерация'] * length,
                          'Номер файла': [file_nr] * length,
                          'Раздел': a13,
                          'ссылка': ['https://fedstat.ru/indicator/' + a14 + ' '] * length 
                          })

        result = pd.concat([result, output], axis=0) #  добавляем сформированную таблицу в результирующую таблицу
    return result

def combiner_1(data_dir = '/home/dad/projects/tgu/test_task/data/'):
    #  выполнил Андрей Хохлов
    ''' Принимает на вход номера файлов для обработки и директорию где эти файлы находятся,
        записывает результрующий файл в директорию по умолчанию и возвращает этот файл как pd.DataFrame.
        Обрабатывает только указанные файлы:
        обработка файлов №№ 3, 7, 8, 10, 23, 24, 26, 27, 31, 34, 35, 39, 44, 56, 58,
        индикаторов №№ 58683, 58684, 59597, 58672, 58525, 58484, 59557, 58527, 58712, 58681, 58702, 58807, 58700, 58517, 58468,
    '''
    import os
    import pandas as pd
    import numpy as np
    import openpyxl
    result = pd.DataFrame(columns=('Расшифровка', 'Обозреваемый период', 'Единица измерения', 'Единица физических величин', 'Значение', 
                                   'Дата обновления данных', 'Пол', 'Возраст', 'Тип населенного пункта', 'Частота предоставления данных', 
                                   'Регион', 'Номер файла', 'Раздел', 'ссылка'))
    for file_nr in [3, 7, 8, 10, 23, 24, 26, 27, 31, 34, 35, 39, 44, 56, 58]:
        #  загружаем файл:
        data_name = data_dir + 'data(' + str(file_nr) + ').xls'
        dict_df = pd.read_excel(data_name, sheet_name=None)
        #  выделим в отдельные датафреймы Данные и Паспорт: 
        df = dict_df['Данные']
        df1 = dict_df['Паспорт']
        #  выделим значения из таблицы Данные:
        a1 = df.columns[0]
        a2 = df.iloc[2:, 0].astype(int)
        a3 = df.iloc[2:, 1]
        #  выставим значение для поля 'Единица физических величин':
        if file_nr not in (35, 39, 56):
            a4 = ['PT' if df1.iloc[1, 1][2:] == 'процент' else df1.iloc[1, 1][2:]]
        elif file_nr == 35:
            a4 =['человек на миллион жителей']
        elif file_nr == 39:
            a4 = ['Количество исследователей (в эквиваленте полной занятости) на миллион жителей']
        elif file_nr == 56:
            a4 =['зарегистрированных больных на 100000 человек']
        
        switch_dict = { 
            3: '58683',
            7: '58684',
            8: '59597',
            10: '58672',
            23: '58525',
            24: '58484',
            26: '59557',
            27: '58527',
            31: '58712',
            34: '58681',
            35: '58702',
            39: '58807',
            44: '58700',
            56: '58517',
            58: '58468',

        }
        
        a14 = switch_dict.get(file_nr)
        
        length = len(a2) # длина получаемой таблицы
        #  сформируем таблицу по шаблону:
        output = pd.DataFrame({'Расшифровка': [a1] * length,
                          'Обозреваемый период': a2 if file_nr != 10 else [df.iloc[1, 1] + ', '] * 2 + df.iloc[2:, 0].astype(int).astype(str),
                          'Единица измерения': ['PT' if df1.iloc[1, 1][2:] == 'процент' else df1.iloc[1, 1][2:]] * length, 
                          'Единица физических величин': a4 * length, 
                          'Значение': df.iloc[2:, 1],
                          'Дата обновления данных': [df1.iloc[5, 1]] * length,
                          'Пол': ['_T'] * length,
                          'Возраст': ['_T'] * length,
                          'Тип населенного пункта': ['_T'] * length,
                          'Частота предоставления данных': ['A' if df1.iloc[2, 1][:9] == '- Годовая' else df1.iloc[2, 1][2:16]] * length,
                          'Регион': ['Российская Федерация'] * length,
                          'Номер файла': [file_nr] * length,
                          'Раздел': ['_T'] * length,
                          'ссылка': ['https://fedstat.ru/indicator/' + a14 + ' '] * length 
                          })
        result = pd.concat([result, output], axis=0) #  добавляем сформированную таблицу в результирующую таблицу
    return result

def combiner_9(data_dir = '/home/dad/projects/tgu/test_task/data/'):
    #  выполнил Андрей Хохлов
    import os
    import pandas as pd
    import numpy as np
    import openpyxl
    result = pd.DataFrame(columns=('Расшифровка', 'Обозреваемый период', 'Единица измерения', 'Единица физических величин', 'Значение', 
                                       'Дата обновления данных', 'Пол', 'Возраст', 'Тип населенного пункта', 'Частота предоставления данных', 
                                       'Регион', 'Номер файла', 'Раздел', 'ссылка'))
    for file_nr in (9, 13, 14, 16, 17):
        #  загружаем файл:
        data_name = data_dir + 'data(' + str(file_nr) + ').xls'
        dict_df = pd.read_excel(data_name, sheet_name=None)
        #  выделим в отдельные датафреймы Данные и Паспорт: 
        df = dict_df['Данные']
        df1 = dict_df['Паспорт']
        if file_nr == 9:
            # подготовка данных:
            df = df.drop(index=[0, 1])
            length = len(df.iloc[:, 0]) # длина получаемой таблицы
            #  экстракция данных из таблицы Данные и паспорт:
            a1 = [df.columns[0]] * length #  Расшифровка
            a2 = df.iloc[:, 0].astype(int) #  Обозреваемый период
            a3 = ['PT' if df1.iloc[1, 1][2:] == 'процент' else df1.iloc[1, 1][2:]] * length #  Единица измерения            
            a4 = ['PT' if df1.iloc[1, 1][2:] == 'процент' else df1.iloc[1, 1][2:]] * length    #  поле 'Единица физических величин':
            a5 = df.iloc[:, 2] #  Значение
            a6 = [df1.iloc[5, 1]] * length #  Дата обновления данных
            a7 = ['_T'] * length #  Пол
            a8 = df.iloc[:, 1]  #  Возраст
            a9 = ['_T'] * length #  Тип населенного пункта'
            a10 = ['A' if df1.iloc[2, 1][:9] == '- Годовая' else df1.iloc[2, 1][2:16]] * length  #  Частота предоставления данных
            a11 = ['Российская Федерация'] * length  # Регион
            a12 = [file_nr] * length  #  Номер файла
            a13 = ['_T'] * length  #  Раздел
            a14 = ['https://fedstat.ru/indicator/59024 '] * length    # ссылка на файл

        if file_nr == 13:
            # подготовка данных:
            df = df.drop(index=[0, 1])
            length = len(df.iloc[:, 1]) # длина получаемой таблицы
            #  экстракция данных из таблицы Данные и паспорт:
            a1 = [df.columns[0] ]* length #  Расшифровка
            a2 = df.iloc[:, 1].astype(int) #  Обозреваемый период
            a3 = ['PT' if df1.iloc[1, 1][2:] == 'процент' else df1.iloc[1, 1][2:]] * length #  Единица измерения 
            a4 = ['PT' if df1.iloc[1, 1][2:] == 'процент' else df1.iloc[1, 1][2:]] * length #  поле 'Единица физических величин':
            a5 = df.iloc[:, 3] #  Значение
            a6 = [df1.iloc[5, 1]] * length #  Дата обновления данных
            a7 = ['_T'] * length #  Пол
            a8 = ['_T'] * length  #  Возраст
            a9 = ['_T'] * length #  Тип населенного пункта'
            a10 = ['A' if df1.iloc[2, 1][:9] == '- Годовая' else df1.iloc[2, 1][2:14]] * length  #  Частота предоставления данных
            a11 = ['Российская Федерация'] * length  # Регион
            a12 = [file_nr] * length  #  Номер файла
            a13 = ['_T'] * length  #  Раздел
            a14 = ['https://fedstat.ru/indicator/58477 '] * length    # ссылка на файл

        if file_nr == 14:
            # подготовка данных:
            df.iloc[1, 0:2] = ('a', 'b')
            df2 = df.rename(columns = df.iloc[1,:])
            df2 = df2.drop(index=[0, 1])
            formatted_df = pd.melt(df2[2:], ['a', 'b'], var_name='c', value_name="numbers")  
            length = len(formatted_df.iloc[:, 1]) # длина получаемой таблицы
            #  экстракция данных из таблицы Данные и паспорт:
            a1 = [df.columns[0]] * length #  Расшифровка
            a2 = formatted_df.iloc[:, 1].astype(int) #  Обозреваемый период
            a3 = ['PT' if df1.iloc[1, 1][2:] == 'процент' else df1.iloc[1, 1][2:]] * length #  Единица измерения 
            a4 = ['PT' if df1.iloc[1, 1][2:] == 'процент' else df1.iloc[1, 1][2:]] * length #  поле 'Единица физических величин':
            a5 = formatted_df.iloc[:, 3] #  Значение
            a6 = [df1.iloc[5, 1]] * length #  Дата обновления данных
            d7 = {'Женщины': 'F', 'Мужчины': 'M', 'Всего': '_T'}
            formatted_df['a'] = formatted_df['a'].map(d7)
            a7 = formatted_df['a'] #  Пол
            a8 = ['_T'] * length  #  Возраст
            d9 = {'Сельская местность': 'R', 'Городская местность': 'U', 'Всего по территории': '_T'}
            formatted_df['c'] = formatted_df['c'].map(d9)
            a9 = formatted_df.iloc[:, 2] #  Тип населенного пункта'
            a10 = ['A' if df1.iloc[2, 1][:9] == '- Годовая' else df1.iloc[2, 1][2:14]] * length  #  Частота предоставления данных
            a11 = ['Российская Федерация'] * length  # Регион
            a12 = [file_nr] * length  #  Номер файла
            a13 = ['_T'] * length  #  Раздел
            a14 = ['https://fedstat.ru/indicator/58711 '] * length    # ссылка на файл

        if file_nr == 16:
            # подготовка данных:
            df.iloc[2, 0:2] = ('a', 'b')
            df2 = df.rename(columns = df.iloc[2,:])
            df2 = df2.drop(index=[0, 2, 1])
            formatted_df = pd.melt(df2, ['a', 'b'], var_name='c', value_name="numbers")  
            length = len(formatted_df.iloc[:, 1]) # длина получаемой таблицы
            #  экстракция данных из таблиц Данные и Паспорт:
            a1 = [df.columns[0]] * length #  Расшифровка
            a2 = formatted_df.iloc[:, 2].astype(int) #  Обозреваемый период
            a3 = ['PT' if df1.iloc[1, 1][2:] == 'процент' else df1.iloc[1, 1][2:]] * length #  Единица измерения 
            a4 = ['PT' if df1.iloc[1, 1][2:] == 'процент' else df1.iloc[1, 1][2:]] * length #  поле 'Единица физических величин':
            a5 = formatted_df.iloc[:, 3] #  Значение
            a6 = [df1.iloc[5, 1]] * length #  Дата обновления данных
            d7 = {'Женщины': 'F', 'Мужчины': 'M', 'Всего': '_T'}
            formatted_df['a'] = formatted_df['a'].map(d7)
            a7 = formatted_df['a'] = formatted_df['a'] #  Пол
            mask = formatted_df['b'].apply(lambda x: x == 'Всего')
            formatted_df['b'][mask] = '_T'
            a8 = formatted_df['b'] #  Возраст
            d9 = {'Сельская местность': 'R', 'Городская местность': 'U', 'Всего по территории': '_T'}
            formatted_df['c'] = formatted_df['c'].map(d9)
            a9 = ['_T'] * length #  Тип населенного пункта'
            a10 = ['A' if df1.iloc[2, 1][:9] == '- Годовая' else df1.iloc[2, 1][2:14]] * length  #  Частота предоставления данных
            a11 = ['Российская Федерация'] * length  # Регион
            a12 = [file_nr] * length  #  Номер файла
            a13 = ['_T'] * length  #  Раздел
            a14 = ['https://fedstat.ru/indicator/58472 '] * length    # ссылка на файл
            
        if file_nr == 17:
        # подготовка данных:
            alphabets=[]
            for i in range(ord('a'), ord('a') + df.shape[1]):
                alphabets.append(chr(i))
            df.iloc[0,:] = alphabets
            df2 = df.rename(columns = df.iloc[0,:])
            df3 = df2.iloc[:3, :]
            df3.iloc[1, -2:] = df3.iloc[1, -3]
            df3.drop(index=0, inplace=True)
            d1 = df3.drop(index=1).to_dict('records')
            d2 = df3.drop(index=2).to_dict('records')
            formatted_df = pd.melt(df2.drop(index=[0, 1, 2]), id_vars=['a', 'b']) 
            formatted_df.dropna(subset=['value'], inplace=True)
            formatted_df['sex'] = formatted_df['variable'].map(*d1)
            formatted_df['year'] = formatted_df['variable'].map(*d2)
            length = len(formatted_df.iloc[:, 1]) # длина получаемой таблицы
            #  экстракция данных из таблиц Данные и Паспорт:
            a1 = [df.columns[0]] * length #  Расшифровка
            a2 = formatted_df.iloc[:, 5].astype(int) #  Обозреваемый период
            a3 = ['PT' if df1.iloc[1, 1][2:] == 'процент' else df1.iloc[1, 1][2:]] * length #  Единица измерения
            a4 = ['PT' if df1.iloc[1, 1][2:] == 'процент' else df1.iloc[1, 1][2:]] * length #  поле 'Единица физических величин':
            a5 = formatted_df.iloc[:, 3] #  Значение
            a6 = [df1.iloc[5, 1]] * length #  Дата обновления данных
            d7 = {'Женщины': 'F', 'Мужчины': 'M', 'Всего': '_T'}
            #  formatted_df['sex'] = formatted_df['sex'].map(d7)
            a7 = formatted_df['sex'].map(d7) #  Пол
            mask = formatted_df['a'].apply(lambda x: x == 'Всего')
            formatted_df['a'][mask] = '_T'
            a8 = formatted_df['a'] #  Возраст
            a9 = ['_T'] * length #  Тип населенного пункта'
            a10 = ['A' if df1.iloc[2, 1][:9] == '- Годовая' else df1.iloc[2, 1][2:14]] * length  #  Частота предоставления данных
            a11 = ['Российская Федерация'] * length  # Регион
            a12 = [file_nr] * length  #  Номер файла
            a13 = ['_T'] * length  #  Раздел
            a14 = ['https://fedstat.ru/indicator/58472 '] * length    # ссылка на файл

        #  сформируем таблицу по шаблону:
        output = pd.DataFrame({'Расшифровка': a1,
                      'Обозреваемый период': a2,
                      'Единица измерения': a3,
                      'Единица физических величин': a4, 
                      'Значение': a5,
                      'Дата обновления данных': a6,
                      'Пол': a7,
                      'Возраст': a8,
                      'Тип населенного пункта': a9,
                      'Частота предоставления данных': a10,
                      'Регион': a11,
                      'Номер файла': a12,
                      'Раздел': a13,
                      'ссылка': a14
                      })
        result = pd.concat([result, output], axis=0) #  добавляем сформированную таблицу в результирующую таблицу
    return result