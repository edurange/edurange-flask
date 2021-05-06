<?php

$method = 'GET';
$param = 'author';
$query = "SELECT * FROM books WHERE author LIKE '%<INPUT>%'";

require('../app.php');
