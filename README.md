# MeasureSoftGram-Core

## Badges

[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-Core&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-Core)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-Core&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-Core)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-Core&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-Core)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-Core&metric=bugs)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-Core)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-Core&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-Core)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-Core&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-Core)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-Core&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-Core)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-Core&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-Core)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-Core&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-Core)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-Core&metric=coverage)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-Core)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_MeasureSoftGram-Core&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_MeasureSoftGram-Core)

> **Este README resume o componente Core.** A documentação completa do produto — incluindo arquitetura, uso detalhado e políticas de contribuição — é central e vive no [MeasureSoftGram Docs](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/).

## O que é

O **MeasureSoftGram-Core** (pacote `msgram-core`) é o núcleo matemático do MeasureSoftGram: uma biblioteca Python responsável por calcular o modelo de qualidade de software, subindo de métricas extraídas até o índice final de qualidade (TSQMI), passando por medidas, subcaracterísticas e características.

## Como Executar o Projeto

Requisitos: **Python 3.10 ou superior**.

### 1. Criar e ativar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Usar como biblioteca

```python
from resources.analysis import calculate_measures
```

---

## Como Rodar os Testes

```bash
pip install tox
tox
```

Para rodar um pacote ou arquivo específico:

```bash
tox <PACKAGE OR FILE>
```

Se não funcionar, tente instalar antes:

```bash
pip install pytest-mock
```

---

## Documentação

A documentação oficial e completa é central: **[MeasureSoftGram Docs](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/)**. Este repositório guarda apenas o código do componente e um resumo.

## Informações Adicionais

- **Docker Hub:** [Core](https://hub.docker.com/r/measuresoftgram/core) · [Service](https://hub.docker.com/r/measuresoftgram/service)
- **Documentação:** [MeasureSoftGram Docs](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/)
- **Guia de Contribuição:** Veja nosso [Guia de Contribuição](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/docs/como-contribuir) e o arquivo [CONTRIBUTING.md](./CONTRIBUTING.md).
- **Demais repositórios do produto:**
  * [Service](https://github.com/fga-eps-mds/MeasureSoftGram-Service)
  * [CLI](https://github.com/fga-eps-mds/MeasureSoftGram-CLI)
  * [Front Web](https://github.com/fga-eps-mds/MeasureSoftGram-Front)
  * [Action](https://github.com/fga-eps-mds/MeasureSoftGram-Action)
  * [Parser](https://github.com/fga-eps-mds/MeasureSoftGram-Parser)
  * [Docs](https://github.com/fga-eps-mds/MeasureSoftGram-Docs)

## Contribuição

As políticas de contribuição são as mesmas para todos os repositórios do produto e estão em **[Guia de Contribuição e Padrões](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/docs/como-contribuir)**. Consulte também o [CONTRIBUTING.md](./CONTRIBUTING.md) deste repositório.

## Código de Conduta

Este projeto segue o **[Código de Conduta](https://fga-eps-mds.github.io/MeasureSoftGram-Docs/docs/codigo-de-conduta)** do MeasureSoftGram, único para todos os repositórios. Veja também o [code_of_conduct.md](./code_of_conduct.md).

## Licença

Este projeto é distribuído sob a licença [AGPL-3.0](./LICENSE).
