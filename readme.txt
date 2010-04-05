GAE Twitter is a project to provide bare-bones Twitter integration for Google
App Engine that makes no assumptions, and is easy to integrate with existing
apps.


= Status =

Right now GAE Twitter only supports reading (i.e. GET) without authentication.
If you want to POST data or have to authenticate, feel free to submit a patch
or file a specific issue.


= Setup =

In your pre-existing application add this project as a submodule, like so:

    git submodule add git://github.com/bdoms/gae_twitter.git gae_twitter

Next, you need to initialize and update the submodule to get the data:

    git submodule init
    git submodule update

And then just add this to your app.yaml 'handlers' section:

    - url: /twitter.*
      script: gae_twitter/twitter.py
      login: admin

Now you just need to configure it by changing which user to follow, and by
setting up the cron job. You'll need to create or modify your project's
cron.yaml file to do this. The included example job looks like this:

    - description: check for updates to a user's twitter status
      url: /twitter?screen_name=twitterapi
      schedule: every 15 minutes

You can easily modify the rate at which it checks, and the screen name it uses.


= Use =

GAE Twitter just updates a single database entry with the most recent post from
the user specified in the config.py file. To use this data, grab it from the
model:

    from gae_twitter import model
    post = model.getPost()

The post object only has two properties for you to worry about:

    post.body # the actual content of the post
    post.timestamp # when it happened (Python datetime object in UTC)

