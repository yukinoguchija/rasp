# -*- coding: utf-8 -*-
 
import requests
import json
class SlackMessage:
    slackUrl = 'https://hooks.slack.com/services/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'
    message = u'暗くなったから灯りをつけたよ'
    def post(self):
        requests.post(self.slackUrl, data = json.dumps({
            'text': self.message, # 投稿するテキスト
            'username': u'raspberry', # 投稿のユーザー名
            'icon_emoji': u':ghost:', # 投稿のプロフィール画像に入れる絵文字
            'link_names': 1, # メンションを有効にする
        }))

slack = SlackMessage()

slack.post()