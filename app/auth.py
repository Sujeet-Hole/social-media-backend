from locust import HttpUser, task

class SocialMediaUser(HttpUser):

    @task(5)
    def get_feed(self):
        self.client.get("/feed")

    @task(3)
    def get_posts(self):
        self.client.get("/posts")

    @task(1)
    def create_post(self):
        self.client.post(
            "/posts",
            json={
                "content": "Locust testing"
            }
        )