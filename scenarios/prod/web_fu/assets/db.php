<?php

const DB_DSN = 'mysql:host=127.0.0.1;dbname=WebFu';
const DB_USER = 'root';
const DB_PASSWORD = '';

$pdo = new PDO(DB_DSN, DB_USER, DB_PASSWORD);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
