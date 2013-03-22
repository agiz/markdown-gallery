import os, re

from twisted.python.filepath import FilePath
from twisted.internet.inotify import IN_MODIFY, IN_CREATE, INotify
from twisted.internet import reactor

import gallery

WATCH_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
WATCH_DIR_LEN = len(WATCH_DIRECTORY)

galleries = {}
call_ids = {}

CALL_DELAY = 30
"""Seconds to wait before creating gallery."""

THUMBNAIL_PREFIX = 't_'
THUMBNAILS_DIR = 't'
OUTPUT_FILE = 'index.md'
IGNORE_LIST = (THUMBNAILS_DIR, THUMBNAIL_PREFIX, OUTPUT_FILE)
"""Do not trigger the if file is likely to be created by the process."""

def process_handler(gallery_root):
    if gallery_root not in galleries:
        galleries[gallery_root] = gallery.Gallery(gallery_root)
    return galleries[gallery_root].process_gallery(
        WATCH_DIRECTORY, WATCH_DIR_LEN)

def find_root(pathname, dir_len=WATCH_DIR_LEN):
    head, tail = os.path.split(pathname)
    oldhead = head
    while head and tail and dir_len != len(head):
        oldhead = head
        head, tail = os.path.split(head)
    return oldhead

def greed_controller(pathname):
    print 'WORKING:', pathname
    process_handler(pathname)
    print 'DONE:', pathname

def created(ignored, path, mask):
    basename = path.basename()
    if re.match(r'^\.|^t$|^t_|^index\.md$', basename):
        return

    pathname = path.path
    pathname = find_root(pathname)
    if pathname not in call_ids or not call_ids[pathname].active():
        print 'SET:', pathname
        call_ids[pathname] = reactor.callLater(CALL_DELAY, greed_controller, pathname)
    else:
        print 'RESET:', pathname
        call_ids[pathname].reset(CALL_DELAY)

notifier = INotify()
notifier.watch(
    FilePath(WATCH_DIRECTORY),
    mask=IN_MODIFY|IN_CREATE,
    callbacks=[created],
    autoAdd=True,
    recursive=True
)
notifier.startReading()
reactor.run()
