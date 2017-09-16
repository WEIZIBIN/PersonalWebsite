import uuid

work_xiaoice={}
free_xiaoice={}

UUID_NAMESPACE_XIAOICE = 'CHAT_XIAOICE'

class Xiaoice():
    def __init__(self, weibo):
        self._weibo = weibo

    def get_weibo(self):
        return self._weibo

    def send_msg(self, msg):
        self._weibo.post_msg_to_xiaoice(msg)

    def get_msg(self):
        return self._weibo.get_msg_from_xiaoice()

    def is_avail(self):
        if self._weibo.im_ready:
            return True


def get_xiaoice_by_client_id(client_id):
    if client_id:
        return work_xiaoice[client_id]


def add_xiaoice(weibo):
    xiaoice = Xiaoice(weibo)
    free_xiaoice[weibo.username] = xiaoice


def get_all_xiaoice():
    return free_xiaoice


def get_avail_xiaoice_client_id():
    for username, xiaoice in free_xiaoice.items():
        if xiaoice.is_avail():
            client_id = uuid.uuid3(UUID_NAMESPACE_XIAOICE, username)
            work_xiaoice[client_id] = free_xiaoice.pop(username)
            return client_id.__str__()