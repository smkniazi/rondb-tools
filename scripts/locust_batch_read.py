import random
import json
from locust import HttpUser, task, between, events

class BatchReadUser(HttpUser):

    table_size = 1000
    batch_size = 128

    @events.init_command_line_parser.add_listener
    def _(parser):
        parser.add_argument("--table-size", type=int, default=100000, help="Set table size")
        parser.add_argument("--batch-size", type=int, default=100, help="Set batch size")
        parser.add_argument("--database-name", type=str, default="benchmark", help="Set database name")
        parser.add_argument("--disable-batch-read", action="store_true", help="Disable batch_read test")
        parser.add_argument("--disable-complex-type-read", action="store_true", help="Disable complex_type_read test")

    @events.test_start.add_listener
    def _(environment, **kwargs):
        BatchReadUser.table_size = environment.parsed_options.table_size
        BatchReadUser.db_name = environment.parsed_options.database_name
        BatchReadUser.batch_size = environment.parsed_options.batch_size
        BatchReadUser.disable_batch_read = environment.parsed_options.disable_batch_read
        BatchReadUser.disable_complex_type_read = environment.parsed_options.disable_complex_type_read
        print(f"Starting Locust with table_size={BatchReadUser.table_size}, batch_size={BatchReadUser.batch_size}")
        print(f"Tests - batch_read: {'disabled' if BatchReadUser.disable_batch_read else 'enabled'}, complex_type_read: {'disabled' if BatchReadUser.disable_complex_type_read else 'enabled'}")

    @task
    def batch_read(self):
        if BatchReadUser.disable_batch_read:
            return

        entries = []
        for _ in range(self.batch_size):
            id1 = random.randint(1, self.table_size)
            entries.append({
                "id1": id1
            })

        payload = {
            "featureStoreName": "fsdb002",
            "featureViewName": "sample_2",
            "featureViewVersion": 1,
            "passedFeatures": [],
            "entries": entries,
            "metadataOptions": None,
            "options": None
        }
        headers = {"Content-Type": "application/json"}

        self.client.post("/0.1.0/batch_feature_store",
                        data=json.dumps(payload),
                        headers=headers,
                        name=f"Batch Read (batch_size={self.batch_size})")

    @task
    def complex_type_read(self):
        if BatchReadUser.disable_complex_type_read:
            return

        id_value = str(random.randint(1, self.table_size))

        payload = {
            "featureStoreName": "fsdb002",
            "featureViewName": "sample_complex_type_512",
            "featureViewVersion": 1,
            "passedFeatures": {},
            "entries": {
                "id": id_value
            },
            "metadataOptions": {
                "featureName": True,
                "featureType": True
            },
            "options": None
        }
        headers = {"Content-Type": "application/json"}

        self.client.post("/0.1.0/feature_store",
                        data=json.dumps(payload),
                        headers=headers,
                        name="Complex Type Read (single entry)")
