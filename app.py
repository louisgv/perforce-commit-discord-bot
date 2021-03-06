import os
import subprocess
import time
from discord_webhooks import DiscordWebhooks
from settings import DISCORD_WEBHOOK_URL, DISCORD_TITLE

# Stores the most recent commit.
global_store = {
  'latest_change': ''
}

def check_for_changes():
  """ Runs the p4 changes command to get the latest commits from the server. """
  p4_changes = subprocess.Popen('p4 changes -t -m 1 -l', stdout=subprocess.PIPE, shell=True)
  output = p4_changes.stdout.read().decode('ISO-8859-1')

  if output != global_store['latest_change']:
    global_store['latest_change'] = output

    if '*pending*' in output: 
      return ''

    else:
      return output

  else: 
    return ''

def post_changes():
  """ Posts the changes to the Discord server via a webhook.  """
  payload = check_for_changes()

  if payload != '':
    message = DiscordWebhooks(DISCORD_WEBHOOK_URL)
    message.set_content(color=0xc8702a, description='`%s`' % (payload))
    message.set_author(name=DISCORD_TITLE)
    message.send()

  else:
    return

def init():
  """ Initializes a 30 second timer used to check if commits have been made.  """
  timer = time.time()

  while True:
    post_changes()
    time.sleep(30.0 - ((time.time() - timer) % 30.0))

init()
