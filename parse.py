def print_tweet(t):
    import json
    tw = json.loads(t)
    print "%s: %s" % (tw["user"]["screen_name"], tw["text"])
