<?php

$title = 'Library lookup';
$method = 'GET';
$placeholder = 'Search by author (e.g. Huxley, Tolkien, etc.)...';
$fields = [
  '#'      => 'id',
  'Title'  => 'title',
  'Author' => 'author',
  'Year'   => 'year'
];

require('main.php');
