<h1>Upload Your File</h1>
<form action="upload.php" method="post" enctype="multipart/form-data" class="upload-form">
    <input type="file" name="file" class="file-input" required accept=".jpg, .jpeg, .png, .gif">
    <button type="submit" class="upload-button">Upload</button>
</form>

<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $uploadDir = __DIR__ . '/uploads/';
    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0755, true);
    }

    $uploadedFile = $uploadDir . basename($_FILES['file']['name']);

    $allowedExtensions = ['jpg', 'jpeg', 'png', 'gif'];
    $fileExtension = strtolower(pathinfo($uploadedFile, PATHINFO_EXTENSION));

    if (in_array($fileExtension, $allowedExtensions)) {
        if (move_uploaded_file($_FILES['file']['tmp_name'], $uploadedFile)) {
            echo "<p class='success-message'>File uploaded successfully: <span>" . htmlspecialchars(basename($_FILES['file']['name'])) . "</span></p>";
        } else {
            echo "<p class='error-message'>Failed to upload file. Please try again.</p>";
        }
    } else {
        echo "<p class='error-message'>Invalid file type. Only images are allowed.</p>";
    }
}
?>
