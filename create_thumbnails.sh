#! /bin/bash

## Generates a chronicling america batch's thumbnails from a jp2
# For an explanation of how convert gets called from inside -exec
# http://unix.stackexchange.com/questions/50692/executing-user-defined-function-in-a-find-exec-call

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

if [ $# == 1 ]; then
  # check that the directory exists
  if [ -d "$1" ]; then
    dir_path=$1
    # strip the trailing slash before running find
    # do fancy things in order to get the convert function into the subshell
    find "${dir_path%/}" -type f -name "*.jp2" -exec bash -c 'convert "$@"' bash {} \;

  else
    echo "Directory $1 does not exist"
  fi
else
  echo "Please specify a directory."
  echo "Example:  ./convert_images /batches/nbu_ford/batch_nbu_ford_ver01/data/"
fi
