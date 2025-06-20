import requests
from wpypress.utils import extract_pagination_headers

class PostsEndpoint:
    def __init__(self, client):
        self.client = client
        self.endpoint = f"{self.client.base_url}/wp-json/wp/v2/posts"

    def list(self, params=None):
        """List posts with optional filters and pagination metadata"""
        headers = self.client.auth.get_headers() if self.client.auth else {}
        response = requests.get(self.endpoint, headers=headers, params=params)
        response.raise_for_status()

        pagination = pagination = extract_pagination_headers(response)
        pagination['page'] = int(params.get('page', 1)) if params else 1
        pagination['per_page'] = int(params.get('per_page', 10)) if params else 10

        return response.json(), pagination

    def get(self, post_id=None, slug=None):
        """Get a single post by ID or slug"""
        if slug:
            url = f"{self.endpoint}?slug={slug}"
        else:
            url = f"{self.endpoint}/{post_id}"
        headers = self.client.auth.get_headers() if self.client.auth else {}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def create(self, title, content, status='publish', categories=None, tags=None, featured_media=None, excerpt=None, **kwargs):
        """Create a new post"""
        data = {
            'title': title,
            'content': content,
            'status': status,
        }
        if excerpt:
            data['excerpt'] = excerpt
        if categories:
            data['categories'] = categories  # List of category IDs
        if tags:
            data['tags'] = tags              # List of tag IDs
        if featured_media:
            data['featured_media'] = featured_media  # Media ID

        data.update(kwargs)
        headers = {
            'Content-Type': 'application/json'
        }
        if self.client.auth:
            headers.update(self.client.auth.get_headers())

        response = requests.post(self.endpoint, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def update(self, post_id, **kwargs):
        """Update an existing post"""
        url = f"{self.endpoint}/{post_id}"
        headers = {
            'Content-Type': 'application/json'
        }
        if self.client.auth:
            headers.update(self.client.auth.get_headers())

        response = requests.post(url, json=kwargs, headers=headers)
        response.raise_for_status()
        return response.json()

    def delete(self, post_id, force=False):
        """Delete a post"""
        url = f"{self.endpoint}/{post_id}"
        headers = self.client.auth.get_headers() if self.client.auth else {}
        params = {'force': 'true' if force else 'false'}
        response = requests.delete(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
