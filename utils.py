def extract_pagination_headers(response):
    return {
        'total': int(response.headers.get('X-WP-Total', 0)),
        'total_pages': int(response.headers.get('X-WP-TotalPages', 0)),
    }