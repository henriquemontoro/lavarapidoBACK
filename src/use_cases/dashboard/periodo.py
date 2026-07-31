import calendar
from datetime import date, datetime, timedelta
from typing import Literal, Optional


def calcular_intervalo(
    ano: int,
    period: Literal["week", "month"],
    mes: Optional[int],
    semana: Optional[int],
) -> tuple[date, date]:
    if period == "month":
        if not mes:
            raise ValueError("mes é obrigatório quando period=month")
        ultimo_dia = calendar.monthrange(ano, mes)[1]
        return date(ano, mes, 1), date(ano, mes, ultimo_dia)

    if not semana:
        raise ValueError("semana é obrigatório quando period=week")
    # ISO 8601: ano-Wsemana-1 (segunda-feira) até +6 dias (domingo).
    segunda = datetime.strptime(f"{ano}-W{semana:02d}-1", "%G-W%V-%u").date()
    return segunda, segunda + timedelta(days=6)
