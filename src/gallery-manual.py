# Manually start the process of making markdown gallery.

import datetime, glob, os, sys

import gallery_to_markdown as output_format

THUMBNAIL_PREFIX = 't_'
THUMBNAILS_DIR = 't'
EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
IMAGE_TYPE = {
    '.jpg': 'JPEG',
    '.jpeg': 'JPEG',
    '.gif': 'GIF',
    '.png': 'PNG'
}

class Gallery(object):
    """Manipulate images in this gallery."""

    def __init__(self, gallery_path):
        self.gallery_path = gallery_path
        self.thumbnails = []
        self.images = []
        self.image_thumb_pair = []

    def process_gallery(self, absolute_path, path_prefix_len):
        """Entry point that controls the flow."""
        self.path_prefix_len = path_prefix_len
        self.list_images()
        output_format.save_file(absolute_path, self.image_thumb_pair)

    def list_thumbnails(self, thumbnails_path):
        if not os.path.exists(thumbnails_path):
            try:
                os.makedirs(thumbnails_path)
            except OSError:
                pass
            return []

        thumbnails = glob.glob(thumbnails_path + os.sep + '*')
        return thumbnails

    def list_images(self):
        self.thumbnails = self.list_thumbnails(
            os.path.join(self.gallery_path, THUMBNAILS_DIR))

        images = glob.glob(self.gallery_path + os.sep + '*')
        images = filter(os.path.isfile, images)
        for image in images:
            base, ext = os.path.splitext(image)
            if ext.lower() in EXTENSIONS:
                tmp_thumb = self.create_thumbnail_name(image)
                self.image_thumb_pair.append((
                    image[self.path_prefix_len:],
                    tmp_thumb[self.path_prefix_len:]
                ))

    def create_thumbnail_name(
        self,
        image,
        thumb_dir=THUMBNAILS_DIR,
        prefix=THUMBNAIL_PREFIX
    ):
        image_path, image_name = os.path.split(image)
        thumbnail_name = os.path.join(
            image_path,
            thumb_dir,
            prefix + image_name
        )
        return thumbnail_name

WATCH_DIR_LEN = len(os.getcwd())

def find_root(pathname, dir_len=WATCH_DIR_LEN):
    head, tail = os.path.split(pathname)
    return head, tail

WATCH_DIRECTORY, gallery_name = find_root(os.getcwd())
WATCH_DIR_LEN = len(WATCH_DIRECTORY)
WATCH_DIRECTORY = os.getcwd()

fu, idiot = find_root(os.getcwd())


gallery = Gallery(WATCH_DIRECTORY)
gallery.process_gallery(fu, WATCH_DIR_LEN)