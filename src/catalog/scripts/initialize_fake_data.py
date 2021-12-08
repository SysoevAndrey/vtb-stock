import asyncio
from typing import Iterable

from elasticsearch._async.client import AsyncElasticsearch
from catalog.core.domain.card import Card
from catalog.entrypoint.config import Config
from catalog.infrastructure.gateways.es_cards_save_service import ESCardsSaveService
from catalog.core.domain.card_document import CardCategory, CardDocument, KeywordParameter, NumberParameter
import random
from uuid import uuid4

LOREM_IPSUM = """
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut
labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit
esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident,
sunt in culpa qui officia deserunt mollit anim id est laborum.
"""


def _fake_paths():
    return [
        [
            CardCategory(
                id="smartphones", parent="electronics", image="https://picsum.photos/200/300", label="Смартфоны"
            )
        ],
        [
            CardCategory(
                id="accessories", parent="electronics", image="https://picsum.photos/200/300", label="Аксессуары"
            )
        ],
        [
            CardCategory(
                id="button_phones",
                parent="electronics",
                image="https://picsum.photos/200/300",
                label="Кнопочные телефоны",
            )
        ],
    ]


def _choice_path():
    return random.choice(_fake_paths())


def _generate_fake_categories():
    root_category = CardCategory(
        id="electronics", parent=None, image="https://picsum.photos/200/300", label="Электроника"
    )
    return [root_category] + _choice_path()


def _fake_number_params():
    return [
        ("price", "Цена"),
        ("memory", "Встроенная память, в Гб"),
        ("ram", "Оперативная память, в Гб"),
        ("capacity", "Емкость аккумулятора, в мА-ч"),
    ]


def _display_type():
    return random.choice(
        [
            "AMOLED",
            "Dynamic AMOLED",
            "IPS",
            "LTPS",
            "Liquid Retina HD",
            "OLED",
            "PLS",
            "Retina HD",
            "Super AMOLED",
            "Super AMOLED Plus",
        ]
    )


def _generate_fake_number_params():
    return [
        NumberParameter(id=param_id, label=param_label, value=float(random.randint(1000, 192231)))
        for param_id, param_label in _fake_number_params()
    ]


def _year():
    return random.choice(["2015", "2016", "2017", "2018", "2019", "2020", "2021"])


def _display_frequency():
    return random.choice(["120", "144", "60", "90"])


def _biometric():
    return random.choice(
        ["Отсутствует", "распознавание лица", "распознавание сетчатки глаза", "сканер отпечатка пальца"]
    )


def _operation_system():
    return random.choice(["Android", "iOS"])


def _brand():
    return random.choice(["Infinix", "Itel", "Jinga", "Lenovo", "Apple", "MEIZU", "Maxvi", "NOKIA", "POCO", "Samsung"])


def _fake_keyword_params():
    return [
        ("brand", "Производитель", _brand),
        ("biometric", "Биометрическая защита", _biometric),
        ("os", "Операционная система", _operation_system),
        ("display_type", "Тип дисплея", _display_type),
        ("display_frequency_hz", "Частота обновления дисплея, в Гц", _display_frequency),
        ("year", "Год выхода модели", _year),
    ]


def _generate_fake_keyword_params():
    return [
        KeywordParameter(id=param_id, label=param_label, values=[param_callback() for _ in range(1, 4)])
        for param_id, param_label, param_callback in _fake_keyword_params()
    ]


def _generate_fake_data() -> Iterable[CardDocument]:
    random_labels = LOREM_IPSUM.split()
    print(len(random_labels))
    for _ in range(1000):
        identifier = uuid4()
        categories = _generate_fake_categories()
        number_parameters = _generate_fake_number_params()
        keyword_parameters = _generate_fake_keyword_params()
        yield CardDocument(
            item=Card(
                id=identifier,
                image="https://picsum.photos/200/300",
                price=int(next(filter(lambda item: item.id == "price", number_parameters)).value),
                label=random.choice(random_labels),
                rating=random.random() * 5,
                reviews_count=random.randint(5, 1000),
                path=f"/stock/electronics/{identifier}",
            ),
            type="products",
            number_parameters=number_parameters,
            keyword_parameters=keyword_parameters,
            categories=categories,
        )


async def main(config_obj: Config):
    es_client = AsyncElasticsearch(
        hosts=[{"host": config_obj.elasticsearch_host, "port": config_obj.elasticsearch_port}]
    )
    service = ESCardsSaveService(es_client=es_client, index_name=config_obj.elasticsearch_cards_index)

    data = _generate_fake_data()

    await service.bulk_save_documents(list(data))


if __name__ == "__main__":
    asyncio.run(main(Config()))
