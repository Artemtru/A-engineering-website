#!/usr/bin/env python3
"""Генератор внутренних страниц сайта А-Инжиниринг.

Главная (index.html) правится руками. Этот скрипт создаёт страницы услуг,
объектов, «О компании», политику ПДн и sitemap.xml с общей шапкой и подвалом.

Запуск из корня репозитория:  python3 tools/build.py
После правки текстов здесь — запустить скрипт и загрузить изменённые файлы на хостинг.
"""
import json
import os
from datetime import date
from html import escape

SITE = "https://a-engineering.pro"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = date.today().isoformat()
YM_ID = 114233373
EMAIL = "info@a-engineering.pro"
PHONE1, PHONE1_HREF = "+7 (495) 204-21-50", "+74952042150"
PHONE2, PHONE2_HREF = "+7 (925) 777-72-73", "+79257777273"
ADDRESS = "119530, г. Москва, Очаковское шоссе, д. 34, помещ. 23/4"
ORG_ID = SITE + "/#org"

LOGO_PATH = ("M 105.160156 356.386719 L 205.664062 142.320312 L 398.761719 321.621094 Z "
             "M 612.769531 447.757812 L 471.109375 320.183594 L 515.933594 307.75 L 464.117188 313.882812 "
             "L 202.082031 77.902344 L 15.402344 446.589844 L 414.207031 335.964844 L 534.597656 447.757812 Z "
             "M 612.769531 447.757812")

# ---------------------------------------------------------------- объекты
OBJECTS = {
    "zhk-bestseller": {
        "name": "ЖК «Бестселлер»",
        "meta": "Жилой комплекс, Москва",
        "status": "Работы ведутся",
        "cover": ("/img/g1.jpg", "ЖК «Бестселлер», визуализация застройщика"),
        "systems": [("ОВ", "Отопление и вентиляция"), ("ВК", "Водоснабжение и канализация"),
                    ("ЭОМ", "Электроснабжение и освещение"), ("СС", "Слаботочные системы")],
        "text": [
            "На жилом комплексе «Бестселлер» в Москве ООО «А-Инжиниринг» выполняет полный комплекс работ "
            "по внутренним инженерным системам здания: отопление и вентиляцию, водоснабжение и канализацию, "
            "электроснабжение и освещение, слаботочные сети.",
            "Монтаж ведут собственные бригады компании. Работы идут параллельно с общестроительными, "
            "поэтому разводку сетей согласуем по графику генподрядчика.",
        ],
        "photos": [("/img/b_3458.jpg", "Поэтажные коллекторы отопления на кирпичной стене"),
                   ("/img/b_3414.jpg", "Запорная арматура и трубопроводы теплового пункта"),
                   ("/img/b_3380.jpg", "Корпуса ЖК «Бестселлер» в процессе строительства"),
                   ("/img/b_3374.jpg", "Монолитный каркас корпуса ЖК «Бестселлер»"),
                   ("/img/b_3531.jpg", "Корпус ЖК «Бестселлер», вид сверху"),
                   ("/img/b_3361.jpg", "Строительная площадка ЖК «Бестселлер»")],
        "services": ["otoplenie", "ventilyaciya-i-kondicionirovanie", "vodosnabzhenie-i-kanalizaciya",
                     "elektromontazh-eom", "slabotochnye-sistemy"],
    },
    "zhk-zarechnyj": {
        "name": "ЖК «Заречный»",
        "meta": "Жилой комплекс: 9 корпусов и подземный паркинг",
        "status": "Работы ведутся",
        "cover": ("/img/z1.jpg", "ЖК «Заречный», визуализация застройщика"),
        "systems": [("ИТП", "Индивидуальные тепловые пункты"), ("ОВ", "Отопление и вентиляция"),
                    ("ВК", "Водоснабжение и канализация"), ("ЭОМ", "Электроснабжение и освещение"),
                    ("СС", "Слаботочные системы"), ("АУПТ", "Автоматическое пожаротушение"),
                    ("АУПВ", "Противопожарный водопровод")],
        "text": [
            "Жилой комплекс «Заречный» — девять корпусов и подземный паркинг. ООО «А-Инжиниринг» выполняет "
            "полный комплекс инженерных работ по всем корпусам и паркингу: индивидуальные тепловые пункты, "
            "отопление и вентиляцию, водоснабжение и канализацию, электроснабжение, слаботочные системы, "
            "автоматическое пожаротушение и внутренний противопожарный водопровод.",
            "На фото — смонтированный нашими бригадами тепловой пункт, разводка сетей отопления и "
            "кабельные трассы ЭОМ и СС.",
        ],
        "photos": [("/img/z_3610.jpg", "Тепловой пункт ЖК «Заречный», общий вид"),
                   ("/img/z_3615.jpg", "Насосные группы и трубопроводы ИТП"),
                   ("/img/z_3608.jpg", "Теплообменники и обвязка в тепловом пункте"),
                   ("/img/z_3697.jpg", "Пучки кабелей ЭОМ и СС на перекрытии"),
                   ("/img/z_3689.jpg", "Воздуховоды и трубы отопления в коридоре"),
                   ("/img/z_3920.jpg", "Разводка трубопроводов отопления в полу"),
                   ("/img/z_3947.jpg", "Корпус ЖК «Заречный»"),
                   ("/img/z_3653.jpg", "Фасад корпуса ЖК «Заречный»"),
                   ("/img/z_3571.jpg", "Корпуса ЖК «Заречный» на стадии строительства")],
        "services": ["itp", "otoplenie", "ventilyaciya-i-kondicionirovanie", "vodosnabzhenie-i-kanalizaciya",
                     "elektromontazh-eom", "slabotochnye-sistemy", "pozharotushenie-aupt-aupv"],
    },
}

