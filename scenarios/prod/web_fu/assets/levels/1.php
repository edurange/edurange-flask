<?php

// Payload: ' OR '1'='1
//       => SELECT * FROM books WHERE name='' OR '1'='1'

const LEVEL = 1;
const ARG = 'name';
const QUERY = "SELECT * FROM countries WHERE name='<ARG>'";

require('../app.php');
