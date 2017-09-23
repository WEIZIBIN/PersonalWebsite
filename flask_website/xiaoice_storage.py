import uuid
from flask_website.config import xiaoice_timeout

work_xiaoice = {}
free_xiaoice = {}


class Xiaoice():
    def __init__(self, weibo):
        self._weibo = weibo

    def get_weibo(self):
        return self._weibo

    def send_msg(self, msg):
        self._weibo.post_msg_to_xiaoice(msg)

    def get_msg(self):
        return self._weibo.get_msg_from_xiaoice(xiaoice_timeout)

    def is_avail(self):
        if self._weibo.im_ready:
            return True


def get_xiaoice_by_client_id(client_id):
    if client_id:
        return work_xiaoice[client_id]


def add_xiaoice(weibo):
    xiaoice = Xiaoice(weibo)
    free_xiaoice[weibo.username] = xiaoice


def get_free_xiaoice():
    return free_xiaoice


def get_work_xiaoice():
    return work_xiaoice


def get_avail_xiaoice_client_id():
    for username, xiaoice in free_xiaoice.items():
        if xiaoice.is_avail():
            client_id = str(uuid.uuid3(uuid.NAMESPACE_OID, username))
            work_xiaoice[client_id] = free_xiaoice.pop(username)
            return client_id


def free_xiaoice_by_client_id(client_id):
    if work_xiaoice[client_id] is not None:
        xiaoice = work_xiaoice.pop(client_id)
        free_xiaoice[xiaoice.get_weibo().username] = xiaoice
