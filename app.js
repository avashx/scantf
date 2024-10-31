function uploadFile() {
    const fileInput = document.getElementById('fileUpload');
    const file = fileInput.files[0];

    if (!file) {
        alert("Please upload an image or PDF.");
        return;
    }

    // Show file preview if it's an image
    const preview = document.getElementById('uploadedImage');
    if (file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = "block";
        };
        reader.readAsDataURL(file);
    }

    const formData = new FormData();
    formData.append("file", file);

    document.getElementById("progress").innerHTML = "Processing file...";

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("progress").innerHTML = "Processing complete!";
        
        // Update alphabetic character count
        const alphabetCountList = document.getElementById("alphabetCount");
        alphabetCountList.innerHTML = "";
        for (const [char, count] of Object.entries(data.alphabet_count)) {
            alphabetCountList.innerHTML += `<li>${char.toUpperCase()}: ${count}</li>`;
        }

        // Display cropped alphabet images
        const croppedImagesContainer = document.getElementById("croppedImagesContainer");
        croppedImagesContainer.innerHTML = "";
        for (const [char, imagePath] of Object.entries(data.alphabet_images)) {
            const img = document.createElement("img");
            img.src = imagePath;
            img.alt = char;
            img.title = char.toUpperCase();
            croppedImagesContainer.appendChild(img);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById("progress").innerHTML = "An error occurred during processing.";
    });
}
