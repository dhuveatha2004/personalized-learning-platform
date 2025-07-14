<?php
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_FILES["video"])) {
    $upload_dir = "static/videos/";
    $file_name = basename($_FILES["video"]["name"]);
    $target_file = $upload_dir . $file_name;

    if (move_uploaded_file($_FILES["video"]["tmp_name"], $target_file)) {
        echo "Video uploaded successfully!";
    } else {
        echo "Error uploading video.";
    }
}
?>
<form method="POST" enctype="multipart/form-data">
  <label>Upload Video:</label>
  <input type="file" name="video" required>
  <button type="submit">Upload</button>
</form>
