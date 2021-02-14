<?php
  $title = 'Country lookup';
  $method = 'GET';
  $placeholder = 'Search by country name (e.g. Portugal)...';
  $fields = [
    '#'            => 'id',
    'Name'         => 'name',
    'Country code' => 'code'
  ];

  require('main.php');
