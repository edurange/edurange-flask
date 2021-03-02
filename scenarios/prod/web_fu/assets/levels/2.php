<?php

// Payload: ' OR '1%'='1
//       => SELECT * FROM books WHERE title LIKE '%' OR '1%'='1%'

const LEVEL = 2;
const ARG = 'title';
const QUERY = "SELECT * FROM books WHERE title LIKE '%<ARG>%'";

require('../app.php');
