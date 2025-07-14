<?php
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit();
}

$_SESSION['selected_course'] = $_SESSION['selected_course'] ?? "None";

if ($_SERVER["REQUEST_METHOD"] == "POST" && !empty($_POST['course'])) {
    $_SESSION['selected_course'] = htmlspecialchars($_POST['course']);
    header("Location: courses.php");
    exit();
}

$conn = new mysqli("localhost", "root", "", "course_list");
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Course Page</title>
  <style>
    /* styles omitted for brevity */
  </style>
</head>
<body>
  <div class="container">
    <header class="header">
      <h1>Welcome to Course Page</h1>
      <p>Selected Course: <span class="selected-course"><?php echo $_SESSION['selected_course']; ?></span></p>
    </header>

    <div class="course-container">
      <?php
      $sql = "SELECT DISTINCT course_name, description, Instructor_name FROM Admin_course";
      $result = $conn->query($sql);

      if ($result->num_rows > 0) {
          while ($row = $result->fetch_assoc()) {
              echo "<div class='course-card'>
                  <h3>" . htmlspecialchars($row['course_name']) . "</h3>
                  <p class='course-description'>" . htmlspecialchars($row['description']) . "</p>
                  <p class='instructor-name'>Instructor: " . htmlspecialchars($row['Instructor_name']) . "</p>
                  <form method='POST' action='courses.php'>
                      <input type='hidden' name='course' value='" . htmlspecialchars($row['course_name']) . "'>
                      <button type='submit'>Resume Course</button>
                  </form>
              </div>";
          }
      } else {
          echo "<p>No courses available.</p>";
      }
      $conn->close();
      ?>
    </div>
  </div>
</body>
</html>
