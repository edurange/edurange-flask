<?php

$fp = fopen('../log.csv', 'a');

// user_id,level,input,output,error,timestamp
fputcsv($fp, array(
    $_COOKIE['session'],
    $level,
    addslashes($input),
    addslashes(json_encode($results)),
    str_replace("\n", "\\n", isset($error) ? $error : 'NULL'),
    date('c'),
));

fclose($fp);
