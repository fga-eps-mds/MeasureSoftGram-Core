import ahpy
import pytest

from core.ahp import (
    CR_THRESHOLD,
    SAATY_PHRASES,
    SAATY_SCALE,
    answer_to_comparison,
    calculate_group,
    pairs,
    priorities_to_weights,
)

# ---------------------------------------------------------------- escala (D2)


def test_escala_de_saaty_tem_os_cinco_valores_impares():
    assert SAATY_SCALE == {
        "igual": 1,
        "moderadamente": 3,
        "fortemente": 5,
        "muito_fortemente": 7,
        "extremamente": 9,
    }


def test_cada_valor_da_escala_tem_uma_frase():
    assert set(SAATY_PHRASES) == set(SAATY_SCALE)
    assert SAATY_PHRASES["igual"] == "igualmente importante"
    assert SAATY_PHRASES["muito_fortemente"] == "muito fortemente mais importante"


def test_limite_de_consistencia_de_saaty():
    assert CR_THRESHOLD == 0.10


# ---------------------------------------------------------------- pares


def test_pares_seguem_a_ordem_do_grupo():
    assert pairs(["passed_tests", "test_builds", "test_coverage"]) == [
        ("passed_tests", "test_builds"),
        ("passed_tests", "test_coverage"),
        ("test_builds", "test_coverage"),
    ]


def test_grupo_de_quatro_entidades_tem_seis_pares():
    assert len(pairs(["a", "b", "c", "d"])) == 6


def test_grupo_de_uma_entidade_nao_tem_pares():
    assert pairs(["ci_feedback_time"]) == []


# ---------------------------------------------------------------- resposta -> AHPy


def test_resposta_igual_vira_valor_1():
    assert answer_to_comparison("a", "b", None, "igual") == (("a", "b"), 1)


def test_quando_a_primeira_e_preferida_a_chave_mantem_a_ordem():
    assert answer_to_comparison("a", "b", "a", "fortemente") == (("a", "b"), 5)


def test_quando_a_segunda_e_preferida_a_chave_inverte():
    assert answer_to_comparison("a", "b", "b", "fortemente") == (("b", "a"), 5)


@pytest.mark.parametrize(
    "preferred,intensity",
    [("c", "fortemente"), ("a", "pouco"), ("a", "igual"), (None, "fortemente")],
)
def test_resposta_invalida_gera_erro(preferred, intensity):
    with pytest.raises(ValueError):
        answer_to_comparison("a", "b", preferred, intensity)


# ---------------------------------------------------------------- pesos inteiros (D4)


@pytest.mark.parametrize(
    "priorities,expected",
    [
        ({"A": 0.875, "B": 0.125}, {"A": 88, "B": 12}),
        ({"A": 0.83333333, "B": 0.16666667}, {"A": 83, "B": 17}),
        # empate de resto: a unidade extra vai para a primeira entidade (34/33/33)
        (
            {"A": 0.33333333, "B": 0.33333333, "C": 0.33333333},
            {"A": 34, "B": 33, "C": 33},
        ),
        # ordem do grupo, não ordem do peso
        (
            {
                "passed_tests": 0.649118,
                "test_builds": 0.07192743,
                "test_coverage": 0.27895457,
            },
            {"passed_tests": 65, "test_builds": 7, "test_coverage": 28},
        ),
    ],
)
def test_prioridades_viram_inteiros_pelo_maior_resto(priorities, expected):
    weights = priorities_to_weights(priorities)
    assert weights == expected
    assert list(weights) == list(expected)  # preserva a ordem do grupo
    assert sum(weights.values()) == 100


def test_empate_de_resto_com_ruido_de_ponto_flutuante():
    # 87,5 / 12,5 pode chegar como 87,4999999...; a unidade extra continua indo para A
    assert priorities_to_weights({"A": 0.87499999999, "B": 0.12500000001}) == {
        "A": 88,
        "B": 12,
    }


def test_pesos_sao_int_do_python():
    weights = priorities_to_weights({"A": 0.5, "B": 0.5})
    assert all(type(w) is int for w in weights.values())


# ---------------------------------------------------------------- Cenário 2


