import datetime, glob, os, sys

import Image

import gallery_to_markdown as output_format
#import gallery_to_html as output_format # Someone has to write that.

THUMBNAIL_PREFIX = 't_'
THUMBNAILS_DIR = 't'
THUMBNAIL_SIZE = (128, 128)
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
            os.makedirs(thumbnails_path)
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
                if tmp_thumb not in self.thumbnails:
                    self.create_thumbnail(image, tmp_thumb)
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

    def create_thumbnail(self, image, thumb):
        base, ext = os.path.splitext(image)
        size = THUMBNAIL_SIZE
        try:
            im = Image.open(image)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(thumb, IMAGE_TYPE[ext.lower()])
            self.thumbnails.append(thumb)
        except IOError:
            raise Exception('Could not create thumbnail!')
