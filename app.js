function startProcess() {
    const file = document.getElementById('fileUpload').files[0];
    if (!file) {
        alert('Please upload an image or PDF file.');
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    // Use the Render or Heroku backend URL here
    const backendUrl = "https://your-app-name.onrender.com/upload";

    document.getElementById("progress").innerHTML = "Uploading and processing file...";

    fetch(backendUrl, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("progress").innerHTML = "Processing complete!";
        document.getElementById("extractedText").innerText = data.text;

        // Highlight visible alphabets
        let alphabetHTML = '';
        for (let charCode = 97; charCode <= 122; charCode++) {
            let char = String.fromCharCode(charCode);
            if (data.visible_alphabets.includes(char)) {
                alphabetHTML += `<span class="highlighted">${char.toUpperCase()}</span> `;
            } else {
                alphabetHTML += `<span>${char.toUpperCase()}</span> `;
            }
        }
        document.getElementById("visibleAlphabets").innerHTML = alphabetHTML;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById("progress").innerHTML = "An error occurred during processing.";
    });
}
