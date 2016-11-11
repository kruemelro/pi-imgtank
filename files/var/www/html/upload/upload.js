// ---------------------------------------------------------------------------
// JS support functions for file upload.
//
// Author: Bernhard Bablok
// License: GPL3
//
// Website: https://github.com/bablokb/pi-imgtank
//
// ---------------------------------------------------------------------------

/**
 * Create previews of files ready for upload
 */

function createPreviews(files) {
  for (var i = 0, f; f = files[i]; i++) {
    console.error("createPreview",f);
    var reader = new FileReader();
    reader.onload = (function (theFile) {
                       return function (e) {
                                // create thumbs
                                var thumb = document.createElement('img');
                                thumb.className = 'preview';
                                thumb.src = e.target.result;
                                thumb.title = theFile.name;
                                document.getElementById('previews').insertBefore(thumb,null);
                              };
                     })(f);
    // read image as data url
    reader.readAsDataURL(f);
  }
}

/**
 * Callback for file-selection change event
 */

function onChangeFileSelect(evt) {
  // reset preview area
  $('#previews').empty();

  // loop through all files
  var files = evt.target.files; // FileList object
  var msgok = "", msgerr = "";
  for (var i = 0, f; f = files[i]; i++) {
    // support only image files
    if (!f.type.match('image.*')) {
      msgerr += "<p class='msgerr'>" + f.name + ": Unsupported file type</p>";
    } else if (f.size > 20000000) {
      msgerr += "<p class='msgerr'>" + f.name + ": too large (limit is 20000000 bytes)</p>";
    } else {
      msgok += "<p class='msgok'>" + f.name + " (" + f.size +") ready for upload</p>";
    }
  }

  // either set error message or enable upload + create thumbs
  if (msgerr.length > 0) {
    $("#msgarea").html(msgerr);
  } else {
    $("#msgarea").html(msgok);
    $("#bt_sub").prop( "disabled",false);
    createPreviews(files);
  }
}

/**
 * Before upload (Reset progress indicator, disable button, clear previews)
 */

function beforeSend() {
    $('#bt_sub').prop( "disabled",true);
    $('progress').attr({value: 0, max: 100});
    $('#previews').empty();
}

/**
 * Callback for ajax upload (set message-area in case of success aka HTTP 200)
 */

function sendOk(data) {
  if (data.length > 0) {
    // console.log(data);
    var result = JSON.parse(data);
    $("#msgarea").html(result.msg);
  } else {
    $("#msgarea").html("<p class='msgerr'>Unknown failure.</p>");
  }
}

/**
 * Callback for ajax upload (set message-area in case of failure)
 */

function sendError(data) {
  // console.error(data);
    var result = JSON.parse(data.responseText);
    $("#msgarea").html(result.msg);
}

/**
 * Callback for progress indicator 
 */

function setProgress(e) {
    if (e.lengthComputable) {
        $('progress').attr({value: e.loaded, max: e.total});
    }
}
