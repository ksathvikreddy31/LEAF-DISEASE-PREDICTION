document.getElementById('uploadButton').addEventListener('click', function () {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        alert("Please upload an image.");
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    // Show loading message
    document.getElementById('result').classList.add('hidden');
    document.getElementById('predictionText').innerText = 'Loading...';

    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').classList.remove('hidden');
        document.getElementById('predictionText').innerText = `Detected Disease: ${data.disease} with ${data.confidence}% confidence.`;
        document.getElementById('uploadedImage').src = URL.createObjectURL(file);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('predictionText').innerText = 'An error occurred. Please try again.';
    });
});
