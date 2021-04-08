<?php

const LEVEL = 2;
const ARG = 'author';
const QUERY = "SELECT * FROM books WHERE author LIKE '%<ARG>%'";

require('../app.php');
