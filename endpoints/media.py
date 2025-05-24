import os
import requests
from wp_api.utils import extract_pagination_headers

class MediaEndpoint:
    def __init__(self, client):
        self.client = client
        self.endpoint = f"{self.client.base_url}/wp-json/wp/v2/media"

    def list(self, params=None):
        """List media items and pagination metadata"""
        headers = self.client.auth.get_headers() if self.client.auth else {}
        response = requests.get(self.endpoint, headers=headers, params=params)
        response.raise_for_status()

        pagination = extract_pagination_headers(response)
        pagination['page'] = int(params.get('page', 1)) if params else 1
        pagination['per_page'] = int(params.get('per_page', 10)) if params else 10

        return response.json(), pagination

    def get(self, media_id):
        """Get a single media item by ID"""
        url = f"{self.endpoint}/{media_id}"
        headers = self.client.auth.get_headers() if self.client.auth else {}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def upload(self, file_path, title=None, alt_text=None, description=None):
        """Upload a media file (image, PDF, etc.)"""
        filename = os.path.basename(file_path)
        mime_type = self._guess_mime_type(filename)

        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Type': mime_type,
        }
        if self.client.auth:
            headers.update(self.client.auth.get_headers())

        with open(file_path, 'rb') as file_data:
            response = requests.post(self.endpoint, headers=headers, data=file_data)
            response.raise_for_status()
            media = response.json()

        # Optionally update title, alt_text, description
        if title or alt_text or description:
            update_data = {}
            if title:
                update_data['title'] = title
            if alt_text:
                update_data['alt_text'] = alt_text
            if description:
                update_data['description'] = description

            headers = {'Content-Type': 'application/json'}
            if self.client.auth:
                headers.update(self.client.auth.get_headers())

            update_url = f"{self.endpoint}/{media['id']}"
            update_response = requests.post(update_url, json=update_data, headers=headers)
            update_response.raise_for_status()
            return update_response.json()

        return media

    def delete(self, media_id):
        """Permanently delete a media item"""
        url = f"{self.endpoint}/{media_id}"
        params = {'force': 'true'}
        headers = self.client.auth.get_headers() if self.client.auth else {}
        response = requests.delete(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def _guess_mime_type(self, filename):
        ext = filename.lower().split('.')[-1]
        return {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'pdf': 'application/pdf',
        }.get(ext, 'application/octet-stream')
