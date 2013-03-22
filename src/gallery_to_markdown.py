import codecs, os, re

ABSOLUTE_URL = ''
RELATIVE_URL = '/'
"""
Absolute and relative host path.
You might want to put something like:
'//floating-woodland-6230.herokuapp.com/i'
as your ABSOLUTE_URL - without trailing slash.
"""

OUTPUT_FILE = 'index.md'

def save_file(
    absolute_path,
    pairs,
    output_filename=OUTPUT_FILE,
    absolute_url=ABSOLUTE_URL
):
    gallery_name = ''
    gallery_holder = []

    for image, thumb in pairs:
        image_path, image_name = os.path.split(image)
        image_name, image_ext = os.path.splitext(image_name)
        gallery_path, gallery_name = os.path.split(image_path)
        gallery_title = gallery_name.strip()
        if gallery_title and not re.match("^[A-Za-z]*$", gallery_title[0]):
            gallery_title = 'Gallery ' + gallery_title
        permalink = RELATIVE_URL + gallery_name
        if len(permalink) > 1:
            permalink = permalink + '/'
        image_link = '[![%s](%s)](%s)' % (
            image_name,
            absolute_url + thumb,
            absolute_url + image
        )
        gallery_holder.append(image_link)

    output_file = os.path.join(absolute_path, gallery_name, output_filename)
    with codecs.open(output_file, 'wb', 'utf-8') as f:
        f.write('---\n')
        f.write('title: \'' + gallery_title + '\'\n')
        f.write('layout: gallery\n')
        f.write('permalink: ' + permalink + '\n')
        f.write('---\n')
        f.write('\n'.join(gallery_holder))
    f.close()
