import os
import time
import requests
from Core.auth import load_env, get_token


class DataverseBase:
    def __init__(self):
        load_env()
        self.url = os.getenv("DATAVERSE_URL", "").rstrip("/")
        self.solution = os.getenv("SOLUTION_NAME", "")
        self.token = get_token()
        self.language_code = int(os.getenv("LANGUAGE_CODE", "1033"))

        if not self.url:
            raise Exception("DATAVERSE_URL manquant dans le .env")
        if not self.solution:
            raise Exception("SOLUTION_NAME manquant dans le .env")

    def call(self, method, url, payload=None, use_solution_header=True):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "OData-Version": "4.0",
            "OData-MaxVersion": "4.0"
        }

        if use_solution_header and self.solution:
            headers["MSCRM.SolutionUniqueName"] = self.solution

        r = requests.request(method=method, url=url, json=payload, headers=headers)

        print(f"HTTP {r.status_code}")
        if not r.ok:
            try:
                print("ERROR JSON:", r.json())
            except Exception:
                print("ERROR TEXT:", r.text)

        return r

    def label(self, text, lang=None):
        lang_code = lang if lang is not None else self.language_code
        return {
            "@odata.type": "Microsoft.Dynamics.CRM.Label",
            "LocalizedLabels": [
                {
                    "@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel",
                    "Label": text,
                    "LanguageCode": lang_code
                }
            ]
        }

    def exists_table(self, schema_name):
        url = f"{self.url}/api/data/v9.2/EntityDefinitions(LogicalName='{schema_name}')"
        r = self.call("GET", url, use_solution_header=False)
        return r.status_code == 200

    def exists_attribute(self, table, field):
        url = (
            f"{self.url}/api/data/v9.2/"
            f"EntityDefinitions(LogicalName='{table}')"
            f"/Attributes(LogicalName='{field}')"
        )
        r = self.call("GET", url, use_solution_header=False)
        return r.status_code == 200

    def publish_all(self):
        url = f"{self.url}/api/data/v9.2/PublishAllXml"
        return self.call("POST", url, payload={}, use_solution_header=False)

    def wait(self, seconds=1):
        time.sleep(seconds)