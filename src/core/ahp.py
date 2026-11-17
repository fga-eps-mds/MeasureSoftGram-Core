"""Pesos do modelo de qualidade por comparação par a par (AHP).

O cálculo AHP (matriz recíproca, autovetor e razão de consistência) é feito
pela biblioteca AHPy. Este módulo só:

- define a escala de Saaty usada nas perguntas;
- converte as respostas do usuário nas comparações esperadas pela AHPy;
- converte as prioridades em pesos inteiros de 0 a 100 que somam 100.
"""

from dataclasses import dataclass
from itertools import combinations
from math import floor
from typing import Dict, List, Optional, Sequence, Tuple

import ahpy

# Escala fundamental de Saaty, só com os valores ímpares (D2).
SAATY_SCALE: Dict[str, int] = {
    "igual": 1,
    "moderadamente": 3,
    "fortemente": 5,
    "muito_fortemente": 7,
    "extremamente": 9,
}

SAATY_PHRASES: Dict[str, str] = {
    "igual": "igualmente importante",
    "moderadamente": "moderadamente mais importante",
    "fortemente": "fortemente mais importante",
    "muito_fortemente": "muito fortemente mais importante",
    "extremamente": "extremamente mais importante",
}

# Limite da razão de consistência definido por Saaty (D5).
CR_THRESHOLD = 0.10
_REMAINDER_DECIMALS = 6
Answer = Tuple[str, str, Optional[str], str]


@dataclass(frozen=True)
class GroupResult:
    priorities: Dict[str, float]
    weights: Dict[str, int]
    consistency_ratio: Optional[float]

    @property
    def consistent(self) -> bool:
        return self.consistency_ratio is None or self.consistency_ratio <= CR_THRESHOLD


def pairs(entities: Sequence[str]) -> List[Tuple[str, str]]:
    """Pares a comparar, na ordem em que as entidades aparecem no grupo."""
    return list(combinations(entities, 2))


def answer_to_comparison(
    a: str, b: str, preferred: Optional[str], intensity: str
) -> Tuple[Tuple[str, str], int]:
    """Converte uma resposta na comparação da AHPy: ((x, y), v) = "x é v vezes mais importante que y"."""
    if intensity not in SAATY_SCALE:
        raise ValueError(f"Intensidade desconhecida: {intensity!r}")

    if preferred is None:
        if intensity != "igual":
            raise ValueError("Sem entidade preferida, a intensidade deve ser 'igual'")
        return (a, b), 1

    if intensity == "igual":
        raise ValueError(
            "Com uma entidade preferida, a intensidade não pode ser 'igual'"
        )
    if preferred == a:
        return (a, b), SAATY_SCALE[intensity]
    if preferred == b:
        return (b, a), SAATY_SCALE[intensity]
    raise ValueError(f"{preferred!r} não faz parte da comparação {a} × {b}")


def priorities_to_weights(priorities: Dict[str, float]) -> Dict[str, int]:
    """Prioridades (somam 1) -> inteiros de 0 a 100 somando 100, pelo maior resto.

    Em empate de resto, a unidade extra vai para a entidade que aparece primeiro.
    A ordem do dicionário de entrada é preservada.
    """
    keys = list(priorities)
    total = sum(priorities.values())
    scaled = [round(priorities[k] * 100 / total, _REMAINDER_DECIMALS) for k in keys]
    weights = [floor(s) for s in scaled]

    missing = 100 - sum(weights)
    by_remainder = sorted(
        range(len(keys)), key=lambda i: (-(scaled[i] - weights[i]), i)
    )
    for i in by_remainder[:missing]:
        weights[i] += 1

    return {k: int(w) for k, w in zip(keys, weights)}


def calculate_group(entities: Sequence[str], answers: Sequence[Answer]) -> GroupResult:
    """Calcula prioridades, pesos e CR de um grupo a partir das respostas."""
    entities = list(entities)
    if not entities:
        raise ValueError("O grupo não tem entidades")

    if len(entities) == 1:
        return GroupResult({entities[0]: 1.0}, {entities[0]: 100}, None)

    expected = set(pairs(entities))
    comparisons = {}
    answered = set()
    for a, b, preferred, intensity in answers:
        pair = (a, b) if (a, b) in expected else (b, a)
        if pair not in expected:
            raise ValueError(f"Comparação fora do grupo: {a} × {b}")
        answered.add(pair)
        key, value = answer_to_comparison(a, b, preferred, intensity)
        comparisons[key] = value

    if answered != expected:
        faltando = ", ".join(
            f"{a} × {b}" for a, b in pairs(entities) if (a, b) not in answered
        )
        raise ValueError(f"Faltam comparações: {faltando}")

    compare = ahpy.Compare("grupo", comparisons, precision=8, random_index="saaty")

    # A AHPy devolve as prioridades ordenadas pelo peso; voltamos para a ordem do grupo.
    priorities = {e: float(compare.target_weights[e]) for e in entities}
    cr = float(compare.consistency_ratio) if len(entities) >= 3 else None

    return GroupResult(priorities, priorities_to_weights(priorities), cr)
