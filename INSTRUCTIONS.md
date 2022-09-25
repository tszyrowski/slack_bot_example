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

# Event subscription

Events are all what is going on in the channel

Go to: `Slack API` -> `Event Subscriptions` turn on `Enable Events`
It gives a `Request URL` option which is an endpoint of app running on a server

## NGROK
https://dashboard.ngrok.com/get-started/setup

download, unzip file and `cd` to directory where it sits

run with 
`./ngrok http 5000`

It should provide the output similar to:
```
ngrok                                                                                                         (Ctrl+C to quit)
                                                                                                                              
Visit http://localhost:4040/ to inspect, replay, and modify your requests                                                     
                                                                                                                              
Session Status                online                                                                                          
Account                       [your name] (Plan: Free)                                                                             
Version                       3.1.0                                                                                           
Region                        Europe (eu)                                                                                     
Latency                       24ms                                                                                            
Web Interface                 http://127.0.0.1:4040                                                                           
Forwarding                    https://[some url].eu.ngrok.io -> http://localhost:5000                                     
                                                                                                                              
Connections                   ttl     opn     rt1     rt5     p50     p90                                                     
                              0       0       0.00    0.00    0.00    0.00 
```

## SlackEventApi

The event is handled by `SlackEventAdapter([signing secret],"/slack/events", app)` 
which takes the signing secret from `Slack API` -> `Basic Information` -> `Signing Secret`

It should be added to `.env`

## Linking together:

Go to `slack api` -> `Event Subscriptions` -> `Request URL` 
and post full endpoint (with `/slack/events`):

https://[some url].eu.ngrok.io/slack/events

Slack will `POST` to the endpoint to verify. The post can be seen locally in a browser:

http://localhost:4040/inspect/http

## Subscribe to event

Go to `slack api` -> `Event Subscriptions` -> `Subscribe to bot events`

add `channels.message`

| Event Name       |	Description                    | Required Scope
|------------------|-----------------------------------|------------------
| message.channels | A message was posted to a channel | channels:history

The above will automatically add scope

To verify:

Go to `slack api` -> `Event Subscriptions` -> `Scopes`

Bot Token Scopes

Scopes that govern what your app can access.

OAuth Scope      | Description
-----------------|------------ 
channels:history | View messages and other content in public channels that First Bot has been added to
chat:write       | Send messages as @first_bot

**After all the app needs to be reinstalled**

# Commands

They are different than events. They start with `/` in a channel

Go to `slack api` -> `Slash Commands` -> [Create New Command]

- in `Command` type in for example `/message-count`
- in `Request URL` create handle url for example: https://[some url].eu.ngrok.io/message-count
- fill up the rest

**Reinstall the app**

## chat_postMessage method

```
client.chat_postMessage.__doc__
'Sends a message to a channel.
        Args:
            channel (str): The channel id. e.g. \'C1234567890\'
            text (str): The message you\'d like to share. e.g. \'Hello world\'
                text is not required when presenting blocks.
            blocks (list): A dictionary list of blocks.
                Blocks are required when not presenting text.
                e.g. [{"type": "section", "text": {"type": "plain_text", "text": "Hello world"}}]
```

## use icons

Enable `chat:write.customize` in Go to `slack api` -> `OAuth & Permissions` -> `Scopes`