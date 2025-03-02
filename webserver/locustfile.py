from locust import HttpUser, task, between
import random

class Workload(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def test_pages(self):
        pages = ["/page1.html", "/page2.html", "/page3.html", "/page4.html", "/page5.html"]
        selected_page = random.choice(pages)
        self.client.get(selected_page)
