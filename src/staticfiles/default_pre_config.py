# flake8: noqa
# pylint: skip-file
DEFAULT_PRE_CONFIG = {
    "characteristics": [
        {
            "key": "reliability",
            "weight": 34,
            "subcharacteristics": [
                {
                    "key": "testing_status",
                    "weight": 50,
                    "measures": [
                        {
                            "key": "passed_tests",
                            "weight": 33,
                            "min_threshold": 0,
                            "max_threshold": 1,
                        },
                        {
                            "key": "test_builds",
                            "weight": 33,
                            "min_threshold": 0,
                            "max_threshold": 300000,
                        },
                        {
                            "key": "test_coverage",
                            "weight": 34,
                            "min_threshold": 60,
                            "max_threshold": 100,
                        },
                    ],
                },
                {
                    "key": "maturity",
                    "weight": 50,
                    "measures": [
                        {
                            "key": "ci_feedback_time",
                            "weight": 100,
                            "min_threshold": 1,
                            "max_threshold": 900,
                        }
                    ],
                },
            ],
        },
        {
            "key": "maintainability",
            "weight": 33,
            "subcharacteristics": [
                {
                    "key": "modifiability",
                    "weight": 100,
                    "measures": [
                        {
                            "key": "non_complex_file_density",
                            "weight": 25,
                            "min_threshold": 0,
                            "max_threshold": 10,
                        },
                        {
                            "key": "commented_file_density",
                            "weight": 25,
                            "min_threshold": 10,
                            "max_threshold": 30,
                        },
                        {
                            "key": "duplication_absense",
                            "weight": 25,
                            "min_threshold": 0,
                            "max_threshold": 5,
                        },
                        {
                            "key": "technical_debt_ratio",
                            "weight": 25,
                            "min_threshold": 0,
                            "max_threshold": 20,
                        },
                    ],
                }
            ],
        },
        {
            "key": "functional_suitability",
            "weight": 33,
            "subcharacteristics": [
                {
                    "key": "functional_completeness",
                    "weight": 100,
                    "measures": [
                        {
                            "key": "team_throughput",
                            "weight": 100,
                            "min_threshold": 45,
                            "max_threshold": 100,
                        },
                    ],
                }
            ],
        },
    ]
}

# A caracteristica security NAO entra no DEFAULT_PRE_CONFIG: o padrao do
# produto continua com as 3 caracteristicas de sempre (34/33/33), por
# retrocompatibilidade e por decisao do P.O. registrada na US01.01.
#
# SECURITY_PRE_CONFIG e o template de ativacao da caracteristica, consumido
# pelo Planejamento de Release (Web) e pelo .msgram/msgram.json (CLI). Os
# pesos de subcaracteristicas e de medidas ja fecham 100% em cada nivel. O
# peso 25 da propria caracteristica assume a ativacao junto das 3 padrao
# (4 x 25 = 100); a etapa de planejamento pode rebalancear esse valor desde
# que a soma das caracteristicas selecionadas continue em 100.
SECURITY_PRE_CONFIG = {
    "characteristics": [
        {
            "key": "security",
            "weight": 25,
            "subcharacteristics": [
                {
                    "key": "confidentiality",
                    "weight": 50,
                    "measures": [
                        {
                            "key": "security_rating_measure",
                            "weight": 50,
                            "min_threshold": 1,
                            "max_threshold": 5,
                        },
                        {
                            "key": "absence_of_vulnerabilities",
                            "weight": 50,
                            "min_threshold": 0,
                            "max_threshold": 1,
                        },
                    ],
                },
                {
                    "key": "integrity",
                    "weight": 50,
                    "measures": [
                        {
                            "key": "security_review_rating_measure",
                            "weight": 50,
                            "min_threshold": 1,
                            "max_threshold": 5,
                        },
                        {
                            "key": "security_alerts_resolution",
                            "weight": 50,
                            "min_threshold": 45,
                            "max_threshold": 100,
                        },
                    ],
                },
            ],
        }
    ]
}
