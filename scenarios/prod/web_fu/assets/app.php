<?php

// The session cookie is set by EDURange; since it's under the same domain we leverage it
if (!isset($_COOKIE['session']) || $_COOKIE['session'] == '') {
    http_response_code(403);
    die('Please login to EDURange to access WebFu.');
}

$count = 0;
$results = [];
$input = $method == 'GET' ? $_GET[$param] : $_POST[$param];
$level = explode('.', basename($_SERVER['REQUEST_URI']))[0];

if (isset($input) && $input != '') {
    require('db.php');
    $c = 0;
    try {
        $rows = $pdo->query(str_replace('<INPUT>', $input, $query));

        foreach ($rows as $row) {
            $data = [];
            foreach ($row as $col => $val) {
                // Only add key-value pairs (e.g., "id"), skipping array indexes (e.g., 0)
                if ($c % 2 == 0)
                    $data[$col] = $val;
        
                $c++;
            }
    
            // Convert PDO statement to plain array
            array_push($results, $data);
            $count++;
        }
    } catch (Exception $e) {
        $error = $e;
    }
}

require('logging.php');
require("views/$level.php");
