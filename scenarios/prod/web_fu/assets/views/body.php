<body>
  <div class="container mt-4">
    <h2><?= $title ?></h2>
    <form method=<?= $method ?>>
      <div class="row mb-4 g-3 align-items-center">
        <div class="col-4">
          <input type="text" name=<?= ARG ?> class="form-control" placeholder=<?= $placeholder ?>>
        </div>
        <div class="col-auto">
          <button type="submit" class="btn btn-success">Search</button>
        </div>
      </div>
    </form>

    <h2>Query results</h2>
    <table class="table">
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
  </div>
</body>
