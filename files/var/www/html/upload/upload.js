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
 * Reset progress indicator
 */

function resetProgress() {
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
