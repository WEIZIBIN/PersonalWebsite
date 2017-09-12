dict_xiaoice = {}


def get_xiaoice_by_username(username):
    return dict_xiaoice[username]


def add_xiaoice(xiaoice):
    dict_xiaoice[xiaoice.username] = xiaoice


def get_all_xiaoice():
    return dict_xiaoice


def get_avail_xiaoice():
    # todo check avail
    for username, xiaoice in dict_xiaoice.items():
        return xiaoice