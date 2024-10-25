<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Image Gallery</title>
    <style>
        /* Basic styling for the body */
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f7f7f7;
            margin: 0;
        }

        /* Container for the gallery */
        .gallery-container {
            text-align: center;
            max-width: 800px;
        }

        /* Styling for the gallery title */
        h1 {
            margin-bottom: 20px;
            color: #333;
        }

        /* Thumbnail styling */
        .gallery-thumbnails {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }

        .thumbnail {
            width: 100px;
            height: 100px;
            margin: 0 10px;
            cursor: pointer;
            transition: transform 0.3s ease;
        }

        .thumbnail:hover {
            transform: scale(1.1);
        }

        /* Styling for the displayed image */
        .image-display img {
            width: 400px;
            height: 400px;
            object-fit: cover;
            border: 3px solid #ccc;
        }
    </style>
</head>
<body>
    <div class="gallery-container">
        <h1>Simple Image Gallery</h1>

        <!-- Thumbnails -->
        <div class="gallery-thumbnails">
            <img src="https://via.placeholder.com/100" alt="Image 1" class="thumbnail" onclick="openImage('https://via.placeholder.com/400')">
            <img src="https://via.placeholder.com/100" alt="Image 2" class="thumbnail" onclick="openImage('https://via.placeholder.com/400/ff0000')">
            <img src="https://via.placeholder.com/100" alt="Image 3" class="thumbnail" onclick="openImage('https://via.placeholder.com/400/00ff00')">
        </div>

        <!-- Displayed Image -->
        <div class="image-display">
            <img id="displayedImage" src="https://via.placeholder.com/400" alt="Displayed Image">
        </div>
    </div>

    <script>
        // Function to display the clicked thumbnail as the main image
        function openImage(imagePath) {
            const displayedImage = document.getElementById('displayedImage');
            displayedImage.src = imagePath;
        }
    </script>
</body>
</html>
