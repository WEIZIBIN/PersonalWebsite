import base64
import binascii
import json
import logging
import queue
import re
from threading import Thread
import time
import urllib.parse
import requests
import rsa

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}
logger = logging.getLogger('weibo')
xiaoice_uid = 5175429989
polling_wait_second = 0


class Weibo():
    def __init__(self, username, password):
        self.s = requests.session()
        self.s.headers.update(headers)
        self.username = username
        self.password = password
        self.pre_login_response = None
        self.ticket = None  # ticket to login
        self.redirect_url = None  # redirect login url
        self.jsonp = None  # im handshake parameter
        self.client_id = None  # client_id to polling WeiboIM
        self.need_captcha = False  # Is Weibo Login need captcha
        self.is_login = False  # Is Weibo login
        self.im_ready = False  # Is IM ready to send or receive msg
        self.im_channel = None  # IM channel to subscribe
        self.msg_queue = None
        self.polling_id = 3  # IM polling_id start from 3

    def login(self):
        self._pre_login()
        # If needs captcha, login interrupt
        if self.need_captcha:
            return
        self._post_login()
        self._get_login()
        self._redirect_login()
        logger.info('weibo login success')
        self.is_login = True

    def get_captcha(self):
        if self.captcha_url is None:
            return None
        return self.s.get(self.captcha_url).content

    def login_with_captcha(self, captcha):
        self._post_login(captcha=captcha)
        self._get_login()
        self._redirect_login()
        logger.info('weibo login success')
        self.is_login = True

    def _pre_login(self):
        url = 'https://login.sina.com.cn/sso/prelogin.php'
        params = {
            'entry': 'weibo',
            'callback': 'sinaSSOController.preloginCallBack',
            'su': self._get_encrypted_username(),
            'rsakt': 'mod',
            'checkpin': '1',
            'client': 'ssologin.js(v1.4.19)',
            '_': int(time.time() * 1000)
        }
        logger.debug('attempt to pre login url : %s params : %s' % (url, params))
        response = self.s.get(url, params=params)
        regex = 'sinaSSOController.preloginCallBack\((.*)\)'
        response_text = re.search(regex, response.text).group(1)
        response_data = json.loads(response_text)
        logger.debug('pre login response : %s' % response_data)
        self.pre_login_response = response_data

        # check if needs captcha
        if self.pre_login_response['showpin'] == 1:
            self.need_captcha = True
        logger.debug('Is need captcha: %s' % self.need_captcha)
        self.post_servertime = int(time.time())
        if self.need_captcha:
            self.captcha_url = 'http://login.sina.com.cn/cgi/pin.php?r=%d&s=0&p=%s' \
                           % (self.post_servertime, self.pre_login_response['pcid'])

    def _post_login(self, captcha=None):
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        servertime = self.post_servertime
        nonce = self.pre_login_response['nonce']
        pubkey = self.pre_login_response['pubkey']
        rsakv = self.pre_login_response['rsakv']
        params = {
            'entry': 'weibo',
            'gateway': '1',
            'from': "",
            'savestate': '7',
            'qrcode_flag': 'false',
            'userticket': '1',
            'pagerefer': "",
            'vsnf': '1',
            'su': self._get_encrypted_username(),
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': self._get_encrypted_password(servertime=servertime, nonce=nonce, pubkey=pubkey),
            'sr': '1920*1080',
            'encoding': 'UTF-8',
            'prelt': '42',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'TEXT'
        }

        # put captcha to params
        if self.need_captcha:
            params['pcid'] = self.pre_login_response['pcid']
            params['door'] = captcha

        logger.debug('attempt to post login url : %s params : %s' % (url, params))
        response_json = self.s.post(url, data=params).json()
        if response_json['retcode'] == '0':
            self.ticket = response_json['ticket']
            logger.debug('%s post login success ticket : %s' % (response_json['nick'], self.ticket))
        else:
            logger.error(
                'post login failed retcode : %s reason: %s' % (response_json['retcode'], response_json['reason']))
            raise ConnectionRefusedError

    def _get_encrypted_password(self, servertime, nonce, pubkey):
        encypted_string = str(servertime) + '\t' + str(nonce) + '\n' + str(self.password)
        key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
        pw_encypted = rsa.encrypt(encypted_string.encode('utf-8'), key)
        pw = binascii.b2a_hex(pw_encypted)
        return pw.decode('utf-8')

    def _get_encrypted_username(self):
        return base64.b64encode(urllib.parse.quote(self.username).encode('utf-8')).decode('utf-8')

    def _get_login(self):
        url = 'https://passport.weibo.com/wbsso/login'
        now = time.time()
        params = {
            'ssosavestate': int(now) + 365 * 86400,
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack&sudaref=weibo.com',
            'ticket': self.ticket,
            'recode': '0'
        }
        logger.debug('attempt to get login url : %s params : %s' % (url, params))
        response = self.s.get(url, params=params)
        regex = 'sinaSSOController.feedBackUrlCallBack\((.*)\);'
        response_text = re.search(regex, response.text).group(1)
        response_json = json.loads(response_text)
        self.redirect_url = 'https://weibo.com/%s' % response_json['userinfo']['userdomain']
        logger.debug('get login response url : %s' % self.redirect_url)

    def _redirect_login(self):
        url = self.redirect_url
        logger.debug('attempt to redirect login url : %s' % url)
        response = self.s.get(self.redirect_url)
        logger.debug('redirect login success')

    def im_init(self):
        if not self.im_ready:
            self._request_webim()
            self._handshake()
            self._subscribe_msg()
            self._switch_to_xiaoice()
            self.msg_queue = queue.Queue(10)
            Thread(target=self._polling_msg_from_xiaoice).start()
            logger.info('Weibo IM init success')
            self.im_ready = True

    def _request_webim(self):
        url = 'http://api.weibo.com/webim/webim_nas.json'
        params = {
            'source': '209678993',
            'returntype': 'json',
            'v': '1.1',
            'source': '209678993',
            'callback': 'angular.callbacks._2'
        }
        self.s.headers.update({'Referer': 'http://api.weibo.com/chat/'})
        logger.debug('attempt to request_webim url : %s params : %s' % (url, params))
        response = self.s.get(url, params=params)
        logger.debug('request_webim success response : %s' % response.text)
        regex = 'angular.callbacks._2\((.*)\);'
        response_text = re.search(regex, response.text).group(1)
        response_json = json.loads(response_text)
        self.im_channel = response_json['channel']
        logger.debug('im subscribe channel : %s' % self.im_channel)

    def _handshake(self):
        url = 'http://web.im.weibo.com/im/handshake'
        now = int(time.time() * 1000)
        self.jsonp = 'jQuery214024520499455942235_' + str(now)
        params = {
            'jsonp': self.jsonp,
            'message': '[{"version": "1.0", "minimumVersion": "1.0", "channel": "/meta/handshake","supportedConnectionTypes": ["callback-polling"], "advice": {"timeout": 60000, "interval": 0},"id": "2"}]',
            '_': now
        }
        logger.debug('attempt to handshake url : %s params : %s' % (url, params))
        response = self.s.get(url, params=params)
        logger.debug('handshake success response : %s' % response.text)
        regex = '\(\[(.*)\]\)'
        response_text = re.search(regex, response.text).group(1)
        response_json = json.loads(response_text)
        self.client_id = response_json['clientId']
        logger.debug('Weibo IM client id : %s' % self.client_id)

    def _subscribe_msg(self):
        url = 'http://web.im.weibo.com/im/'
        now = int(time.time() * 1000)
        params = {
            'jsonp': self.jsonp,
            'message': ('[{"channel":"/meta/subscribe","subscription":"%s","id":"%s","clientId":"%s"}]'
                        % (self.im_channel, self.polling_id, self.client_id)),
            '_': now
        }
        self.polling_id += 1
        logger.debug('attempt to subscribe url : %s params : %s' % (url, params))
        response = self.s.get(url, params=params)
        logger.debug('subscribe success response : %s' % response.text)

    def _switch_to_xiaoice(self):
        url = 'http://web.im.weibo.com/im/'
        now = int(time.time() * 1000)
        params = {
            'jsonp': self.jsonp,
            'message': (
            '[{"channel":"/im/req","data":{"cmd":"synchroniz","type":"dmread","uid":%s},"id":"%s","clientId":"%s"}]'
            % (xiaoice_uid, self.polling_id, self.client_id)),
            '_': now
        }
        self.polling_id += 1
        logger.debug('attempt to switch to xiaoice url : %s params : %s' % (url, params))
        response = self.s.get(url, params=params)
        logger.debug('switch to xiaoice success response : %s' % response.text)

    def get_msg_from_xiaoice(self, timeout):
        try:
            msg = self.msg_queue.get(timeout=timeout)
        except queue.Empty:
            return None
        return msg

    def post_msg_to_xiaoice(self, msg):
        url = 'http://api.weibo.com/webim/2/direct_messages/new.json?source=209678993'
        params = {
            'text': urllib.parse.quote(msg),
            'uid': xiaoice_uid
        }
        self.polling_id += 1
        logger.debug('attempt to post msg url : %s params : %s' % (url, params))
        response = self.s.post(url, data=params)
        logger.debug('post msg success response : %s' % response.text)

    def _polling_msg_from_xiaoice(self):
        while True:
            url = 'http://web.im.weibo.com/im/connect'
            now = int(time.time() * 1000)
            params = {
                'jsonp': self.jsonp,
                'message': '[{"channel":"/meta/connect","connectionType":"callback-polling","id":"%s","clientId":"%s"}]'
                           % (self.polling_id, self.client_id),
                '_': now
            }
            self.polling_id += 1
            logger.debug('attempt to polling IM url : %s params : %s' % (url, params))
            response = self.s.get(url, params=params)
            logger.debug('polling IM success response : %s' % response.text)
            regex = '\(\[(.*)\]\)'
            match = re.search(regex, response.text)
            if match is not None:
                response_content = match.group(1)
                im_datas = Weibo._split_data_from_polling_response(response_content)
                for im_data in im_datas:
                    if 'data' in im_data and 'type' in im_data['data'] and im_data['data']['type'] == 'msg':
                        for item in im_data['data']['items']:
                            if item[0] == xiaoice_uid:
                                self.msg_queue.put(item[1])
            time.sleep(polling_wait_second)

    @staticmethod
    def _split_data_from_polling_response(response_content):
        """
        this function helps to split IM data from multiple json response
        example response text:
            {"data":{"lastmid":4131597492035838,"type":"unreader","items":{"total":6,"5175429989":6},"dm_isRemind":0},"channel":"/im/5908081220"},
            {"data":{"ret":0},"channel":"/im/5908081220","id":"4"},
            {"data":{"type":"synchroniz","ret":0},"channel":"/im/5908081220","id":"4"},
            {"advice":{"interval":0,"timeout":170000,"reconnect":"retry"},"channel":"/meta/connect","id":"6","successful":true}
        split each json string and convert to dict object, add all to list [{data1:...}, {data:...}, ...]
        :param response_content:
        :return:a list of dict object split from response_content
        """
        datas = []
        # scan response_content
        left_parenthesis_count = 0
        right_parenthesis_count = 0
        data = ''
        is_start = False
        for char in response_content:
            if char == '{':
                is_start = True
                left_parenthesis_count += 1
            if char == '}':
                right_parenthesis_count += 1
            if is_start:
                data += char
                if left_parenthesis_count == right_parenthesis_count:
                    data_json = json.loads(data)
                    datas.append(data_json)
                    data = ''
                    left_parenthesis_count = 0
                    right_parenthesis_count = 0
                    is_start = False
        return datas


def init_weibo_im(weibo_username, weibo_password):
    weibo = Weibo(weibo_username, weibo_password)
    weibo.login()
    if weibo.is_login:
        weibo.im_init()
    return weibo


def init_weibo_im_with_captcha(weibo, captcha):
    weibo.login_with_captcha(captcha)
    weibo.im_init()
