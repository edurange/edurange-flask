<?php

require('../auth.php');

session_start();

$level = 4;
$_SESSION["counter"] += 1;
$input = isset($_GET['name']) ? $_GET['name'] : 'stranger';  // pwned

// TODO: improve injection detection by using regexp
$exploited = false;
if (strpos($input, '<script>') !== false and strpos($input, '</script>') !== false)
  $exploited = true;

require('../logging.php');

?>

<!DOCTYPE html>
<html>
<?php require('../views/header.php'); ?>

<!-- TODO: add form so user doesn't need to add parameter manually. -->
<body class="bg-dark">
  <div class="container pt-4 text-white">
    <h2 class="mt-5">Hello, <?= $input; ?>.</h2>

    <pre class="border border-info mt-5 p-3">You have visited this page <?= $_SESSION["counter"]; ?> times.</pre>

    <?php if($exploited): ?>
    <pre class="border border-success mt-3 p-3">Congrats! Here is your flag: FLAG{4LW4Y5_54N71Z3_1NPU7}</pre>
    <?php else: ?>
    <pre class="border border-danger mt-3 p-3">No flag for you :(</pre>
    <?php endif; ?>
  </div>
  <!-- NOTE: cGFyYW1ldGVyIGBuYW1lYCBpcyBhbHJlYWR5IHdvcmtpbmcu -->
</body>
</html>
