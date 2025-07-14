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
