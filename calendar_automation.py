#!/usr/bin/env python3
"""Automação de calendário com integração REST.

Busca feriados públicos via API e gera um planejamento simples para os próximos dias.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Dict, List

import requests

API_URL = "https://date.nager.at/api/v3/PublicHolidays/{year}/{country}"


@dataclass
class DayPlan:
    day: date
    weekday: str
    is_weekend: bool
    holiday_name: str | None


def fetch_holidays(country: str, year: int) -> Dict[date, str]:
    """Retorna os feriados do país/ano informado no formato {data: nome}."""
    response = requests.get(API_URL.format(year=year, country=country), timeout=15)
    response.raise_for_status()

    holidays: Dict[date, str] = {}
    for item in response.json():
        holiday_date = datetime.strptime(item["date"], "%Y-%m-%d").date()
        holidays[holiday_date] = item["localName"]
    return holidays


def build_plan(country: str, start_day: date, days: int) -> List[DayPlan]:
    """Monta o plano de dias com marcação de fim de semana e feriado."""
    holidays_by_date = fetch_holidays(country, start_day.year)

    end_day = start_day + timedelta(days=days)
    if end_day.year != start_day.year:
        holidays_by_date.update(fetch_holidays(country, end_day.year))

    plan: List[DayPlan] = []
    for offset in range(days):
        current_day = start_day + timedelta(days=offset)
        weekday = current_day.strftime("%A")
        is_weekend = current_day.weekday() >= 5

        plan.append(
            DayPlan(
                day=current_day,
                weekday=weekday,
                is_weekend=is_weekend,
                holiday_name=holidays_by_date.get(current_day),
            )
        )
    return plan


def print_plan(plan: List[DayPlan]) -> None:
    """Exibe o planejamento no terminal de forma legível."""
    print("\nPlanejamento automático de calendário\n")
    print("Data       | Dia da semana | Status")
    print("-" * 48)

    for item in plan:
        status = []
        if item.is_weekend:
            status.append("Fim de semana")
        if item.holiday_name:
            status.append(f"Feriado: {item.holiday_name}")
        if not status:
            status.append("Dia útil")

        print(f"{item.day.isoformat()} | {item.weekday:<12} | {' | '.join(status)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera um planejamento dos próximos dias com base em feriados oficiais."
    )
    parser.add_argument(
        "--country",
        default="BR",
        help="Código do país (ISO 3166-1 alpha-2). Ex.: BR, US, PT.",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=14,
        help="Quantidade de dias para planejamento.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.days < 1:
        raise SystemExit("O valor de --days deve ser maior que zero.")

    try:
        plan = build_plan(args.country.upper(), date.today(), args.days)
    except requests.RequestException as exc:
        raise SystemExit(f"Falha ao buscar feriados na API: {exc}") from exc

    print_plan(plan)


if __name__ == "__main__":
    main()
