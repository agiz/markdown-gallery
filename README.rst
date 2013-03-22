markdown gallery
========
.. image:: https://travis-ci.org/markdown-gallery/markdown-gallery.png?branch=master
   :target: https://travis-ci.org/markdown-gallery/markdown-gallery
   :alt: Build status

**Table of Contents**

.. contents::
    :local:
    :depth: 1
    :backlinks: none

About
-----
markdown gallery watches a directory for new images, generates
thumbnails and outputs a markdown file with your images.


Usage
-----
You might want to change:

- in gallery_to_markdown.py
    ABSOLUTE_URL: Absolute url of your site. `http://mysite.com/gallery`.

- in gallery.py
    THUMBNAIL_PREFIX: Prefix for thumbnail. Defaults to `t_`
    THUMBNAILS_DIR: Name of thumbnail directory inside a gallery, default `t`.
    THUMBNAIL_SIZE: Defaults to `128x128`.

- in gallery_watcher.py
    THUMBNAIL_PREFIX, THUMBNAILS_DIR, THUMBNAIL_SIZE, OUTPUT_FILE:
    These constants are ignored by gallery_watcher.
    This is redundant but keep it same as in gallery.py.
    WATCH_DIRECTORY: root directory of your galleries. That would be
    `/home/galleries` in below file tree.
::

  |-- home
  |   |-- galleries
  |       |-- gallery_1
  |       |-- gallery_2
  |       `-- gallery_3


-run `python gallery_watcher.py`
