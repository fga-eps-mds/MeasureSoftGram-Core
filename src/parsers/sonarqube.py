from staticfiles import SONARQUBE_AVAILABLE_METRICS, SONARQUBE_SUPPORTED_MEASURES


class Sonarqube:
    def extract_supported_metrics(self, metrics):
        data = SONARQUBE_AVAILABLE_METRICS

        return self.__extract_sonarqube_supported_metrics(metrics, data)

    def __extract_sonarqube_supported_metrics(self, metrics, sonar_metrics):
        collected_metrics = {}
        supported_metrics = []

        # NOTE: list comprehension que preenche o supported_metrics apenas
        #       com os valores das "metrics" do dicionário de SUPPORTEDs
        [
            supported_metrics.extend(list(x.values())[0]["metrics"])
            for x in SONARQUBE_SUPPORTED_MEASURES
        ]

        for component in metrics:
            qualifier = component["qualifier"]
            path = component["path" if qualifier != "TRK" else "name"]
            collected_metrics[path] = {"qualifier": qualifier, "measures": []}

            for obj in component["measures"]:
                metric_key = obj["metric"]
                if metric_key not in supported_metrics:
                    continue

                collected_metrics[path]["measures"].append(
                    {"metric": metric_key, "value": float(obj["value"])}
                )

        return collected_metrics