# ---------------------------------------------------------------- услуги
COMMON_STEPS = [
    ("Заявка", "Звонок, заявка с сайта или проект на почту"),
    ("Выезд инженера", "Осмотр объекта, замеры, изучение проекта"),
    ("Смета", "Подробный расчёт работ и оборудования по позициям"),
    ("Договор", "Фиксируем цену и сроки"),
    ("Монтаж", "Своими бригадами, с отчётами заказчику"),
    ("Сдача", "Пусконаладка и исполнительная документация"),
]

FAQ_PRICE = ("Сколько стоит {what}?",
             "Стоимость зависит от проекта, площади и выбранного оборудования. Мы составляем подробную смету "
             "по позициям работ и материалов бесплатно — по проекту или после выезда инженера на объект. "
             "Цена фиксируется в договоре и не меняется без согласования с заказчиком.")
FAQ_WHO = ("С кем вы работаете?",
           "С генподрядчиками, застройщиками, управляющими компаниями и частными заказчиками в Москве и "
           "Московской области. Можем взять один раздел или всю инженерную часть объекта.")
FAQ_DOCS = ("Сдаёте ли вы исполнительную документацию?",
            "Да. По завершении монтажа проводим пусконаладку и передаём заказчику исполнительную документацию.")

SERVICES = {
    "otoplenie": {
        "short": "Отопление и теплоснабжение",
        "h1": "Монтаж систем отопления в Москве и Московской области",
        "title": "Монтаж отопления в Москве под ключ — А-Инжиниринг",
        "desc": "Монтаж систем отопления, ИТП, узлов учёта тепла и тёплых полов в жилых и коммерческих зданиях "
                "в Москве и МО. Свои бригады, смета бесплатно. ООО «А-Инжиниринг».",
        "lead": "Монтируем внутренние системы отопления и теплоснабжения жилых домов, ЖК и коммерческих "
                "объектов — от поэтажной разводки до тепловых пунктов и узлов учёта.",
        "intro": [
            "ООО «А-Инжиниринг» выполняет монтаж систем отопления на строящихся и реконструируемых объектах. "
            "Работаем по проекту заказчика, при необходимости помогаем с подбором оборудования и составлением сметы.",
            "Отопление часто монтируем вместе с вентиляцией, водоснабжением и тепловым пунктом — так проще "
            "согласовать трассы и сдать инженерную часть одним подрядчиком.",
        ],
        "scope": ["Поэтажная и поквартирная разводка", "Коллекторные узлы и узлы учёта тепла",
                  "Радиаторы и конвекторы", "Тёплые полы", "Стояки и магистральные трубопроводы",
                  "Индивидуальные тепловые пункты (ИТП)", "Котельные", "Опрессовка и пусконаладка"],
        "photos": [("/img/b_3458.jpg", "Поэтажные коллекторы отопления"),
                   ("/img/z_3920.jpg", "Разводка трубопроводов отопления в полу"),
                   ("/img/z_3689.jpg", "Трубы отопления и воздуховоды в коридоре")],
        "faq_what": "монтаж отопления",
        "related": ["itp", "ventilyaciya-i-kondicionirovanie", "vodosnabzhenie-i-kanalizaciya"],
    },
    "itp": {
        "short": "Индивидуальные тепловые пункты (ИТП)",
        "h1": "Монтаж ИТП — индивидуальных тепловых пунктов",
        "title": "Монтаж ИТП в Москве — тепловые пункты под ключ | А-Инжиниринг",
        "desc": "Монтаж индивидуальных тепловых пунктов (ИТП) для жилых комплексов и коммерческих зданий в Москве "
                "и МО: обвязка теплообменников, насосные группы, узлы учёта, пусконаладка.",
        "lead": "Собираем и запускаем индивидуальные тепловые пункты для жилых комплексов и коммерческих зданий. "
                "На фото — ИТП, смонтированный нашими бригадами в ЖК «Заречный».",
        "intro": [
            "Тепловой пункт — сердце системы отопления и горячего водоснабжения здания. От качества обвязки "
            "теплообменников, насосных групп и автоматики зависит, будет ли в квартирах стабильно тепло.",
            "ООО «А-Инжиниринг» монтирует ИТП по проекту, проводит гидравлические испытания и пусконаладку, "
            "передаёт исполнительную документацию. Сейчас ведём монтаж тепловых пунктов в ЖК «Заречный» "
            "(9 корпусов и подземный паркинг).",
        ],
        "scope": ["Монтаж теплообменников и обвязка", "Насосные группы отопления и ГВС",
                  "Запорная и регулирующая арматура", "Узлы учёта тепловой энергии",
                  "Подключение автоматики и шкафов управления", "Гидравлические испытания",
                  "Пусконаладка", "Исполнительная документация"],
        "photos": [("/img/z_3610.jpg", "Тепловой пункт ЖК «Заречный», общий вид"),
                   ("/img/z_3615.jpg", "Насосные группы и трубопроводы ИТП"),
                   ("/img/z_3608.jpg", "Теплообменники и обвязка в тепловом пункте")],
        "faq_what": "монтаж ИТП",
        "related": ["otoplenie", "vodosnabzhenie-i-kanalizaciya", "servisnoe-obsluzhivanie"],
    },
    "ventilyaciya-i-kondicionirovanie": {
        "short": "Вентиляция и кондиционирование",
        "h1": "Монтаж вентиляции и кондиционирования в Москве",
        "title": "Монтаж вентиляции и кондиционирования в Москве | А-Инжиниринг",
        "desc": "Монтаж приточно-вытяжной вентиляции, дымоудаления, VRF-систем и чиллеров в жилых и коммерческих "
                "зданиях в Москве и МО. Пусконаладка, исполнительная документация.",
        "lead": "Монтируем общеобменную вентиляцию, системы дымоудаления и холодоснабжения для жилых комплексов, "
                "офисов и коммерческих помещений.",
        "intro": [
            "ООО «А-Инжиниринг» выполняет монтаж систем вентиляции и кондиционирования по проекту: прокладку "
            "воздуховодов, установку вентиляционного оборудования, систем противодымной защиты и холодоснабжения.",
            "После монтажа проводим пусконаладку и передаём заказчику исполнительную документацию.",
        ],
        "scope": ["Приточно-вытяжная (общеобменная) вентиляция", "Системы дымоудаления и подпора воздуха",
                  "Монтаж воздуховодов и фасонных изделий", "VRF-системы", "Чиллеры и холодоснабжение",
                  "Пусконаладочные работы"],
        "photos": [("/img/z_3689.jpg", "Воздуховоды и трубы в коридоре жилого дома")],
        "faq_what": "монтаж вентиляции",
        "related": ["otoplenie", "elektromontazh-eom", "servisnoe-obsluzhivanie"],
    },
    "vodosnabzhenie-i-kanalizaciya": {
        "short": "Водоснабжение и канализация",
        "h1": "Монтаж водоснабжения и канализации (ВК)",
        "title": "Монтаж водоснабжения и канализации в Москве | А-Инжиниринг",
        "desc": "Монтаж внутренних сетей ХВС, ГВС, бытовой и ливневой канализации, насосных станций и водоподготовки "
                "в Москве и МО. Свои бригады, смета бесплатно.",
        "lead": "Монтируем внутренние сети холодного и горячего водоснабжения, бытовой и ливневой канализации, "
                "насосные станции и узлы ввода.",
        "intro": [
            "ООО «А-Инжиниринг» выполняет раздел ВК на жилых комплексах и коммерческих объектах: от узла ввода "
            "до поэтажной разводки и подключения сантехнических приборов.",
            "Раздел ВК удобно вести вместе с отоплением и тепловым пунктом — горячее водоснабжение готовится в ИТП, "
            "и монтаж одним подрядчиком упрощает стыковку систем.",
        ],
        "scope": ["Узлы ввода водопровода", "Сети ХВС и ГВС", "Бытовая канализация", "Ливневая канализация (ливнёвка)",
                  "Насосные станции и повысительные установки", "Водоподготовка", "Гидравлические испытания"],
        "photos": [],
        "faq_what": "монтаж водоснабжения и канализации",
        "related": ["otoplenie", "itp", "pozharotushenie-aupt-aupv"],
    },
    "elektromontazh-eom": {
        "short": "Электроснабжение и освещение (ЭОМ)",
        "h1": "Электромонтажные работы (ЭОМ) в Москве",
        "title": "Электромонтажные работы ЭОМ в Москве — А-Инжиниринг",
        "desc": "Электромонтаж ЭОМ: ВРУ и щиты, кабельные линии, рабочее и аварийное освещение, заземление в жилых и "
                "коммерческих зданиях в Москве и МО.",
        "lead": "Выполняем внутреннее электрооборудование зданий: силовые сети, щиты, освещение и заземление.",
        "intro": [
            "ООО «А-Инжиниринг» ведёт раздел ЭОМ (электрооборудование, электроосвещение) на жилых комплексах "
            "и коммерческих объектах — от вводно-распределительных устройств до квартирных щитов и светильников.",
            "Кабельные трассы ЭОМ и слаботочных систем прокладываем согласованно, чтобы не было пересечений "
            "и переделок.",
        ],
        "scope": ["ВРУ, ГРЩ и распределительные щиты", "Силовые кабельные линии", "Рабочее освещение",
                  "Аварийное и эвакуационное освещение", "Заземление и уравнивание потенциалов",
                  "Электроизмерительные испытания"],
        "photos": [("/img/z_3697.jpg", "Кабельные трассы ЭОМ и СС на перекрытии")],
        "faq_what": "электромонтаж",
        "related": ["slabotochnye-sistemy", "ventilyaciya-i-kondicionirovanie", "servisnoe-obsluzhivanie"],
    },
    "slabotochnye-sistemy": {
        "short": "Слаботочные системы (СС)",
        "h1": "Монтаж слаботочных систем (СС)",
        "title": "Монтаж слаботочных систем в Москве: СКС, видеонаблюдение, СКУД | А-Инжиниринг",
        "desc": "Монтаж слаботочных систем: СКС и интернет, видеонаблюдение, домофония и СКУД, диспетчеризация "
                "для жилых комплексов и коммерческих объектов в Москве и МО.",
        "lead": "Сети связи и системы безопасности для жилых и коммерческих объектов: СКС, видеонаблюдение, "
                "домофония, контроль доступа и диспетчеризация.",
        "intro": [
            "ООО «А-Инжиниринг» выполняет раздел СС на жилых комплексах: прокладку слаботочных трасс, монтаж "
            "оборудования и пусконаладку систем.",
            "Слаботочные системы монтируем вместе с разделом ЭОМ — трассы согласованы, а заказчик получает "
            "одного ответственного подрядчика.",
        ],
        "scope": ["СКС и сети передачи данных", "Видеонаблюдение", "Домофония", "СКУД — контроль доступа",
                  "Диспетчеризация инженерных систем", "Пусконаладка"],
        "photos": [("/img/z_3697.jpg", "Кабельные трассы ЭОМ и СС на перекрытии")],
        "faq_what": "монтаж слаботочных систем",
        "related": ["elektromontazh-eom", "pozharotushenie-aupt-aupv", "servisnoe-obsluzhivanie"],
    },
    "pozharotushenie-aupt-aupv": {
        "short": "Пожаротушение (АУПТ, АУПВ)",
        "h1": "Монтаж автоматического пожаротушения и противопожарного водопровода",
        "title": "Монтаж АУПТ и АУПВ в Москве — пожаротушение | А-Инжиниринг",
        "desc": "Монтаж автоматических установок пожаротушения (АУПТ), спринклерных систем и внутреннего "
                "противопожарного водопровода (АУПВ) в жилых домах и паркингах в Москве и МО.",
        "lead": "Автоматическое пожаротушение и внутренний противопожарный водопровод в жилых домах и подземных "
                "паркингах.",
        "intro": [
            "ООО «А-Инжиниринг» монтирует спринклерные системы, пожарные краны и насосные станции пожаротушения. "
            "Сейчас выполняем разделы АУПТ и АУПВ в ЖК «Заречный», включая подземный паркинг.",
        ],
        "scope": ["Спринклерные системы", "Внутренний противопожарный водопровод (пожарные краны)",
                  "Насосные станции пожаротушения", "Пожаротушение подземных паркингов", "Гидравлические испытания"],
        "photos": [],
        "faq_what": "монтаж пожаротушения",
        "related": ["vodosnabzhenie-i-kanalizaciya", "slabotochnye-sistemy", "servisnoe-obsluzhivanie"],
    },
    "generalnyj-podryad": {
        "short": "Генеральный подряд",
        "h1": "Генеральный подряд и инженерная часть объекта",
        "title": "Генеральный подряд в Москве — А-Инжиниринг",
        "desc": "Генеральный подряд: строительство зданий, координация смежных разделов, сметы и КП, исполнительная "
                "документация. ООО «А-Инжиниринг», Москва и МО.",
        "lead": "Берём на себя строительство и координацию смежных разделов на объекте — с прозрачной сметой и "
                "сроками в договоре.",
        "intro": [
            "ООО «А-Инжиниринг» выступает генеральным подрядчиком: организует общестроительные работы, координирует "
            "инженерные разделы и ведёт исполнительную документацию.",
            "Собственная сметная экспертиза позволяет готовить подробные сметы и коммерческие предложения, "
            "в которых видна каждая позиция работ и материалов.",
        ],
        "scope": ["Общестроительные работы", "Координация смежных разделов", "Сметы и коммерческие предложения",
                  "Графики работ", "Исполнительная документация"],
        "photos": [("/img/z_3571.jpg", "Корпуса жилого комплекса на стадии строительства")],
        "faq_what": "генеральный подряд",
        "related": ["otoplenie", "elektromontazh-eom", "servisnoe-obsluzhivanie"],
    },
    "servisnoe-obsluzhivanie": {
        "short": "Сервисное обслуживание",
        "h1": "Сервисное обслуживание инженерных систем",
        "title": "Обслуживание инженерных систем в Москве — А-Инжиниринг",
        "desc": "Плановое обслуживание и ремонт инженерных систем зданий: регламентные работы, аварийный выезд, "
                "гарантийный сервис. Москва и Московская область.",
        "lead": "Обслуживаем инженерные системы после сдачи объекта: регламентные работы, ремонт и аварийный выезд.",
        "intro": [
            "ООО «А-Инжиниринг» обслуживает смонтированные системы отопления, вентиляции, водоснабжения, "
            "электроснабжения и тепловые пункты. Знаем объекты изнутри, потому что сами их монтировали.",
        ],
        "scope": ["Регламентные работы по графику", "Аварийный выезд", "Гарантийный сервис",
                  "Ремонт и замена оборудования", "Обслуживание ИТП"],
        "photos": [],
        "faq_what": "обслуживание",
        "related": ["itp", "otoplenie", "ventilyaciya-i-kondicionirovanie"],
    },
}

