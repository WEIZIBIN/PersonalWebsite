dict_xiaoice = {}


class Xiaoice():
    def __init__(self, weibo):
        self._weibo = weibo
        self.client_id = None

    def get_weibo(self):
        return self._weibo

    def send_msg(self, msg):
        self._weibo.post_msg_to_xiaoice(msg)

    def get_msg(self):
        return self._weibo.get_msg_from_xiaoice()

    def is_avail(self):
        if self._weibo.im_ready:
            return True


def get_xiaoice_by_username(username):
    return dict_xiaoice[username]


def add_xiaoice(weibo):
    xiaoice = Xiaoice(weibo)
    dict_xiaoice[xiaoice.get_weibo().username] = xiaoice


def get_all_xiaoice():
    return dict_xiaoice


def get_avail_xiaoice():
    for username, xiaoice in dict_xiaoice.items():
        if xiaoice.is_avail():
            return xiaoice
