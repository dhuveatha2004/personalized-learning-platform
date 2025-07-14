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
