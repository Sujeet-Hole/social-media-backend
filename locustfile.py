from locust import HttpUser, task, between


class SocialMediaUser(HttpUser):

    wait_time = between(1, 3)

    @task(5)
    def get_posts(self):
        self.client.get("/posts/1")

    @task(4)
    def get_feed(self):
        self.client.get("/feed/?user_id=1")

    @task(2)
    def get_followers(self):
        self.client.get("/follow/1")

    @task(2)
    def get_user(self):
        self.client.get("/auth/users/1")