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
        $base_esc = htmlspecialchars(($base));
        $target_file = $target_dir . $base;
        $imageFileType = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));

// Check if image file is a actual image or fake image
        $check = getimagesize($file["tmp_name"]);
        if ($check === TRUE) {
            $status = "error";
            $msg = "$msg<div class='upload_msgerr'>File $base_esc is not an image.</div><br>";
            http_response_code(412);
            continue;
        }
// Check if file already exists
        if (file_exists($target_file)) {
            $status = "error";
            $msg = "$msg<div class='upload_msgerr'>File $base_esc already exists.</div><br>";
            http_response_code(412);
            continue;
        }
// Check file size
        if ($file["size"] > 20000000) {
            $status = "error";
            $msg = "$msg<div class='upload_msgerr'>File $base_esc is too large.</div><br>";
            http_response_code(412);
            continue;
        }
// Allow certain file formats
        if ($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg" && $imageFileType != "gif") {
            $status = "error";
            $msg = "$msg<div class='upload_msgerr'>File $base_esc is neither JPG, JPEG, PNG or GIF.</div><br>";
            http_response_code(412);
            continue;
        }

        if (move_uploaded_file($file["tmp_name"], $target_file)) {
            $msg = "$msg<div class='upload_msgok'>File $base_esc has been uploaded.</div><br>";
        } else {
            $status = "error";
            $msg = "$msg<div class='upload_msgerr'>Error while uploading file $base_esc.</div><br>";
            http_response_code(500);
        }
    }
    echo '{"status": "' . $status . '" ,"msg": "' . $msg . '"}';
}
?>