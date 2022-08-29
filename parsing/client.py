from requests_html import HTMLSession
import json


# Вывод категорий по кнопке услуги
def service(m):
    session = HTMLSession()

    param = session.get(
        f'https://dikidi.app/mobile/ajax/newrecord/company_services/?lang=ru&company={m}&master=&share='
    )

    list_service = param.text
    data = json.loads(list_service)

    service_price = []

    for it in data['data']['list']:

        g = ["text", "callback_data"]
        r = dict.fromkeys(g, data['data']['list'][f'{it}']['name'])

        r.update({'callback_data': f'serv|{str(it)}|{m}'})
        service_price.append(r)

    return service_price


def service_id(m, item):
    session = HTMLSession()

    param = session.get(
        f'https://dikidi.app/mobile/ajax/newrecord/company_services/?lang=ru&company={m}&master=&share='
    )

    list_service = param.text
    data = json.loads(list_service)

    service_usl = []

    for it in data['data']['list'][f'{item}']['services']:
        sda = it['name']
        ass = it['price']
        rttr = it['time']
        prir = it['id']

        g = ["text", "callback_data"]
        r = dict.fromkeys(g, f'{sda} цена:{ass}руб\n время:{rttr}мин')
        r.update({'callback_data': f'usl|{str(prir)}|{m}|{item}'})
        service_usl.append(r)

    return service_usl


def date_id(m, item):
    session = HTMLSession()

    param = session.get(
        f'https://dikidi.app/ru/mobile/ajax/newrecord/get_datetimes/?company_id={m}&service_id%5B%5D={item}&with_first=1'
    )

    list_service = param.text
    data = json.loads(list_service)

    service_date = []

    for it in data['data']['dates_true']:
        date = it
        salon = m
        usluga = item

        g = ["text", "callback_data"]
        r = dict.fromkeys(g, it)
        r.update({'callback_data': f'dat|{str(date)}|{salon}|{usluga}'})
        service_date.append(r)

    return service_date


def date_master(m, date, item):
    session = HTMLSession()

    param = session.get(
        f'https://dikidi.app/ru/mobile/ajax/newrecord/get_datetimes/?company_id={m}&date={date}&service_id%5B%5D={item}'
    )

    list_service = param.text
    data = json.loads(list_service)
    data_master = data['data']['masters']

    service_date = []

    for k, v in data_master.items():
        service_date.append(k)

    master_date = []

    for i in service_date:
        tr = data['data']['masters'][f'{i}']['username']
        g = ["text", "callback_data"]
        r = dict.fromkeys(g, tr)
        r.update({'callback_data': f'mast|{str(date)}|{m}|{item}|{i}'})
        master_date.append(r)

    return master_date


def time_master(m, date, item, mast):
    session = HTMLSession()

    param = session.get(
        f'https://dikidi.app/ru/mobile/ajax/newrecord/get_datetimes/?company_id={m}&date={date}&service_id%5B%5D={item}'
    )

    list_service = param.text
    data = json.loads(list_service)
    data_master = data['data']['times'][f'{mast}']

    service_date = []

    for it in data_master:

        g = ["text", "callback_data"]
        r = dict.fromkeys(g, it)
        r.update({'callback_data': f'tim|{str(date)}|{m}|{item}|{mast}|{it}'})
        service_date.append(r)

    return service_date


def master_select(m):
    session = HTMLSession()

    param = session.get(
        f'https://dikidi.app/ru/ajax/newrecord/to_master_get_masters/?company_id={m}'
    )

    list_service = param.text
    data = json.loads(list_service)

    master_salon = []

    for it in data['masters_order']:

        g = ["text", "callback_data"]
        r = dict.fromkeys(g, data['masters'][f'{it}']['username'])
        r.update({'callback_data': f'MSal|{m}|{it}'})
        master_salon.append(r)

    return master_salon


def master_cat(m, item):
    session = HTMLSession()

    param = session.get(
        f'https://dikidi.app/mobile/ajax/newrecord/company_services/?lang=ru&company={m}&master={item}&share='
    )

    list_service = param.text
    data = json.loads(list_service)
    text = data['data']['list']

    service_usl = []

    for k, v in text.items():
        service_usl.append(k)

    master_category = []

    for it in service_usl:
        g = ["text", "callback_data"]
        r = dict.fromkeys(g, data['data']['list'][f'{it}']['name'])
        r.update({'callback_data': f'Mcat|{m}|{item}|{it}'})
        master_category.append(r)

    return master_category


def master_serv_cat(m, item, u):
    session = HTMLSession()

    param = session.get(
        f'https://dikidi.app/mobile/ajax/newrecord/company_services/?lang=ru&company={m}&master={item}&share='
    )

    list_service = param.text
    data = json.loads(list_service)
    text = data['data']['list'][f'{u}']['services']

    service_usl = []

    for it in text:

        name = it['name']
        price = it['price']
        time = it['time']
        id_usluga = it['id']

        g = ["text", "callback_data"]
        r = dict.fromkeys(g, f'{name} цена:{price}руб\n время:{time}мин')
        r.update({'callback_data': f'MUC|{m}|{item}|{u}|{id_usluga}'})
        service_usl.append(r)

    return service_usl


def master_serv_date(m, item, u):
    session = HTMLSession()

    param = session.get(
        f'https://dikidi.app/ru/mobile/ajax/newrecord/get_datetimes/?company_id={m}&service_id%5B%5D={u}&master_id={item}&with_first=1'
    )

    list_date = param.text
    data = json.loads(list_date)
    text = data['data']['dates_true']

    service_usl = []

    for it in text:

        g = ["text", "callback_data"]
        r = dict.fromkeys(g, it)
        r.update({'callback_data': f'MDC|{m}|{item}|{u}|{it}'})
        service_usl.append(r)

    return service_usl


def master_time_date(m, item, u, d):
    session = HTMLSession()

    param = session.get(
        f'https://dikidi.app/ru/mobile/ajax/newrecord/get_datetimes/?company_id={m}&date={d}&service_id%5B%5D={u}&master_id={item}'
    )

    list_time = param.text
    data = json.loads(list_time)
    text = data['data']['times'][f'{item}']

    service_usl = []

    for it in text:

        g = ["text", "callback_data"]
        r = dict.fromkeys(g, it)
        r.update({'callback_data': f'MtD|{m}|{item}|{u}|{d}|{it}'})
        service_usl.append(r)

    return service_usl


def par_master_info():
    session = HTMLSession()

    param = session.get(
        f'https://dikidi.app/ru/ajax/newrecord/to_master_get_masters/?company_id=225859'
    )

    t = param.text
    data = json.loads(t)

    img = data['masters']['1635673']['image']

    return img


def work_salon_info(m):
    session = HTMLSession()

    param = session.get(
        f'https://dikidi.app/ru/mobile/ajax/newrecord/project_options/?company={m}&session=62d2e1b0f1fd05-28653842&social_key='
    )

    t = param.text
    data = json.loads(t)

    n = ''
    r = ''
    e = ''

    for i in data['data']['company']['schedule']:
        n = i.get('day')
        r = i.get('work_from')
        e = i.get('work_to')

    text = f"{data['data']['company']['name']}.\n" \
           f"Адрес: {data['data']['company']['address']}.\n" \
           f"Режим работы {n} c {r} до {e}.\n" \
           f"Телефон: {data['data']['company']['phone']}."

    return text
