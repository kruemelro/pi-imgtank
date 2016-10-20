<?php
// ---------------------------------------------------------------------------
// Server-side processing of file uploads.
//
// WARNING: upload-scripts are always dangerous. This code has not been
//          audited, use at your own risk!!
//
// Origin of the code
//  * W3Schools     (basic processing)
//  * PHP manual    (reordering of $_FILES)
//  * own additions (messages, responsse codes)
//
// Author: Bernhard Bablok
// License: GPL3
//
// Website: https://github.com/bablokb/pi-imgtank
//
// ---------------------------------------------------------------------------


function reorderArrayFiles(&$file_post) {

    $file_ary = array();
    $file_count = count($file_post['name']);
    $file_keys = array_keys($file_post);

    for ($i = 0; $i < $file_count; $i++) {
        foreach ($file_keys as $key) {
            $file_ary[$i][$key] = $file_post[$key][$i];
        }
    }

    return $file_ary;
}

$target_dir = "/data/uploads/";

if ($_FILES['fileToUpload']) {
    $file_ary = reorderArrayFiles($_FILES['fileToUpload']);
    $status = "ok";
    $msg = "";
    foreach ($file_ary as $file) {

        $base = basename($file["name"]);
        $target_file = $target_dir . $base;
        $imageFileType = pathinfo($target_file, PATHINFO_EXTENSION);

// Check if image file is a actual image or fake image
        $check = getimagesize($file["tmp_name"]);
        if ($check === TRUE) {
            $status = "error";
            $msg = "$msg<p class='msgerr'>File $base is not an image.</p>";
            http_response_code(412);
            continue;
        }
// Check if file already exists
        if (file_exists($target_file)) {
            $status = "error";
            $msg = "$msg<p class='msgerr'>File $base already exists.</p>";
            http_response_code(412);
            continue;
        }
// Check file size
        if ($file["size"] > 5000000) {
            $status = "error";
            $msg = "$msg<p class='msgerr'>File $base is too large.</p>";
            http_response_code(412);
            continue;
        }
// Allow certain file formats
        if ($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg" && $imageFileType != "gif") {
            $status = "error";
            $msg = "$msg<p class='msgerr'>File $base is neither JPG, JPEG, PNG or GIF.</p>";
            http_response_code(412);
            continue;
        }

        if (move_uploaded_file($file["tmp_name"], $target_file)) {
            $msg = "$msg<p class='msgok'>File $base has been uploaded.</p>";
        } else {
            $status = "error";
            $msg = "$msg<p class='msgerr'>Error while uploading file $base.</p>";
            http_response_code(500);
        }
    }
    echo '{"status": "' . $status . '" ,"msg": "' . $msg . '"}';
}
?>