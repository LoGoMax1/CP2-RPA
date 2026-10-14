# CP2-RPA

## Automação de Calendário (Python)

Este projeto implementa uma automação em Python para organizar os próximos dias do calendário,
identificando dias úteis, fins de semana e feriados públicos por meio de integração REST com a API pública **Nager.Date**.

### Requisitos

- Python 3.10+
- Dependências em `requirements.txt`

### Instalação

```bash
pip install -r requirements.txt
```

### Execução

```bash
python calendar_automation.py --country BR --days 14
```

Parâmetros:

- `--country`: código do país (ISO 3166-1 alpha-2), padrão `BR`
- `--days`: quantidade de dias no planejamento, padrão `14`

### Integração Externa

A automação consome a API REST:

`https://date.nager.at/api/v3/PublicHolidays/{ano}/{pais}`
