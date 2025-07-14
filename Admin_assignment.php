<?php
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_FILES["assignment"])) {
    $upload_dir = "uploads/assignments/";
    $file_name = basename($_FILES["assignment"]["name"]);
    $target_file = $upload_dir . $file_name;

    if (move_uploaded_file($_FILES["assignment"]["tmp_name"], $target_file)) {
        echo "Assignment uploaded successfully!";
    } else {
        echo "Upload failed.";
    }
}
?>
<form method="POST" enctype="multipart/form-data">
  <label>Upload Assignment:</label>
  <input type="file" name="assignment" required>
  <button type="submit">Upload</button>
</form>
