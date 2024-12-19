<?php
$baseDir = realpath(__DIR__);
$page = isset($_GET['page']) ? $_GET['page'] : 'home.php';


$page = preg_replace('/[^a-zA-Z0-9\/\._-]/', '', $page);


$filePath = realpath($baseDir . '/' . $page);


include 'includes/header.php';


if ($filePath && strpos($filePath, $baseDir) === 0 && is_file($filePath)) {
    include($filePath);
} else {
    echo "<p>Page not found or access denied!</p>";
}


include 'includes/footer.php';
?>
