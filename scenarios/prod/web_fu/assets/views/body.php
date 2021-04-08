<body class="bg-dark">
  <div class="container pt-4 text-white">
    <h2><?= $title ?></h2>
    <form method="<?= $method ?>">
      <div class="row g-3 mb-4">
        <div class="col-6">
          <input type="text" name="<?= ARG ?>" class="form-control" placeholder="<?= $placeholder ?>">
        </div>
        <div class="col">
          <button type="submit" class="btn btn-success">Search</button>
        </div>
      </div>
    </form>

    <div class="row">
      <h3 class="col">Query results</h3>
      <p class="col" style="text-align: right;">Returned <b><?= $count ?> hits</b></p>
    </div>
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
  </div>
</body>
