from rt_base import *

def update_object_tags(taglist=[]):
    response = get_data(method='update_object_tags', params=taglist)
