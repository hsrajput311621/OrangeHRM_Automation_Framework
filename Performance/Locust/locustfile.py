from locust import HttpUser, task, between

class OrangeHRMUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def login(self):
        self.client.post("/web/index.php/auth/validate", {
            "username": "Admin",
            "password": "admin123"
        })

    @task
    def dashboard(self):
        self.client.get("/web/index.php/dashboard/index")