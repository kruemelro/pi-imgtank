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
 * Callback for file-selection change event
 */

function onChangeFileSelect(evt) {
  console.error("onChangeFileSelect",evt);
  var files = evt.target.files; // FileList object
  var msgok = "", msgerr = "";
  for (var i = 0, f; f = files[i]; i++) {
    // support only image files
    if (!f.type.match('image.*')) {
      msgerr += "<p class='msgerr'>" + f.name + ": Unsupported file type</p>";
      continue;
    } else {
      msgok += "<p class='msgok'>" + f.name + " (" + f.size +") ready for upload</p>";
    }
  }
  if (msgerr.length > 0) {
    $("#msgarea").html(msgerr);
  } else {
    $("#msgarea").html(msgok);
    $("#bt_sub").prop( "disabled",false);
  }
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
 * Before upload (Reset progress indicator, disable button)
 */

function beforeSend() {
    $("#bt_sub").prop( "disabled",true);
    $('progress').attr({value: 0, max: 100});
}

/**
 * Callback for progress indicator 
 */

function setProgress(e) {
    if (e.lengthComputable) {
        $('progress').attr({value: e.loaded, max: e.total});
    }
}
