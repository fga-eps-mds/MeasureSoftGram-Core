import os

import requests

from src.cli.staticfiles import SONARQUBE_AVAILABLE_METRICS, SONARQUBE_SUPPORTED_MEASURES 


class Sonarqube:

    def __init__(self):
        self.endpoint = os.getenv("SONAR_URL", "https://sonarcloud.io/api/metrics/search")

    def extract_supported_metrics(self, metrics):
        try:
            request = requests.get(self.endpoint)

            if request.ok:
                data = request.json()
            else:
                data = SONARQUBE_AVAILABLE_METRICS
        except Exception:
            data = SONARQUBE_AVAILABLE_METRICS

        return self.__extract_sonarqube_supported_metrics(metrics, data)

    def __extract_sonarqube_supported_metrics(self, metrics, sonar_metrics):
        collected_metrics = {}
        supported_metrics = []

        [
            supported_metrics.extend(list(x.values())[0]['metrics'])
            for x in SONARQUBE_SUPPORTED_MEASURES
        ]

        for component in metrics:
            for obj in component['measures']:
                metric_key = obj['metric']

                if metric_key not in supported_metrics:
                    continue

                collected_metrics[metric_key] = float(obj['value'])

        return collected_metrics
