from RSSItem import Item
import feedparser
from future import Future
try:
	import cPickle as pickle
except:
	import pickle
from lockfile import FileLock
from time import sleep
from functions import *
import socket
from gi.repository import GObject
from gi.repository import Notify
import os
import sys

hasher = []

class Notification(GObject.Object):
    def __init__(self):

        super(Notification, self).__init__()
        # lets initialise with the application name
        Notify.init("RSS Updater")

    def send_notification(self, title, text, file_path_to_icon=""):

        n = Notify.Notification.new(title, text, file_path_to_icon)
        n.show()

def getFeeds(hit_list):
    future_calls = [Future(feedparser.parse,rss_url) for rss_url in hit_list]
    feeds = [future_obj() for future_obj in future_calls]
    return feeds

def parseFeed(feed):
    return [Item(x) for x in feed["items"]]


def loadFeeds(location):
    lock = getFileLock("/tmp", "feeds.txt")
    with open("%s/feeds.txt" % location, "r") as fp:
        data = fp.readlines()
    lock.release()
    return [x.replace("\n", "") for x in data]

def update(location, feedItems):
    lock = getFileLock("/tmp", "rssItems.pkl")
    items = loadItems(location)
    notary = Notification()
    for x in feedItems:
        if x.isOld():
            continue
        if x not in items:
            items.append(x)
            notary.send_notification("New RSS Item", x.name, "/media/joshua/YUKI_N/RSS/cgi-bin/rss.svg")
            os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( .1, 250))
    items.sort()
    dumpItems(location, items)
    lock.release()
    return
    
def stripOld(location):
    lock = getFileLock("/tmp", "rssItems.pkl")
    items = loadItems(".")
    a = [x for x in items if (not x.isOld() and x.isRead())]
    dumpItems(".", a)
    lock.release()
    return

def main():
    lock = FileLock("./rssItems.pkl")
    lock.break_lock()
    lock = FileLock("./feeds.txt")
    lock.break_lock()
    #feeds = loadFeeds(".")
    #print "Doing initial load of: %s" % feeds
    #feeds = getFeeds(feeds)
    #for x in feeds:
    #    temp = parseFeed(x)
    #    update(".", temp)
    socket.setdefaulttimeout(30)
    stripOld(".")
    lock = getFileLock("/tmp", "rssItems.pkl")
    global hasher
    hasher = loadItems(".")
    lock.release()
    while(True):
        #stripOld(".")
        feeds = loadFeeds(".")
        for x in feeds:
            print "--------\nWorking on %s" % x
            try:
				current = getFeeds([x])[0]
				feedItems = parseFeed(current)
				update(".", feedItems)
				print "Finished updating %s" % x 
            
            except Exception as e:
				print "Skipped %s" % x
				with open("debug.txt", "ab") as fp:
					fp.write("Broke with %s : %s\n" % (x, str(e)))
            sleep(120. / len(feeds))
        
        
if __name__ == "__main__":
    main()
            
