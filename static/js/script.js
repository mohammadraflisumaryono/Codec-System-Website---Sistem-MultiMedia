function toggleCompressionLevel() {
    const action = document.getElementById('action').value;
    const compressionLevelWrapper = document.getElementById('compressionLevelWrapper');
    compressionLevelWrapper.classList.toggle('hidden', action !== 'compress');
}

async function processFile() {
    const fileInput = document.getElementById('fileInput');
    const mediaType = document.getElementById('mediaType').value;
    const action = document.getElementById('action').value;
    const compressionLevel = document.getElementById('compressionLevel').value;
    const file = fileInput.files[0];
    const preview = document.getElementById('preview');
    const output = document.getElementById('output');
    const progress = document.getElementById('progress');
    const progressBar = document.querySelector('.progress-bar');

    if (!file) {
        output.innerHTML = '<p class="error">Please select a file</p>';
        return;
    }

    preview.innerHTML = '';
    output.innerHTML = '';
    progress.classList.add('visible');
    progressBar.style.width = '0%';

    // Preview file
    const url = URL.createObjectURL(file);
    if (mediaType === 'image') {
        const img = document.createElement('img');
        img.src = url;
        preview.appendChild(img);
    } else if (mediaType === 'audio') {
        const audio = document.createElement('audio');
        audio.src = url;
        audio.controls = true;
        preview.appendChild(audio);
    } else if (mediaType === 'video') {
        const video = document.createElement('video');
        video.src = url;
        video.controls = true;
        video.width = 320;
        preview.appendChild(video);
    }

    // Simulate progress
    let progressValue = 0;
    const progressInterval = setInterval(() => {
        progressValue += 10;
        progressBar.style.width = `${progressValue}%`;
        if (progressValue >= 80) clearInterval(progressInterval);
    }, 200);

    // Send file to server
    const formData = new FormData();
    formData.append('file', file);
    formData.append('media_type', mediaType);
    formData.append('action', action);
    if (action === 'compress') {
        formData.append('compression_level', compressionLevel);
    }

    try {
        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();

        clearInterval(progressInterval);
        progressBar.style.width = '100%';
        setTimeout(() => progress.classList.remove('visible'), 500);

        if (response.ok) {
            output.innerHTML = `<p>${result.message}</p><a href="${result.file}" download>Download Result</a>`;
        } else {
            output.innerHTML = `<p class="error">${result.error}</p>`;
        }
    } catch (error) {
        clearInterval(progressInterval);
        progressBar.style.width = '100%';
        setTimeout(() => progress.classList.remove('visible'), 500);
        output.innerHTML = `<p class="error">Error processing file: ${error.message}</p>`;
    }
}

// Initialize compression level visibility
document.addEventListener('DOMContentLoaded', toggleCompressionLevel);