SERVICE_ORDER = ["otoplenie", "itp", "ventilyaciya-i-kondicionirovanie", "vodosnabzhenie-i-kanalizaciya",
                 "elektromontazh-eom", "slabotochnye-sistemy", "pozharotushenie-aupt-aupv",
                 "generalnyj-podryad", "servisnoe-obsluzhivanie"]


# ---------------------------------------------------------------- шаблон
def svc_url(slug): return f"/uslugi/{slug}/"
def obj_url(slug): return f"/obekty/{slug}/"


def head(title, desc, path, ld, og_image="/img/og.jpg"):
    ld_html = "\n".join(
        '<script type="application/ld+json">\n' + json.dumps(x, ensure_ascii=False, indent=1) + "\n</script>"
        for x in ld)
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{SITE}{path}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="120x120" href="/favicon.png">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="А-Инжиниринг">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}{og_image}">
<meta name="theme-color" content="#16202A">
{ld_html}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css">
</head>
<body>
"""


def header():
    return f"""<header class="top">
  <div class="wrap">
    <a href="/" class="logo" aria-label="А-Инжиниринг — на главную"><svg class="logo-mark" viewBox="15 77 598 371" aria-hidden="true"><path fill="currentColor" d="{LOGO_PATH}"/></svg><span class="logo-text">А-Инжиниринг</span></a>
    <nav class="nav" id="nav">
      <a href="/uslugi/">Услуги</a>
      <a href="/obekty/">Объекты</a>
      <a href="/o-kompanii/">О компании</a>
      <a href="/#contacts">Контакты</a>
    </nav>
    <a class="top-phone" href="tel:{PHONE1_HREF}">{PHONE1}</a>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="nav">Меню</button>
  </div>
