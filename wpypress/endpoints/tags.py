import requests
from wpypress.utils import extract_pagination_headers


class TagsEndpoint:
    def __init__(self, client):
        self.client = client
        self.endpoint = f"{self.client.base_url}/wp-json/wp/v2/tags"

    def list(self, params=None):
        """List all tags (with optional filters) and pagination metadata"""
        headers = self.client.auth.get_headers() if self.client.auth else {}
        response = requests.get(self.endpoint, headers=headers, params=params)
        response.raise_for_status()

        pagination = pagination = extract_pagination_headers(response)
        pagination['page'] = int(params.get('page', 1)) if params else 1
        pagination['per_page'] = int(params.get('per_page', 10)) if params else 10

        return response.json(), pagination

    def get(self, tag_id):
        """Get a tag by ID"""
        url = f"{self.endpoint}/{tag_id}"
        headers = self.client.auth.get_headers() if self.client.auth else {}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def create(self, name, slug=None, description=None, **kwargs):
        """Create a new tag"""
        data = {'name': name}
        if slug:
            data['slug'] = slug
        if description:
            data['description'] = description
        data.update(kwargs)

        headers = {'Content-Type': 'application/json'}
        if self.client.auth:
            headers.update(self.client.auth.get_headers())

        response = requests.post(self.endpoint, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def update(self, tag_id, **kwargs):
        """Update an existing tag"""
        url = f"{self.endpoint}/{tag_id}"
        headers = {'Content-Type': 'application/json'}
        if self.client.auth:
            headers.update(self.client.auth.get_headers())

        response = requests.post(url, json=kwargs, headers=headers)
        response.raise_for_status()
        return response.json()

    def delete(self, tag_id):
        """Permanently delete a tag"""
        url = f"{self.endpoint}/{tag_id}"
        params = {'force': 'true'}
        headers = self.client.auth.get_headers() if self.client.auth else {}
        response = requests.delete(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
