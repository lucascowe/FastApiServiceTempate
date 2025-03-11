import os.path
import unittest
import requests

from app.models.settings import Settings


print(f"Starting tests on .env {os.path.isfile('.env')}")
if os.path.isfile('.env') is False:
    print(f"Current folder {os.curdir}: {os.listdir(os.curdir)}")
settings = Settings()
print(f"Service name: {settings.server_name}")


class MyTestCase(unittest.TestCase):
    def test_version(self):
        response = requests.get(f"http://localhost:{settings.external_port}/server/version")
        print(response.json())
        self.assertEqual(200, response.status_code)
        response_json = response.json()
        self.assertEqual(settings.server_name, response_json.get("name"))
        self.assertEqual(settings.version, response_json.get("version"))

    def test_status(self):
        response = requests.get(f"http://localhost:{settings.external_port}/server/status")
        print(response.json())
        self.assertEqual(200, response.status_code)
        response_json = response.json()
        self.assertEqual(settings.server_name, response_json.get("name"))
        self.assertEqual(settings.version, response_json.get("version"))
        for service in settings.databases:
            self.assertTrue(service in response_json.get('services', {}))


if __name__ == '__main__':
    input(f"Service name: {settings.server_name}")
    unittest.main()
