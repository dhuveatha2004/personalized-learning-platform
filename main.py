<?php
session_start();
ob_start();

$host = "localhost";
$user = "root";
$pass = "";
$dbname = "login_db";

$conn = mysqli_connect($host, $user, $pass, $dbname);
if (!$conn) die("Database Connection Failed: " . mysqli_connect_error());

if (!isset($_SESSION['user_name'])) $_SESSION['user_name'] = "Guest";

$checkColumn = mysqli_query($conn, "SELECT COLUMN_NAME FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = '$dbname' AND TABLE_NAME = 'users' AND COLUMN_NAME = 'first_login'");
if (mysqli_num_rows($checkColumn) == 0) {
    die("Error: 'first_login' column does not exist in the 'users' table.");
}

if (isset($_SESSION['user_id'])) {
    $user_id = $_SESSION['user_id'];
    mysqli_query($conn, "UPDATE users SET first_login = 0 WHERE id = '$user_id' AND first_login = 1");
}

$result = mysqli_query($conn, "SELECT COUNT(*) AS total FROM users WHERE first_login = 0");
if (!$result) die("Query Error: " . mysqli_error($conn));
$row = mysqli_fetch_assoc($result);
$logged_in_users = $row['total'];

$enrollment_count = isset($_SESSION['enrolled_courses']) ? count($_SESSION['enrolled_courses']) : 0;
$completed_count = isset($_SESSION['completed_courses']) ? count($_SESSION['completed_courses']) : 0;
$uploaded_count = isset($_SESSION['uploaded_assignments']) ? count($_SESSION['uploaded_assignments']) : 0;

mysqli_close($conn);
ob_end_flush();
?>

<!-- HTML Section -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Admin Dashboard</title>
  <link rel="icon" href="logo.jpg" type="image/x-icon">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- CSS styles skipped for brevity -->
