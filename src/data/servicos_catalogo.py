from typing import List, Optional, TypedDict


class ServicoCatalogo(TypedDict):
    title: str
    minutes: int
    price: float
    detalhamento: Optional[List[str]]


# Catálogo real de serviços do Lava-Rápido Nogueira. A ORDEM da lista é a
# ordem operacional de execução (o que é feito primeiro). Pacotes com
# "detalhamento" viram várias etapas checáveis no atendimento; sem
# detalhamento, o pacote inteiro é uma única etapa.
SERVICE_CATALOG: List[ServicoCatalogo] = [
    {"title": "Lavagem do Motor", "minutes": 60, "price": 35.0, "detalhamento": None},
    {
        "title": "Lavagem Simples",
        "minutes": 20,
        "price": 50.0,
        "detalhamento": [
            "Lavagem do tapete",
            "Aspiração",
            "Pano úmido",
            "Limpeza vidro",
            "Secagem do tapete",
            "Pretinho",
            "Cheirinho",
        ],
    },
    {
        "title": "Lavagem Completa",
        "minutes": 60,
        "price": 90.0,
        "detalhamento": [
            "Jato de alta pressão",
            "Shampoo de cima a baixo",
            "Enxágue",
            "Secagem",
            "Sopro de ar",
            "Lavagem do tapete",
            "Aspiração",
            "Pano úmido",
            "Limpeza vidro",
            "Secagem do tapete",
            "Pretinho",
            "Cheirinho",
        ],
    },
    {"title": "Polimento", "minutes": 240, "price": 500.0, "detalhamento": None},
    {"title": "Cera", "minutes": 20, "price": 30.0, "detalhamento": None},
    {"title": "Higienização do Couro", "minutes": 120, "price": 75.0, "detalhamento": None},
    {"title": "Higienização do Tecido", "minutes": 100, "price": 50.0, "detalhamento": None},
]

_BY_TITLE = {item["title"]: item for item in SERVICE_CATALOG}
_ORDER_INDEX = {item["title"]: index for index, item in enumerate(SERVICE_CATALOG)}


def get_price(title: str) -> float:
    item = _BY_TITLE.get(title)
    return item["price"] if item else 0.0


def calcular_preco_total(servicos: Optional[List[str]]) -> float:
    return sum(get_price(title) for title in (servicos or []))


def expandir_em_etapas(servicos: Optional[List[str]]) -> List[str]:
    """Expande os pacotes selecionados em etapas checáveis, na ordem
    operacional certa (independente da ordem em que foram selecionados).
    Pacotes sem detalhamento viram uma única etapa (o próprio nome)."""
    ordenados = sorted(servicos or [], key=lambda title: _ORDER_INDEX.get(title, len(SERVICE_CATALOG)))
    etapas: List[str] = []
    for title in ordenados:
        item = _BY_TITLE.get(title)
        if not item:
            continue
        detalhamento = item["detalhamento"]
        if detalhamento:
            etapas.extend(f"{title} · {passo}" for passo in detalhamento)
        else:
            etapas.append(title)
    return etapas
