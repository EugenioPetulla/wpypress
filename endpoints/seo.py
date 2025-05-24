import requests

class SEOEndpoint:
    def __init__(self, client):
        self.client = client
        self.base_url = self.client.base_url
        self.yoast_check_endpoint = f"{self.base_url}/wp-json/yoast/v1/get_head"

    def update(self, post_id, title=None, description=None, canonical=None, robots=None,
               focus_keyword=None, og_title=None, og_description=None, type='post'):
        """
        Update Yoast SEO metadata for a post or page through standard post meta fields.

        :param post_id: ID of the post or page
        :param type: 'post' or 'page' (default: 'post')
        """
        if type not in ['post', 'page']:
            raise ValueError("type must be either 'post' or 'page'")

        endpoint = f"{self.base_url}/wp-json/wp/v2/{type}s/{post_id}"

        headers = {'Content-Type': 'application/json'}
        if self.client.auth:
            headers.update(self.client.auth.get_headers())

        meta_fields = {}

        if title:
            meta_fields['yoast_wpseo_title'] = title
        if description:
            meta_fields['yoast_wpseo_metadesc'] = description
        if canonical:
            meta_fields['yoast_wpseo_canonical'] = canonical
        if robots:
            meta_fields['yoast_wpseo_robots'] = robots
        if focus_keyword:
            meta_fields['yoast_wpseo_focuskw'] = focus_keyword

        if og_title:
            meta_fields['yoast_wpseo_opengraph-title'] = og_title
        if og_description:
            meta_fields['yoast_wpseo_opengraph-description'] = og_description

        data = {'meta': meta_fields}

        response = requests.post(endpoint, headers=headers, json=data)
        if not response.ok:
            raise Exception(f"Failed to update SEO metadata: {response.status_code} {response.text}")

        return response.json()

    def is_yoast(self):
        """
        Checks if the Yoast SEO plugin is active and exposing its REST API.
        Returns True if available, False otherwise.
        """
        headers = self.client.auth.get_headers() if self.client.auth else {}
        params = {'url': f"{self.client.base_url}/"}

        try:
            response = requests.get(self.yoast_check_endpoint, headers=headers, params=params)
            return response.status_code == 200
        except requests.RequestException:
            return False