</header>
"""


def footer():
    links = "".join(f'<a href="{svc_url(s)}">{escape(SERVICES[s]["short"])}</a>' for s in SERVICE_ORDER)
    return f"""<div class="lightbox" id="lb" role="dialog" aria-label="Просмотр фото"><img alt=""></div>
<footer>
  <div class="wrap">
    <nav class="foot-nav" aria-label="Услуги">{links}<a href="/obekty/">Объекты</a><a href="/o-kompanii/">О компании</a><a href="/politika-konfidencialnosti/">Политика конфиденциальности</a></nav>
    <span class="foot-logo"><svg class="foot-mark" viewBox="15 77 598 371" aria-hidden="true"><path fill="currentColor" d="{LOGO_PATH}"/></svg>© 2026 ООО «А-Инжиниринг»</span>
    <span>ИНН 9729423201 · ОГРН 1267700271200</span>
  </div>
</footer>
<script>
const burger=document.getElementById('burger'),nav=document.getElementById('nav');
burger.addEventListener('click',()=>{{const o=nav.classList.toggle('open');burger.setAttribute('aria-expanded',o);}});
const lb=document.getElementById('lb'),lbi=lb.querySelector('img');
document.querySelectorAll('.gallery img').forEach(i=>i.addEventListener('click',()=>{{lbi.src=i.src;lbi.alt=i.alt;lb.classList.add('show');}}));
lb.addEventListener('click',()=>lb.classList.remove('show'));
document.addEventListener('keydown',e=>{{if(e.key==='Escape')lb.classList.remove('show');}});
</script>
<!-- Яндекс.Метрика -->
<script>
var YM_ID = {YM_ID};
(function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}})
(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
ym(YM_ID, "init", {{clickmap:true, trackLinks:true, accurateTrackBounce:true, webvisor:true}});
function goal(name){{ if (window.ym) ym(YM_ID, "reachGoal", name); }}
document.querySelectorAll('a[href^="tel:"]').forEach(function(a){{a.addEventListener('click',function(){{goal('phone_click');}});}});
document.querySelectorAll('a[href^="mailto:"]').forEach(function(a){{a.addEventListener('click',function(){{goal('email_click');}});}});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/{YM_ID}" style="position:absolute;left:-9999px" alt=""></div></noscript>
</body>
</html>
"""


def crumbs_html(items):
    parts = ['<a href="/">Главная</a>']
    for name, path in items[:-1]:
        parts.append(f'<a href="{path}">{escape(name)}</a>')
    parts.append(f'<span aria-current="page" style="margin:0;opacity:1">{escape(items[-1][0])}</span>')
    return '<nav class="crumbs" aria-label="Навигация">' + '<span>/</span>'.join(parts) + "</nav>"


def crumbs_ld(items):
    lst = [{"@type": "ListItem", "position": 1, "name": "Главная", "item": SITE + "/"}]
    for i, (name, path) in enumerate(items, start=2):
        lst.append({"@type": "ListItem", "position": i, "name": name, "item": SITE + path})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": lst}


def page_hero(items, h1, lead, actions=True):
    act = (f'<div class="hero-actions"><a href="/#request" class="btn btn-main">Рассчитать смету</a>'
           f'<a href="tel:{PHONE1_HREF}" class="btn btn-ghost">{PHONE1}</a></div>') if actions else ""
    return f"""<main>
<section class="page-hero">
  <div class="wrap">
    {crumbs_html(items)}
    <h1>{escape(h1)}</h1>
    <p class="lead">{escape(lead)}</p>
    {act}
  </div>
</section>
"""


def cta(text="Пришлите проект или опишите задачу — инженер свяжется с вами в рабочее время и подготовит смету."):
    return f"""<section class="cta">
  <div class="wrap">
    <div><h2>Рассчитаем стоимость вашего объекта</h2><p>{escape(text)}</p></div>
    <div class="cta-side">
      <a class="tel" href="tel:{PHONE1_HREF}">{PHONE1}</a>
      <a class="tel" style="font-size:22px;font-weight:500;color:#C9D1D7" href="tel:{PHONE2_HREF}">{PHONE2}</a>
      <a href="mailto:{EMAIL}" style="color:#C9D1D7">{EMAIL}</a>
      <a href="/#request" class="btn btn-main" style="margin-top:8px">Оставить заявку</a>
    </div>
  </div>
</section>
</main>
"""


def gallery(photos):
    if not photos:
        return ""
    imgs = "".join(f'<img src="{src}" alt="{escape(alt)}" loading="lazy" width="1000" height="750">' for src, alt in photos)
    return f'<div class="gallery" style="margin-top:36px">{imgs}</div>'


def write(path, html):
    out = os.path.join(ROOT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)


# ---------------------------------------------------------------- страницы
def build_service(slug):
    s = SERVICES[slug]
    path = svc_url(slug)
    items = [("Услуги", "/uslugi/"), (s["short"], path)]
    faq = [(FAQ_PRICE[0].format(what=s["faq_what"]), FAQ_PRICE[1]), FAQ_WHO, FAQ_DOCS]
    objs = [k for k, o in OBJECTS.items() if slug in o["services"]]
    ld = [
        crumbs_ld(items),
        {"@context": "https://schema.org", "@type": "Service", "name": s["h1"], "serviceType": s["short"],
         "description": s["desc"], "url": SITE + path, "provider": {"@id": ORG_ID},
         "areaServed": [{"@type": "City", "name": "Москва"}, {"@type": "State", "name": "Московская область"}]},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]
    intro = "".join(f"<p>{escape(p)}</p>" for p in s["intro"])
    scope = "".join(f"<li>{escape(x)}</li>" for x in s["scope"])
    steps = "".join(f'<div class="step"><div class="step-num">{i}</div><h3>{escape(t)}</h3><p>{escape(d)}</p></div>'
                    for i, (t, d) in enumerate(COMMON_STEPS, 1))
    obj_cards = "".join(
        f'<a class="card card-img" href="{obj_url(k)}"><img src="{OBJECTS[k]["cover"][0]}" alt="{escape(OBJECTS[k]["cover"][1])}" loading="lazy">'
        f'<div class="card-body"><h3>{escape(OBJECTS[k]["name"])}</h3><p>{escape(OBJECTS[k]["meta"])}</p>'
        f'<span class="more">Подробнее об объекте →</span></div></a>' for k in objs)
    obj_block = (f'<section class="page-sec alt"><div class="wrap"><h2>Объекты, где мы выполняем эти работы</h2>'
                 f'<div class="cards">{obj_cards}</div></div></section>') if objs else ""
    rel = "".join(f'<a class="card" href="{svc_url(r)}"><h3>{escape(SERVICES[r]["short"])}</h3>'
                  f'<p>{escape(SERVICES[r]["lead"])}</p><span class="more">Подробнее →</span></a>' for r in s["related"])
    faq_html = "".join(f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in faq)
    html = (head(s["title"], s["desc"], path, ld) + header() + page_hero(items, s["h1"], s["lead"]) + f"""
<section class="page-sec">
  <div class="wrap">
    <div class="prose">{intro}</div>
    {gallery(s["photos"])}
  </div>
</section>
<section class="page-sec alt">
  <div class="wrap">
    <h2>Что входит в работы</h2>
    <ul class="checks">{scope}</ul>
  </div>
</section>
<section class="page-sec">
  <div class="wrap">
    <h2>Как мы работаем</h2>
    <div class="steps">{steps}</div>
  </div>
</section>
{obj_block}
<section class="page-sec">
  <div class="wrap">
    <h2>Частые вопросы</h2>
    <div class="faq">{faq_html}</div>
  </div>
</section>
<section class="page-sec alt">
  <div class="wrap">
    <h2>Смежные работы</h2>
    <div class="cards">{rel}</div>
  </div>
</section>
""" + cta() + footer())
    write(path, html)
    return path


def build_services_hub():
    path = "/uslugi/"
    items = [("Услуги", path)]
    cards = "".join(f'<a class="card" href="{svc_url(k)}"><h3>{escape(SERVICES[k]["short"])}</h3>'
                    f'<p>{escape(SERVICES[k]["lead"])}</p><span class="more">Подробнее →</span></a>' for k in SERVICE_ORDER)
    ld = [crumbs_ld(items),
          {"@context": "https://schema.org", "@type": "ItemList", "name": "Услуги ООО «А-Инжиниринг»",
           "itemListElement": [{"@type": "ListItem", "position": i, "url": SITE + svc_url(k), "name": SERVICES[k]["short"]}
                               for i, k in enumerate(SERVICE_ORDER, 1)]}]
    html = (head("Услуги по монтажу инженерных систем в Москве | А-Инжиниринг",
                 "Монтаж отопления, ИТП, вентиляции, водоснабжения и канализации, ЭОМ, слаботочных систем и "
                 "пожаротушения в Москве и МО. Генподряд и сервис. ООО «А-Инжиниринг».", path, ld)
            + header() + page_hero(items, "Услуги по монтажу инженерных систем",
                                   "Берём на себя инженерную часть объекта целиком или отдельные разделы. Работаем с "
                                   "генподрядчиками, застройщиками, управляющими компаниями и частными заказчиками.")
            + f'<section class="page-sec"><div class="wrap"><div class="cards">{cards}</div></div></section>'
            + cta() + footer())
    write(path, html)
    return path


def build_object(slug):
    o = OBJECTS[slug]
    path = obj_url(slug)
    items = [("Объекты", "/obekty/"), (o["name"], path)]
    ld = [crumbs_ld(items)]
    text = "".join(f"<p>{escape(p)}</p>" for p in o["text"])
    systems = "".join(f"<li><b>{escape(a)}</b>{escape(b)}</li>" for a, b in o["systems"])
    svc = "".join(f'<a class="card" href="{svc_url(k)}"><h3>{escape(SERVICES[k]["short"])}</h3>'
                  f'<span class="more">Подробнее об услуге →</span></a>' for k in o["services"])
    html = (head(f"{o['name']} — инженерные системы | А-Инжиниринг",
                 f"{o['name']}: {o['meta'].lower()}. ООО «А-Инжиниринг» выполняет монтаж инженерных систем: "
                 + ", ".join(a for a, _ in o["systems"]) + ". Фото с объекта.", path, ld, og_image=o["cover"][0])
            + header() + page_hero(items, o["name"], o["meta"] + ". Статус: " + o["status"].lower() + ".", actions=False)
            + f"""
<section class="page-sec">
  <div class="wrap"><div class="project" style="padding:0;background:none">
    <figure class="project-main"><img src="{o['cover'][0]}" alt="{escape(o['cover'][1])}"><figcaption>Визуализация застройщика</figcaption></figure>
    <div class="project-info">
      <span class="status">{escape(o['status'])}</span>
      <div class="prose" style="margin-top:16px">{text}</div>
      <ul class="systems">{systems}</ul>
    </div>
  </div></div>
</section>
<section class="page-sec alt">
  <div class="wrap">
    <h2>Фото с объекта</h2>
    {gallery(o['photos'])}
  </div>
</section>
<section class="page-sec">
  <div class="wrap">
    <h2>Работы на объекте</h2>
    <div class="cards">{svc}</div>
  </div>
</section>
""" + cta() + footer())
    write(path, html)
    return path


def build_objects_hub():
    path = "/obekty/"
    items = [("Объекты", path)]
    cards = "".join(
        f'<a class="card card-img" href="{obj_url(k)}"><img src="{o["cover"][0]}" alt="{escape(o["cover"][1])}" loading="lazy">'
        f'<div class="card-body"><h3>{escape(o["name"])}</h3><p>{escape(o["meta"])} · '
        + ", ".join(a for a, _ in o["systems"]) + '</p><span class="more">Подробнее →</span></div></a>'
        for k, o in OBJECTS.items())
    html = (head("Объекты — жилые комплексы | А-Инжиниринг",
                 "Объекты ООО «А-Инжиниринг»: ЖК «Бестселлер» и ЖК «Заречный». Монтаж ИТП, ОВ, ВК, ЭОМ, СС, АУПТ "
                 "и АУПВ. Фото с объектов.", path, [crumbs_ld(items)])
            + header() + page_hero(items, "Наши объекты",
                                   "Жилые комплексы, на которых мы ведём полный комплекс инженерных работ.", actions=False)
            + f'<section class="page-sec"><div class="wrap"><div class="cards">{cards}</div></div></section>'
            + cta() + footer())
    write(path, html)
    return path


def build_about():
    path = "/o-kompanii/"
    items = [("О компании", path)]
    req = [("Полное название", "Общество с ограниченной ответственностью «А-ИНЖИНИРИНГ»"),
           ("Краткое название", "ООО «А-ИНЖИНИРИНГ»"), ("ИНН / КПП", "9729423201 / 772901001"),
           ("ОГРН", "1267700271200"), ("Адрес", ADDRESS), ("Директор", "Хасянзянов Марсель Завдатевич"),
           ("Р/с", "40702810601640002833"), ("Банк", "АО «Альфа-Банк», г. Москва"), ("БИК", "044525593"),
           ("К/с", "30101810200000000593"), ("Телефоны", f"{PHONE1}, {PHONE2}"), ("Почта", EMAIL),
           ("Сайт", "a-engineering.pro")]
    dl = "".join(f"<dt>{escape(a)}</dt><dd>{escape(b)}</dd>" for a, b in req)
    ld = [crumbs_ld(items),
          {"@context": "https://schema.org", "@type": "AboutPage", "url": SITE + path, "about": {"@id": ORG_ID}}]
    html = (head("О компании ООО «А-Инжиниринг» — реквизиты, ИНН 9729423201",
                 "ООО «А-Инжиниринг» (ИНН 9729423201, ОГРН 1267700271200) — монтаж инженерных систем в Москве и МО. "
                 "Реквизиты, адрес, контакты.", path, ld)
            + header() + page_hero(items, "О компании «А-Инжиниринг»",
                                   "Монтажная компания полного цикла: инженерные системы жилых комплексов и "
                                   "коммерческих зданий в Москве и Московской области.")
            + f"""
<section class="page-sec">
  <div class="wrap prose">
    <p>ООО «А-Инжиниринг» выполняет монтаж внутренних инженерных систем: отопления и тепловых пунктов, вентиляции и
    кондиционирования, водоснабжения и канализации, электроснабжения и освещения, слаботочных систем,
    автоматического пожаротушения и противопожарного водопровода. Также выступаем генеральным подрядчиком и
    обслуживаем смонтированные системы.</p>
    <p>Работаем с генподрядчиками, застройщиками, управляющими компаниями и частными заказчиками. Монтаж ведут
    собственные бригады, смета расписывается по каждой позиции работ и материалов, сроки закрепляются в договоре.</p>
    <p>Сейчас компания ведёт работы на <a href="{obj_url('zhk-bestseller')}">ЖК «Бестселлер»</a> в Москве и
    <a href="{obj_url('zhk-zarechnyj')}">ЖК «Заречный»</a> (9 корпусов и подземный паркинг).</p>
  </div>
</section>
<section class="page-sec alt">
  <div class="wrap">
    <h2>Реквизиты</h2>
    <dl class="req-table">{dl}</dl>
  </div>
</section>
""" + cta() + footer())
    write(path, html)
    return path


def build_privacy():
    path = "/politika-konfidencialnosti/"
    items = [("Политика конфиденциальности", path)]
    body = f"""
<h2>1. Общие положения</h2>
<p>Настоящая политика определяет порядок обработки персональных данных пользователей сайта a-engineering.pro
(далее — Сайт) в соответствии с Федеральным законом от 27.07.2006 № 152-ФЗ «О персональных данных».</p>
<p>Оператор персональных данных — ООО «А-ИНЖИНИРИНГ», ИНН 9729423201, ОГРН 1267700271200, адрес: {ADDRESS}.
Контакт для обращений по вопросам персональных данных: {EMAIL}.</p>
<h2>2. Какие данные мы обрабатываем</h2>
<p>Имя, номер телефона и текст сообщения, которые пользователь сам указывает в форме заявки. Также сервис
Яндекс.Метрика собирает обезличенные данные о посещении Сайта (cookie, IP-адрес, сведения о браузере и действиях на Сайте).</p>
<h2>3. Цели обработки</h2>
<p>Связаться с пользователем по его заявке, подготовить расчёт стоимости работ и коммерческое предложение;
анализировать посещаемость Сайта для его улучшения.</p>
<h2>4. Правовое основание</h2>
<p>Согласие пользователя, которое он даёт, отправляя форму заявки на Сайте.</p>
<h2>5. Порядок обработки</h2>
<p>Данные из формы заявки передаются на электронную почту Оператора и в базе данных Сайта не сохраняются.
Для пересылки заявки используется облачный сервис обработки запросов. Оператор не передаёт персональные данные
третьим лицам, за исключением случаев, предусмотренных законодательством РФ.</p>
<p>Данные хранятся не дольше, чем этого требуют цели обработки, после чего удаляются.</p>
<h2>6. Права пользователя</h2>
<p>Пользователь может запросить сведения об обработке своих данных, потребовать их уточнения или удаления, а
также отозвать согласие, направив запрос на {EMAIL}. Оператор ответит в сроки, установленные законом.</p>
<h2>7. Изменение политики</h2>
<p>Оператор вправе изменять настоящую политику. Актуальная версия всегда размещена на этой странице.</p>
<p>Редакция от {TODAY}.</p>
"""
    html = (head("Политика конфиденциальности — А-Инжиниринг",
                 "Политика обработки персональных данных пользователей сайта a-engineering.pro, ООО «А-Инжиниринг».",
                 path, [crumbs_ld(items)])
            + header() + page_hero(items, "Политика обработки персональных данных",
                                   "ООО «А-ИНЖИНИРИНГ», сайт a-engineering.pro", actions=False)
            + f'<section class="page-sec"><div class="wrap prose policy">{body}</div></section></main>' + footer())
    write(path, html)
    return path


def build_sitemap(paths):
    urls = ["/"] + paths
    pri = {"/": "1.0", "/uslugi/": "0.9", "/obekty/": "0.7", "/o-kompanii/": "0.6", "/politika-konfidencialnosti/": "0.2"}
    rows = "".join(
        f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>"
        f"{pri.get(u, '0.8' if u.startswith('/uslugi/') else '0.7')}</priority>\n  </url>\n" for u in urls)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                + rows + "</urlset>\n")


def build_404():
    """Страница «не найдено»: не индексируется, ведёт на услуги и главную. Подключена в .htaccess."""
    links = "".join(f'<li><a href="{svc_url(s)}">{escape(SERVICES[s]["short"])}</a></li>' for s in SERVICE_ORDER)
    html = head("Страница не найдена — А-Инжиниринг", "Такой страницы нет на сайте А-Инжиниринг.", "/404.html", [])
    html = html.replace('<link rel="canonical" href="https://a-engineering.pro/404.html">',
                        '<meta name="robots" content="noindex, follow">')
    html += header() + page_hero([("Страница не найдена", None)], "Страница не найдена",
                                 "Возможно, ссылка устарела. Посмотрите наши услуги или вернитесь на главную.")
    html += f"""<section><div class="wrap"><ul class="checks">{links}</ul>
<p style="margin-top:28px"><a class="btn btn-main" href="/">На главную</a></p></div></section>
</main>
""" + footer()
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    paths = [build_services_hub()] + [build_service(s) for s in SERVICE_ORDER]
    paths += [build_objects_hub()] + [build_object(o) for o in OBJECTS]
    paths += [build_about(), build_privacy()]
    build_sitemap(paths)
    build_404()
    print("\n".join(paths))
