import requests
import json
import logging
import time
import datetime
import pytz
from pytz import timezone

class SlackMessaging():

  def post_image(self, message, image_url, title='Sekurrity!!'):
      slack_url = 'https://hooks.slack.com/services/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'
      slack_attachments = []
      slack_date = datetime.datetime.now(tz=pytz.utc).astimezone(timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M:%S')
      footer = 'Posted at: ' + slack_date

      slack_attachment = { "title" : title, "footer" : footer }
      slack_attachment['image_url'] = image_url
      slack_attachments.append(slack_attachment)

      payload = {
           'username': 'Bot Qui Qui',
           'icon_emoji': 'eye',
           'link_names' : '1',
           'channel': 'sekurrity',
           'text': message,
           'attachments': slack_attachments
      }
      headers = {
           'cache-control': "no-cache",
           'content-type': "application/x-www-form-urlencoded"
      }
      response = requests.request("POST", slack_url, data=json.dumps(payload), headers=headers)
      logging.info ("slack response = " + str(response))
      logging.info ("slack response = " + str(response.text))
