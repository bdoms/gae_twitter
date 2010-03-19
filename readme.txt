GAE Twitter is a project to provide bare-bones Twitter integration for Google
App Engine that makes no assumptions, and is easy to integrate with existing
apps.


= Status =

Right now GAE Twitter only supports reading (i.e. GET) without authentication.
If you want to POST data or have to authenticate, feel free to submit a patch
or file a specific issue.


= Setup =

In your pre-existing application add this project as a submodule, like so:

    git submodule add git://github.com/bdoms/gaetwitter.git gaetwitter

Next, you need to initialize and update the submodule to get the data:

    git submodule init
    git submodule update

And then just add this to your app.yaml 'handlers' section:

    - url: /twitter.*
      script: gaetwitter/twitter.py
      login: admin

Now you just need to configure it by changing which user you want it to user.
In config.py change the 'TWITTER_USER' variable to the screen name of the user
you want to follow.

You also need to add the job to your parent application's cron.yaml file. See
the included one for an example.


= Use =

GAE Twitter just updates a single database entry with the most recent post from
the user specified in the config.py file. To use this data, grab it from the
model:

    from gaetwitter import model
    post = model.getPost()

The post object only has two properties for you to worry about:

    post.body # the actual content of the post
    post.timestamp # when it happened (Python datetime object in UTC)

