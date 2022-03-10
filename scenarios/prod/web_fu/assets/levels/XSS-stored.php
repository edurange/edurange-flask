<?php

// The session cookie is set by EDURange; since it's under the same domain we leverage it
if (!isset($_COOKIE['session']) || $_COOKIE['session'] == '') {
    http_response_code(403);
    die('Please login to EDURange to access WebFu.');
}

require('../db.php');

$level = 5;
$exploited = false;

// Insert the user's comment into database.
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['comment']) && $_POST['comment'] !== "") {
  $input = $_POST['comment'];

  try {
    $pdo->query("INSERT INTO comments (text) VALUES (\"$input\")");  // So exploitable.
  } catch (Exception $e) {
    echo $e;
  }

  // TODO: improve injection detection by using regexp
  if(strpos($input, '<script>') !== false and strpos($input, '</script>') !== false) {
    $exploited = true;
  }

  require('../logging.php');  // Only log if there is user input.
}

$c = 0;
$results = [];
$fields = [
  '#'       => 'id',
  'Text' => 'text',
];

// NOTE: perhaps we want to filter comments by author (random seed stored in cookie).
//       This way users cannot exploit each other.
$rows = $pdo->query("SELECT * FROM comments");

// Get all the comments.
foreach ($rows as $row) {
  $data = [];
  foreach ($row as $col => $val) {
    // Only add key-value pairs (e.g., "id"), skipping array indexes (e.g., 0)
    if ($c % 2 == 0)
      $data[$col] = $val;

    $c++;
  }

  array_push($results, $data);  // Convert PDO statement to plain array
}

?>

<!DOCTYPE html>
<html>
<?php require('../views/header.php'); ?>

<body class="bg-dark">
  <div class="container pt-4 text-white">
    <h2 class="mt-5 mb-3">Hi 👋 </h2>
    <form action method="POST">
      <textarea name="comment" class="form-control" placeholder="Got anything to say? Comment here!" rows="3" required></textarea>
      <div class="d-grid">
        <button type="submit" class="btn btn-info fs-5 mt-2 px-4 py-2">Post</button>
      </div>
    </form>

    <h2 class="mt-4 mb-2 pt-1">Comments 🗣</h2>
    <table class="table table-dark">
      <thead>
        <tr>
          <?php foreach ($fields as $field => $column): ?>
          <th scope="col"><?= $field ?></th>
          <?php endforeach ?>
        </tr>
      </thead>
      <tbody>
        <?php foreach ($results as $row): ?>
        <tr>
          <?php foreach ($fields as $field => $column): ?>
          <td><?= $row[$column] ?></td>
          <?php endforeach ?>
        </tr>
        <?php endforeach ?>
      </tbody>
    </table>

    <?php if($exploited): ?>
    <pre class="border border-success mt-5 p-3">Congrats! Here is your flag: FLAG{P4YL04D_1NJ3CT3D}</pre>
    <?php else: ?>
    <pre class="border border-danger mt-5 p-3">No flag for you :(</pre>
    <?php endif; ?>
  </div>
</body>
</html>
