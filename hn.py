import requests
import json

TOP_STORIES_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json'
STORY_URL_TEMPLATE = 'https://hacker-news.firebaseio.com/v0/item/%s.json'


def get_top_ids(num=None):
    '''Returns the current top `num` story IDs.'''
    http_response = requests.get(TOP_STORIES_URL)
    if http_response.status_code != 200:
        raise Exception("HTTP %s: %s" % (http_response.status_code, http_response.content))
    response_json = json.loads(http_response.content)
    if num is None:
        return response_json
    else:
        return response_json[:num]


def get_top_stories(num=None):
    '''Returns the current top `num` stories.

    @returns: list of dict containing story content, of the following format:
        {u'by': u'some_username', -- the user who posted this story
        u'id': 9058826, -- the id of this post
        u'kids': [123, 456], -- the child posts of this post
        u'score': 128, -- the upvote score of this post
        u'text': u'', -- the post content
        u'time': 1424118730, -- UNIX timestamp at which this story was posted
        u'title': u'Routing on OpenStreetMap.org', -- post title
        u'type': u'story', -- type of post
        u'url': u'https://blog.openstreetmap.org/2015/02/16/routing-on-openstreetmap-org/' -- source URL
    '''
    story_ids = get_top_ids(num=num)
    stories = []
    for story_id in story_ids:
        http_response = requests.get(STORY_URL_TEMPLATE % story_id)
        if http_response.status_code != 200:
            raise Exception("HTTP %s: %s" % (http_response.status_code, http_response.content))
        content = json.loads(http_response.content)
        stories.append(content)
    return stories
