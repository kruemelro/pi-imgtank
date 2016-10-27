#!/bin/bash
# ---------------------------------------------------------------------------
# This file contains common functions for copy_img2/mv_img2.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pi-imgtank
#
# ---------------------------------------------------------------------------

# --- global settings   -----------------------------------------------------

setGlobalDefaults() {
  SCRIPT=$(basename "$0")
  DEBUG=1                               # writes to syslog if set to 1
  DATA_ROOT="/data"                     # Root of data/backup-directory
  DATA_OWNER="pi:pi"                    # uid:gid of data-owner
  IMAGE_ROOT="$DATA_ROOT/images"        # Root of image-directory
  THUMB_ROOT="$DATA_ROOT/thumbnails"    # Root of thumbs-directory
  THUMB_SIZE="256x256"
  IMG_PREFIX="pimg_"                    # prefix for all images
}

# --- write message to system log   -----------------------------------------

msg() {
  [ "$DEBUG" = "1" ] && logger -s -t "$SCRIPT" "$1"
}

# --- get next image-number   -----------------------------------------------

nextNumber() {
  local nFile="$IMAGE_ROOT/.currentNumber"
  declare -i cNum=-1

  # if we have a number, use it (else use default of -1)
  if [ -f "$nFile" ]; then
    cNum=$(cat "$nFile")
  fi

  # increment number, save and return new value
  let cNum+=1
  echo "$cNum" > "$nFile"
  echo "$IMG_PREFIX$(printf '%04g' $cNum)"
}

# --- get date of image   ----------------------------------------------------

getImageDate() {
  local d=$(gm identify -format '%[EXIF:DateTimeOriginal]' "$1" | \
                                                     cut -d" " -f1 | tr -d ':')
  if [ -n "$d" ]; then
    # exif date is available, so use it
    echo "$d"
  else
    # fallback to date of image-file
    date -r "$1" '+%Y%m%d'
  fi
}

# --- create thumbnail of a given image   ------------------------------------

createThumb() {
  local src="$IMAGE_ROOT/$1"
  local target="$THUMB_ROOT/$1"
  gm convert -size "$THUMB_SIZE" "$src" -resize "$THUMB_SIZE" \
                                                       +profile "*" "$target"
  chown "$DATA_OWNER" "$target"
}

