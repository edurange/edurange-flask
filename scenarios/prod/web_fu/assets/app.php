<?php

require('config.php');

$results = [];

if (isset($_GET[ARG]) && $_GET[ARG] != '') {
    $pdo = new PDO(DB_DSN, DB_USER, DB_PASSWORD);
    $results = $pdo->query( str_replace('<ARG>', $_GET[ARG], QUERY) );
}

require('views/' . LEVEL . '.php');
