<?php

// The session cookie is set by EDURange; since it's under the same domain we leverage it
if (!isset($_COOKIE['session']) || $_COOKIE['session'] == '') {
  http_response_code(403);
  die('Please login to EDURange to access WebFu.');
}
