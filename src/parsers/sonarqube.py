import os

import requests

from staticfiles import SONARQUBE_AVAILABLE_METRICS, SONARQUBE_SUPPORTED_MEASURES


class Sonarqube:

    def __init__(self, metrics, dir_path):
        self.endpoint = os.getenv("SONAR_URL", "https://sonarcloud.io/api/metrics/search")
        self.metrics = metrics
        self.dir_path = dir_path

    def import_sonarqube_supported_metrics(self):
        try:
            request = requests.get(self.endpoint)

            if request.ok:
                data = request.json()
            else:
                data = SONARQUBE_AVAILABLE_METRICS
        except Exception:
            data = SONARQUBE_AVAILABLE_METRICS

        with open(dir_path, "w"):
            f.write(self.__extract_supported_metrics(data))

    def __extract_supported_metrics(sonar_metrics):
        supported_metrics = SONARQUBE_SUPPORTED_MEASURES
        collected_metrics = {}

        for component in self.metrics['components']:
            for obj in component['measures']:
                metric_key = obj['metric']

                if metric_key not in supported_metrics:
                    continue

                collected_metrics[metric_key] = float(obj['value'])

        return collected_metrics
