<?php

require('../auth.php');

$level = 6;
$input = isset($_GET['image_url'])
  ? $_GET['image_url']
  : 'https://edurange.watzek.cloud:8443/res/profile.png';

// TODO: add more possible payloads (JS events, i.e., onXXXX)
// TODO: improve injection detection by using regexp or parsing payload (check for valid JS).
$exploited = false;
if (strpos($input, 'onerror=') !== false || strpos($input, 'onmouseover=') !== false)
  $exploited = true;

require('../logging.php');

?>

<!DOCTYPE html>
<html>
<?php require('../views/header.php'); ?>

<body class="bg-dark">
  <div class="container pt-4 text-white">
    <div class="d-flex justify-content-between mt-5 mb-3">
      <h3>Profile picture</h3>
      <img alt="Profile picture" src=<?= $input; ?> height="100" width="100"/>
    </div>

    <form action method="GET">
      <input name="image_url" class="form-control" placeholder="New profile pic" required></input>
      <button type="submit" class="btn btn-info fs-5 mt-2 px-4 py-2">Update profile picture</button>
    </form>

    <?php if($exploited): ?>
    <pre class="border border-success mt-5 p-3">Congrats! Here is your flag: FLAG{0NSUCC3SS_4L3R7(PWN)}</pre>
    <?php else: ?>
    <pre class="border border-danger mt-5 p-3">No flag for you :(</pre>
    <?php endif; ?>
  </div>
</body>
</html>
