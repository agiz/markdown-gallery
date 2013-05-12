#!/bin/bash

if [ $# -eq 0 ] ; then
  echo 'usage: ./jpeg_optimize.sh "*.jpg"'
  exit 0
fi

# OS X:
# brew install imagemagick # (convert, identify)
# brew install jpegoptim
# brew install libjpeg-turbo # (jpegtran)

# Baseline ("Standard") to use a format recognizable to most Web browsers. 
# Baseline Optimized to optimize the color quality of the image and produce a slightly smaller file size. This option is not supported by all Web browsers. 
# Progressive to create an image that displays gradually as it is downloaded--in a series of scans (you specify how many) showing increasingly detailed versions of the entire image. Progressive JPEG images files are slightly larger in size, require more RAM for viewing, and are not supported by all applications and Web browsers.

# http://www.yuiblog.com/blog/2008/12/05/imageopt-4/

THUMBNAILS_DIR='t'
THUMBNAIL_PREFIX='t_'
THUMBNAIL_SIZE='x128'
THUMBNAILS_QUALITY='65'

check_interlace() {
  idout=`identify -verbose "${1}" | grep -i interlace | grep -i none$`
  if [[ -z $idout ]]
  then
    echo "${1} is progressive"
  else
    echo "${1} is non-progressive"
  fi
}

make_thumbnail() {
  # convert image to 128 height
  convert "${1}" -interlace none -resize ${THUMBNAIL_SIZE} "./${THUMBNAILS_DIR}/${THUMBNAIL_PREFIX}${1}"
  # set quality to 65, strip meta-data, optimize
  jpegoptim --strip-all -m${THUMBNAILS_QUALITY} -f "./${THUMBNAILS_DIR}/${THUMBNAIL_PREFIX}${1}"
}

# make thumbnails directory
mkdir -p "./${THUMBNAILS_DIR}"

for img in `find . -iname "${1}" -type f -depth 1`
do
  # strip ./ in front of file
  img="${img#./}"

  make_thumbnail "${img}"

  # convert big images to progressive
  #image_optim "${img}"
  # default image_optim chain:
  jpegoptim --strip-all -f "${img}"
  jpegtran -copy none -progressive "${img}" >"progressive_${img}"
  mv "progressive_${img}" "${img}"
done
