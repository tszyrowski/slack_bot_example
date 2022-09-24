# Add bot to a channel

The app needs to be connected to a particular channel. 
Without connection, sending messages results in failure:
```
7581 ± /home/t/workspace_slack/slack_bot_example/vSlackApp/bin/python /home/t/workspace_slack/slack_bot_example/bot.py
/home/t/workspace_slack/slack_bot_example/bot.py:2: DeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
  import imp
Traceback (most recent call last):
  File "/home/t/workspace_slack/slack_bot_example/bot.py", line 14, in <module>
    client.chat_postMessage(channel="#test", text="Hello from slack chat bot")
  File "/home/t/workspace_slack/slack_bot_example/vSlackApp/lib/python3.9/site-packages/slack/web/client.py", line 1077, in chat_postMessage
    return self.api_call("chat.postMessage", json=kwargs)
  File "/home/t/workspace_slack/slack_bot_example/vSlackApp/lib/python3.9/site-packages/slack/web/base_client.py", line 150, in api_call
    return self._sync_send(api_url=api_url, req_args=req_args)
  File "/home/t/workspace_slack/slack_bot_example/vSlackApp/lib/python3.9/site-packages/slack/web/base_client.py", line 241, in _sync_send
    return self._urllib_api_call(
  File "/home/t/workspace_slack/slack_bot_example/vSlackApp/lib/python3.9/site-packages/slack/web/base_client.py", line 369, in _urllib_api_call
    return SlackResponse(
  File "/home/t/workspace_slack/slack_bot_example/vSlackApp/lib/python3.9/site-packages/slack/web/slack_response.py", line 194, in validate
    raise e.SlackApiError(message=msg, response=self)
slack.errors.SlackApiError: The request to the Slack API failed.
The server responded with: {'ok': False, 'error': 'not_in_channel'}
```
Connection can be done by goint to `Slack`, in channel message `/invite <chose bot's name>`

