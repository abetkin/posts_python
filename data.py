

from util import asobj

class blog:
    parent = None
    id = 1
    title = 'Blog'
    text = 'Any posts are welcome'
    tags = ['root', 'moderated']
    comments = []

class post:
    id = 2
    parent = 1
    text = 'Let there be text'
    tags = ['misc']

posts = [blog, post]


def get_user():
    class me:
        name = 'vitalik',
        email = 'abvit89@gmail.com'
    return me

def get_comments_for(post_id):
    return (p for p in posts if p.parent == post_id)

def get_post(post_id):
    return next(p for p in posts if p.id == post_id)

def create_post(**data):
    data = asobj(data)
    posts.append(data)
    return get_post(data.parent)