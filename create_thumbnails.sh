#! /bin/bash

## Generates jpg thumbnails from jp2s
# requires graphicsmagick and parallel

convert() {
  # configuration
  overwrite=false
  dimensions="360x512"

  # take the extension off of the file path
  filepath=${1%.*}
  if [ -e "$filepath.jpg" -a "$overwrite" = "false" ]; then
    echo "Did not replace the following file: $filepath.jpg"
  else
    echo "Creating file $filepath.jpg with dimensions $dimensions"
    gm convert -size "$dimensions" "$filepath.jp2" -resize "$dimensions" +profile "*" "$filepath.jpg"
  fi
}
export -f convert

begin=`date`
if [ $# == 1 ]; then
  # check that the directory exists
  if [ -d "$1" ]; then
    dir_path=$1
    # strip the trailing slash before running find
    find "${dir_path%/}" -type f -name "*.jp2" | parallel --jobs 200% convert

  else
    echo "Directory $1 does not exist"
    exit 1
  fi
else
  echo "Please specify a directory."
  echo "Example:  ./convert_images /batches/prefix_batch/batch_name/data/"
  exit 1
fi
end=`date`
echo "Script started at $begin"
echo "Script finished at $end"

