import base64

class BasicAuth:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_headers(self):
        token = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
        return {
            "Authorization": f"Basic {token}"
        }