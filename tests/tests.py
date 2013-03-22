import os, sys, time, unittest

WATCH_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
GALLERY_NAME = 'fixtures'
GALLERY_PATH = os.path.join(
    WATCH_DIRECTORY,
    GALLERY_NAME
)

THUMBNAIL_PREFIX = 't_'
THUMBNAILS_DIR = 't'
THUMBNAILS_PATH = os.path.join(GALLERY_PATH, THUMBNAILS_DIR)

GIF_IMAGE_NAME = 'python-logo.gif'
GIF_IMAGE_PATH = os.path.join(
    WATCH_DIRECTORY,
    GALLERY_NAME,
    GIF_IMAGE_NAME
)

JPG_IMAGE_NAME = 'logo.jpg'
JPG_IMAGE_PATH = os.path.join(
    WATCH_DIRECTORY,
    GALLERY_NAME,
    JPG_IMAGE_NAME
)

OUTPUT_FILENAME = 'mygallery.md'

# HACK: Prepend ../ to PYTHONPATH so that we can import httpie form there.
TESTS_ROOT = WATCH_DIRECTORY
sys.path.insert(0, os.path.realpath(os.path.join(TESTS_ROOT, '..')))

from src import gallery
from src import gallery_to_markdown

class GalleryTest(unittest.TestCase):
    def setUp(self):
        self.gallery = gallery.Gallery(GALLERY_PATH)

    def tearDown(self):
        for root, dirs, files in os.walk(THUMBNAILS_PATH, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
            try:
                os.rmdir(root)
            except OSError:
                raise Exception('Directory is not empty!')

    def test_list_thumbnails_empty(self):
        thumbnails = self.gallery.list_thumbnails(THUMBNAILS_PATH)
        self.assertEqual(thumbnails, [])

    def test_create_thumbnail_name(self):
        thumbnail_name = self.gallery.create_thumbnail_name(
            GIF_IMAGE_PATH,
            THUMBNAILS_DIR,
            THUMBNAIL_PREFIX
        )

        self.assertEqual(
            thumbnail_name,
            os.path.join(
                GALLERY_PATH,
                THUMBNAILS_DIR,
                THUMBNAIL_PREFIX + GIF_IMAGE_NAME
            )
        )

    def test_create_thumbnail_gif(self):
        self.gallery.list_thumbnails(THUMBNAILS_PATH)
        time.sleep(1)

        thumbnail_name = self.gallery.create_thumbnail_name(
            GIF_IMAGE_PATH,
            THUMBNAILS_DIR,
            THUMBNAIL_PREFIX
        )

        self.gallery.create_thumbnail(
            GIF_IMAGE_PATH,
            thumbnail_name
        )

        time.sleep(1)
        self.assertTrue(os.path.isfile(thumbnail_name))

    def test_create_thumbnail_jpg(self):
        self.gallery.list_thumbnails(THUMBNAILS_PATH)
        time.sleep(1)

        thumbnail_name = self.gallery.create_thumbnail_name(
            JPG_IMAGE_PATH,
            THUMBNAILS_DIR,
            THUMBNAIL_PREFIX
        )

        self.gallery.create_thumbnail(
            JPG_IMAGE_PATH,
            thumbnail_name
        )

        time.sleep(1)
        self.assertTrue(os.path.isfile(thumbnail_name))

    def test_list_thumbnails_full(self):
        self.test_create_thumbnail_gif()
        self.test_create_thumbnail_jpg()

        thumbnails = self.gallery.list_thumbnails(THUMBNAILS_PATH)
        self.assertEqual(len(thumbnails), 2)

class MarkdownTest(unittest.TestCase):
    def tearDown(self):
        os.remove(os.path.join(GALLERY_PATH, OUTPUT_FILENAME))

    def test_save_file(self):
        image_thumbnail_pairs = (('/fixtures/a.jpg', '/fixtures/t/t_a.jpg'),)
        gallery_to_markdown.save_file(
            WATCH_DIRECTORY,
            image_thumbnail_pairs,
            OUTPUT_FILENAME,
            'http://localhost/gallery'
        )

        file_size = 0
        try:
            file_size = os.path.getsize(os.path.join(
                GALLERY_PATH, OUTPUT_FILENAME))
        except OSError:
            raise Exception('Cannot read file!')

        self.assertTrue(file_size > 0)

def main():
    unittest.main()

if __name__ == '__main__':
    main()