</head>
<body>
  <div class="navbar">
    <a href="Admin_course.php">Course Upload</a>
    <a href="Admin_Videos.php">Upload Videos</a>
    <a href="Admin-Quiz.php">Upload Quiz</a>
    <a href="admin_assignment.php">Upload Assignment</a>
  </div>

  <div class="header">
    <h2>Admin Dashboard</h2>
    <img src="profile.jpg" alt="Profile" class="profile-img" onclick="togglePopup()">
  </div>
  <div class="popup" id="popup">Admin: <?php echo $_SESSION['user_name']; ?><br>Role: Super Admin</div>

  <div class="dashboard-container">
    <div class="stats-grid">
      <div class="small-card"><h3>Active Users</h3><p><?php echo $logged_in_users; ?></p></div>
      <div class="small-card"><h3>Total Users</h3><p><?php echo $logged_in_users; ?></p></div>
      <div class="small-card"><h3>Total Accounts</h3><p><?php echo $logged_in_users; ?></p></div>
      <div class="small-card"><h3>Total Views</h3><p><?php echo $logged_in_users; ?></p></div>
    </div>

    <div class="graphs">
      <div class="graph">
        <h3>Student Performance</h3>
        <canvas id="performanceChart" class="small-graph"></canvas>
      </div>
      <div class="graph">
        <h3>Student Activity</h3>
        <canvas id="activityChart" class="small-graph"></canvas>
      </div>
    </div>
  </div>

  <script>
    let enrolledCount = <?php echo $enrollment_count; ?>;
    let completedCount = <?php echo $completed_count; ?>;
    let visitCount = <?php echo $_SESSION['visit_count']; ?>;
    let uploadedCount = <?php echo $uploaded_count; ?>;

    new Chart(document.getElementById("performanceChart"), {
      type: 'line',
      data: {
        labels: ["Enrolled", "Completed"],
        datasets: [{
          label: "Courses",
          data: [enrolledCount, completedCount],
          borderColor: "#004080",
          backgroundColor: "rgb(255, 94, 217)",
          borderWidth: 3,
          fill: true,
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        scales: { y: { beginAtZero: true } }
      }
    });

    new Chart(document.getElementById("activityChart"), {
      type: 'pie',
      data: {
        labels: ["Active Visits"],
        datasets: [{
          data: [visitCount, 100 - visitCount],
          backgroundColor: ["#ffcc00", "#ddd"],
          hoverOffset: 4
        }]
      },
      options: { responsive: true, maintainAspectRatio: true }
    });
  </script>
</body>
</html>

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

<?php
session_start();
if (!isset($_SESSION['username'])) {
    header("Location: Main-Dashboard.php");
    exit();
}

if (!isset($_SESSION['selected_course'])) {
    $_SESSION['selected_course'] = "None";
}

if (isset($_POST['course'])) {
    $_SESSION['selected_course'] = $_POST['course'];
}

if (isset($_POST['reset'])) {
    $_SESSION['selected_course'] = "None";
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Web Development Course</title>
  <style>
    /* styles omitted for brevity */
  </style>
</head>
<body>
  <div class="container">
    <h1><?php echo $_SESSION['selected_course']; ?></h1>
    <div class="content">
      <div>
        <h2>Instructor: Lucifer</h2>
        <p>Advance your expertise with hands-on learning.</p>
        <button onclick="openPopup()">Enroll Now</button>
      </div>
      <img src="chatbot.jpg" alt="AI Upskilling" />
    </div>
  </div>

  <div class="overlay" id="overlay" onclick="closePopup()"></div>
  <div class="popup" id="popup">
    <form method="POST" action="course-Videos.php">
      <h3>Enter Your Details</h3>
      <input type="text" name="name" placeholder="Enter Name" required />
      <input type="date" name="date" required />
      <button type="submit" name="submit_form">Submit</button>
      <button type="button" onclick="closePopup()">Close</button>
    </form>
  </div>

  <script>
    function openPopup() {
      document.getElementById("popup").style.display = "block";
      document.getElementById("overlay").style.display = "block";
      setTimeout(() => {
        document.getElementById("popup").classList.add("show");
      }, 10);
    }

    function closePopup() {
      document.getElementById("popup").classList.remove("show");
      setTimeout(() => {
        document.getElementById("popup").style.display = "none";
        document.getElementById("overlay").style.display = "none";
      }, 400);
    }
  </script>
</body>
</html>

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


<!DOCTYPE html>
<html>
<head>
  <title>AI Chatbot</title>
</head>
<body>
  <h1>Ask the AI</h1>
  <form id="chatForm">
    <input type="text" id="question" placeholder="Type your question..." required>
    <button type="submit">Send</button>
  </form>
  <div id="response"></div>

  <script>
    document.getElementById("chatForm").addEventListener("submit", async function (event) {
      event.preventDefault();
      const question = document.getElementById("question").value;
      const res = await fetch("http://127.0.0.1:5000/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
      });
      const data = await res.json();
      document.getElementById("response").innerText = data.answer || "No response from bot.";
    });
  </script>
</body>
</html>

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

<?php
// Simplified logic
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $question = $_POST['question'];
    $answer = $_POST['answer'];
    // Save to database
}
?>
<form method="POST">
  <input type="text" name="question" placeholder="Enter Question">
  <input type="text" name="answer" placeholder="Correct Answer">
  <button type="submit">Add Quiz</button>
</form>

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

CREATE DATABASE IF NOT EXISTS login_db;
USE login_db;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) NOT NULL,
  password VARCHAR(255) NOT NULL,
  first_login BOOLEAN DEFAULT 1
);

CREATE DATABASE IF NOT EXISTS course_list;
USE course_list;

CREATE TABLE Admin_course (
  id INT AUTO_INCREMENT PRIMARY KEY,
  course_name VARCHAR(255) UNIQUE NOT NULL,
  Instructor_name VARCHAR(255) NOT NULL,
  description TEXT NOT NULL
);

