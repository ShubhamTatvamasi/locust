from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task(1)
    def get_index(self):
        self.client.get("/")
