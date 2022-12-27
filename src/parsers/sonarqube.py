import os

import requests

from staticfiles import SONARQUBE_AVAILABLE_METRICS, SONARQUBE_SUPPORTED_MEASURES


class Sonarqube:

    def __init__(self):
        self.endpoint = os.getenv("SONAR_URL", "https://sonarcloud.io/api/metrics/search")

    def import_sonarqube_supported_metrics(self, metrics):
        try:
            request = requests.get(self.endpoint)

            if request.ok:
                data = request.json()
            else:
                data = SONARQUBE_AVAILABLE_METRICS
        except Exception:
            data = SONARQUBE_AVAILABLE_METRICS

        return self.__extract_supported_metrics(data, metrics)

    def __extract_supported_metrics(
        sonar_metrics,
        metrics,
    ):
        # TODO: refatorar dicionário SONARQUBE_SUPPORTED_MEASURES
        supported_metrics = {
            supported_metric.key: supported_metric
            for supported_metric in SONARQUBE_SUPPORTED_MEASURES
        }

        collected_metrics = {}
        for component in data['components']:
            for obj in component['measures']:
                metric_key = obj['metric']

                if metric_key not in supported_metrics:
                    continue

                collected_metrics[metric_key] = float(obj['value'])

        return collected_metrics
