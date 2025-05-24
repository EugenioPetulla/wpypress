# wpypress

`wpypress` is a Python library designed for interacting with the WordPress REST API. It simplifies the process of managing posts, pages, media, categories, tags, and SEO settings on WordPress sites.

## Features

- **Post Management**: Create, update, delete, and list posts.
- **Page Management**: Create, update, delete, and list pages.
- **Media Management**: Upload, update, delete, and list media items.
- **Category & Tag Management**: Create, update, delete, and list categories and tags.
- **SEO Management**: Manage SEO settings using the Yoast SEO plugin.

## Installation

To install `wpypress`, simply use pip:

```bash
pip install wpypress
```

## Usage

### Initialization

To start using the library, first, initialize the `WPClient` with your WordPress site credentials:

```python
from wpypress import WPClient

wp = WPClient(
    base_url="https://your-wordpress-site.com",
    username="admin",
    password="your-password"
)
```

### Posts

#### Fetch Posts

Retrieve the first page of posts:

```python
posts, pagination = wp.posts.list(params={'per_page': 10, 'page': 1})
print(f"Total posts: {pagination['total']}")
print(f"Total pages: {pagination['total_pages']}")
print(f"Current page: {pagination['page']}\n")
```

#### Create a Post

Create a new post with categories and tags:

```python
post = wp.posts.create(
    title="My New Post",
    content="This is the content.",
    status="publish",
    categories=[2],
    tags=[5, 6],
    featured_media=15
)
```

#### Delete a Post

To delete a post, use:

```python
wp.posts.delete(123, force=True)
```

### Pages

#### Create a New Page

To create a new page:

```python
page = wp.pages.create(
    title="About Us",
    content="This is our about page.",
    excerpt="About page",
    status="publish"
)
```

### Media

#### Upload an Image

To upload a media item, execute:

```python
media = wp.media.upload(
    file_path='./images/photo.jpg',
    title='My Photo',
    alt_text='A beautiful photo',
    description='Uploaded via REST APIs'
)
```

### Categories

#### Create a Category

```python
new_category = wp.categories.create(
    name="Tech News",
    slug="tech-news",
    description="Technology related articles"
)
```

### Tags

#### Create a Tag

```python
new_tag = wp.tags.create(
    name="Python",
    slug="python",
    description="All posts about Python"
)
```

### SEO

#### Update Post SEO (Yoast SEO)

Ensure your site has the Yoast SEO plugin activated to manage SEO settings easily:

```python
if wp.seo.is_yoast():
    wp.seo.update(
        post_id=456,
        title="Page SEO Title",
        description="Meta description for the page.",
        og_title="OpenGraph Title for Page",
        og_description="OpenGraph Description for Page",
        type="page"
    )
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