@pytest.mark.parametrize(
    "intensity,peso_a,peso_b",
    [
        ("igual", 50, 50),
        ("moderadamente", 75, 25),
        ("fortemente", 83, 17),
        ("muito_fortemente", 88, 12),
        ("extremamente", 90, 10),
    ],
)
def test_cenario_2_frase_e_pesos(intensity, peso_a, peso_b):
    preferred = None if intensity == "igual" else "A"
    result = calculate_group(["A", "B"], [("A", "B", preferred, intensity)])
    assert result.weights == {"A": peso_a, "B": peso_b}
    assert result.consistency_ratio is None  # 2 entidades: não se aplica


# ---------------------------------------------------------------- vetores da US (seção 4)


def test_grupo_caracteristicas():
    result = calculate_group(
        ["reliability", "maintainability", "functional_suitability"],
        [
            ("reliability", "maintainability", None, "igual"),
            ("reliability", "functional_suitability", "reliability", "moderadamente"),
            (
                "maintainability",
                "functional_suitability",
                "maintainability",
                "moderadamente",
            ),
        ],
    )
    assert result.priorities == pytest.approx(
        {
            "reliability": 0.4286,
            "maintainability": 0.4286,
            "functional_suitability": 0.1429,
        },
        abs=1e-4,
    )
    assert result.weights == {
        "reliability": 43,
        "maintainability": 43,
        "functional_suitability": 14,
    }
    assert result.consistency_ratio == pytest.approx(0.0, abs=1e-6)
    assert result.consistent


def test_grupo_testing_status():
    result = calculate_group(
        ["passed_tests", "test_builds", "test_coverage"],
        [
            ("passed_tests", "test_builds", "passed_tests", "muito_fortemente"),
            ("passed_tests", "test_coverage", "passed_tests", "moderadamente"),
            ("test_builds", "test_coverage", "test_coverage", "fortemente"),
        ],
    )
    assert list(result.weights) == ["passed_tests", "test_builds", "test_coverage"]
    assert result.weights == {"passed_tests": 65, "test_builds": 7, "test_coverage": 28}
    assert result.consistency_ratio == pytest.approx(0.0624, abs=1e-4)
    assert result.consistent


def test_grupo_circular_e_inconsistente():
    result = calculate_group(
        ["A", "B", "C"],
        [
            ("A", "B", "A", "muito_fortemente"),
            ("A", "C", "C", "muito_fortemente"),
            ("B", "C", "B", "muito_fortemente"),
        ],
    )
    assert result.weights == {"A": 34, "B": 33, "C": 33}
    assert result.consistency_ratio == pytest.approx(4.9451, abs=1e-4)
    assert not result.consistent


def test_saida_bate_com_a_chamada_direta_a_ahpy():
    comparacoes = {
        ("passed_tests", "test_builds"): 7,
        ("passed_tests", "test_coverage"): 3,
        ("test_coverage", "test_builds"): 5,
    }
    direto = ahpy.Compare("x", comparacoes, precision=8, random_index="saaty")
    result = calculate_group(
        ["passed_tests", "test_builds", "test_coverage"],
        [
            ("passed_tests", "test_builds", "passed_tests", "muito_fortemente"),
            ("passed_tests", "test_coverage", "passed_tests", "moderadamente"),
            ("test_builds", "test_coverage", "test_coverage", "fortemente"),
        ],
    )
    assert result.priorities == pytest.approx(dict(direto.target_weights))
    assert result.consistency_ratio == pytest.approx(direto.consistency_ratio)


# ---------------------------------------------------------------- Cenário 3 e erros


def test_cenario_3_grupo_com_uma_entidade():
    result = calculate_group(["ci_feedback_time"], [])
    assert result.weights == {"ci_feedback_time": 100}
    assert result.consistency_ratio is None
    assert result.consistent


def test_resposta_faltando_gera_erro():
    with pytest.raises(ValueError):
        calculate_group(["A", "B", "C"], [("A", "B", None, "igual")])


def test_entidade_desconhecida_gera_erro():
    with pytest.raises(ValueError):
        calculate_group(["A", "B"], [("A", "X", None, "igual")])


def test_grupo_vazio_gera_erro():
    with pytest.raises(ValueError):
        calculate_group([], [])
