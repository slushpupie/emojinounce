# Emojinounce

Announce emoji as they change in Slack

## General Idea

For some Slack workspaces, emoji are a way of life.  As such, it becomes important to know which emoji are added, removed, or even aliased.  This very simple bot will post to a designated channel whenever such an evet occurs.

## Installation

The recommended way to run this, is via Docker image.  These instructions are fairly generic so that you can deploy your docker image the way you want (Kubernetes, Swarm, Nomad, etc)

You will need to run this on your own system somewhere that can receive HTTPS posts from Slack (or where you can use [ngrok](http://ngrok.com)) Directions for how to do this are beyond the scope of this document.  By default this will use the endpoint `/slack_events` to recieve events from Slack, but this can be customized using the environmental variable `SLACK_EVENTS_ENDPOINT`.

### 🏛 First, create an app on https://api.slack.com/apps 

![](https://cloud.githubusercontent.com/assets/32463/24877733/32979776-1de5-11e7-87d4-b5dc9e3e7973.png)

### 🤖 Add a bot user to your app

![](https://cloud.githubusercontent.com/assets/32463/24877750/47a16034-1de5-11e7-989b-2a90b9d8e7e3.png)

Visit your app's **Install App** page and click **Install App to Team**.

![](https://cloud.githubusercontent.com/assets/32463/24877770/61804c36-1de5-11e7-91ef-5cf2e0845729.png)

### 🔐 Authorize your app

![](https://cloud.githubusercontent.com/assets/32463/24877792/774ed94c-1de5-11e7-8857-ac8d662c5b27.png)

### 🔐 Save your app's credentials

Once you've authorized your app, you'll be presented with your app's tokens.

![](https://cloud.githubusercontent.com/assets/32463/24877652/d8eebbb4-1de4-11e7-8f75-2cfb1e9d45ee.png)


Copy your app's **Bot User OAuth Access Token** and add it to your  environmental variables

```
  export SLACK_BOT_TOKEN=xxxXXxxXXxXXxXXXXxxxX.xXxxxXxxxx
```

Next, go back to your app's **Basic Information** page

![](https://user-images.githubusercontent.com/32463/43932347-63b21eca-9bf8-11e8-8b30-0a848c263bb1.png)

Add your app's **Signing Secret** to your environmental variables

```
  export SLACK_SIGNING_SECRET=xxxxxxxxXxxXxxXxXXXxxXxxx
```

Create a channel in Slack where you want to post the announcements. You will need the channel ID, and add it to your environmental variables

```
  export SLACK_ANNOUNCE_CHANNEL_ID=C123456789
```

With all the environment variables set, you can now run the app:

```
  docker run -e SLACK_BOT_TOKEN -e SLACK_SIGNING_SECRET -e SLACK_ANNOUNCE_CHANNEL_ID -p 80:5000 slushpupie/emojinounce:latest
```

### ☑️Subscribe your app to events

Add your **Request URL** and subscribe your app to `emoji_changed` under bot events. **Save** and toggle **Enable Events** to `on`

![](https://user-images.githubusercontent.com/1573454/30185162-644d0cb8-93ee-11e7-96af-55fe10d9d5c8.png)

![](https://cloud.githubusercontent.com/assets/32463/24877931/e119181a-1de5-11e7-8b0c-fcbc3419bad7.png)

### 🎉  Once your app has been installed and subscribed to Bot Events, you will begin receiving event data from Slack**

Now when you change a custom emoji on your workspace, your emojinounce bot will output it to the channel!


🤔  Support
------------

Need help?  `create an Issue`_ right here on GitHub.


🚀Contributing workflow
-----------------------

Here’s how we suggest you go about proposing a change to this project:

 1. Fork this project to your account.
 2. Create a branch for the change you intend to make.
 3. Make your changes to your fork.
 4. Send a pull request from your fork’s branch to our master branch.
 5. Using the web-based interface to make changes is fine too, and will help you by automatically forking the project and prompting to send a pull request too.

👩‍⚖️License
---------
[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)
