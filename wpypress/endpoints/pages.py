import requests
from wpypress.utils import extract_pagination_headers

class PagesEndpoint:
    def __init__(self, client):
        self.client = client
        self.endpoint = f"{self.client.base_url}/wp-json/wp/v2/pages"

    def list(self, params=None):
        """List pages and pagination metadata"""
        headers = self.client.auth.get_headers() if self.client.auth else {}
        response = requests.get(self.endpoint, headers=headers, params=params)
        response.raise_for_status()

        pagination = extract_pagination_headers(response)
        pagination['page'] = int(params.get('page', 1)) if params else 1
        pagination['per_page'] = int(params.get('per_page', 10)) if params else 10

        return response.json(), pagination

    def get(self, page_id, slug=None):
        """Get a single page by ID"""
        if slug:
            url = f"{self.endpoint}?slug={slug}"
        else:
            url = f"{self.endpoint}/{page_id}"
        headers = self.client.auth.get_headers() if self.client.auth else {}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def create(self, title, content, excerpt=None, status='publish', featured_media=None, **kwargs):
        """Create a new page"""
        data = {
            'title': title,
            'content': content,
            'status': status,
        }
        if excerpt:
            data['excerpt'] = excerpt
        if featured_media:
            data['featured_media'] = featured_media

        data.update(kwargs)

        headers = {'Content-Type': 'application/json'}
        if self.client.auth:
            headers.update(self.client.auth.get_headers())

        response = requests.post(self.endpoint, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def update(self, page_id, **kwargs):
        """Update an existing page"""
        url = f"{self.endpoint}/{page_id}"
        headers = {'Content-Type': 'application/json'}
        if self.client.auth:
            headers.update(self.client.auth.get_headers())

        response = requests.post(url, json=kwargs, headers=headers)
        response.raise_for_status()
        return response.json()

    def delete(self, page_id, force=False):
        """Delete a page. Param force=False trash the page, otherwise will be permanently deleted"""
        url = f"{self.endpoint}/{page_id}"
        params = {'force': 'true' if force else 'false'}
        headers = self.client.auth.get_headers() if self.client.auth else {}
        response = requests.delete(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
