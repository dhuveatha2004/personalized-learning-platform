<?php
session_start();

$host = "localhost";
$user = "root";
$pass = "";
$dbname = "course_list";

$conn = mysqli_connect($host, $user, $pass, $dbname);
if (!$conn) die("Database connection failed: " . mysqli_connect_error());

$create_table = "CREATE TABLE IF NOT EXISTS Admin_course (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL UNIQUE,
    Instructor_name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL
)";
mysqli_query($conn, $create_table);

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $course_name = mysqli_real_escape_string($conn, $_POST['course_name']);
    $instructor_name = mysqli_real_escape_string($conn, $_POST['instructor_name']);
    $description = mysqli_real_escape_string($conn, $_POST['description']);

    if (!empty($course_name) && !empty($instructor_name) && !empty($description)) {
        $insert_query = "INSERT IGNORE INTO Admin_course (course_name, Instructor_name, description)
            VALUES ('$course_name', '$instructor_name', '$description')";
        if (mysqli_query($conn, $insert_query)) {
            echo "<script>alert('Course added successfully!'); window.location.href='';</script>";
        } else {
            echo "<script>alert('Error adding course!');</script>";
        }
    } else {
        echo "<script>alert('All fields are required!');</script>";
    }
}

$result = mysqli_query($conn, "SELECT DISTINCT course_name FROM Admin_course ORDER BY id DESC");
mysqli_close($conn);
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Course Management</title>
  <style>
    /* styles omitted for brevity */
  </style>
</head>
<body>
  <div class="course-list-container">
    <h2>Courses Added:</h2>
    <div class="course-list">
      <?php
      while ($row = mysqli_fetch_assoc($result)) {
          echo "<div class='course-item'>" . htmlspecialchars($row['course_name']) . "</div>";
      }
      ?>
    </div>
  </div>

  <div class="container">
    <h1>Add New Course</h1>
    <form method="POST" onsubmit="return validateForm()">
      <input type="text" name="course_name" id="course_name" placeholder="Enter Course Name" required />
      <input type="text" name="instructor_name" id="instructor_name" placeholder="Enter Instructor Name" required />
      <textarea name="description" id="description" rows="3" placeholder="Enter Course Description" required></textarea>
      <button type="submit">Add Course</button>
    </form>
  </div>

  <script>
    function validateForm() {
      let name = document.getElementById("course_name").value;
      let instructor = document.getElementById("instructor_name").value;
      let desc = document.getElementById("description").value;
      if (name.trim() === "" || instructor.trim() === "" || desc.trim() === "") {
        alert("All fields are required!");
        return false;
      }
      return true;
    }
  </script>
</body>
</html>
