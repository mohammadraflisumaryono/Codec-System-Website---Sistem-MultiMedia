function toggleCompressionLevel() {
    const action = document.getElementById('action').value;
    const compressionLevelWrapper = document.getElementById('compressionLevelWrapper');
    const messageWrapper = document.getElementById('messageWrapper');
    compressionLevelWrapper.classList.toggle('hidden', action !== 'compress');
    messageWrapper.classList.toggle('hidden', action !== 'embed');
}

function toggleOptions() {
    const mediaType = document.getElementById('mediaType').value;
    const actionSelect = document.getElementById('action');
    actionSelect.innerHTML = `
        <option value="compress">Compress</option>
        <option value="decompress">Decompress</option>
        ${mediaType === 'image' ? `
            <option value="embed">Embed Message</option>
            <option value="extract">Extract Message</option>
        ` : ''}
    `;
    toggleCompressionLevel();
}

function displayPreview(file, elementId, mediaType) {
    const element = document.getElementById(elementId);
    element.innerHTML = '';
    const url = file instanceof File ? URL.createObjectURL(file) : file;
    if (mediaType === 'image') {
        const img = document.createElement('img');
        img.src = url;
        img.onerror = () => {
            element.innerHTML = '<p class="error">Failed to load preview</p>';
        };
        element.appendChild(img);
    } else if (mediaType === 'audio') {
        const audio = document.createElement('audio');
        audio.src = url;
        audio.controls = true;
        element.appendChild(audio);
    } else if (mediaType === 'video') {
        const video = document.createElement('video');
        video.src = url;
        video.controls = true;
        video.width = 200;
        element.appendChild(video);
    }
}

async function processFile() {
    const fileInput = document.getElementById('fileInput');
    const mediaType = document.getElementById('mediaType').value;
    const action = document.getElementById('action').value;
    const compressionLevel = document.getElementById('compressionLevel').value;
    const message = document.getElementById('messageInput').value;
    const file = fileInput.files[0];
    const inputPreview = document.getElementById('inputPreview');
    const outputPreview = document.getElementById('outputPreview');
    const output = document.getElementById('output');
    const progress = document.getElementById('progress');
    const progressBar = document.querySelector('.progress-bar');

    if (!file) {
        output.innerHTML = '<p class="error">Please select a file</p>';
        return;
    }

    if (action === 'embed' && !message) {
        output.innerHTML = '<p class="error">Please enter a message to embed</p>';
        return;
    }

    outputPreview.innerHTML = '';
    output.innerHTML = '';
    progress.classList.add('visible');
    progressBar.style.width = '0%';

    // Display input preview
    displayPreview(file, 'inputPreview', mediaType);

    // Validate message length for embed
    if (action === 'embed') {
        const img = new Image();
        img.src = URL.createObjectURL(file);
        img.onload = async () => {
            const maxChars = Math.floor((img.width * img.height * 3) / 8) - 3;
            if (message.length > maxChars) {
                output.innerHTML = `<p class="error">Message too long. Max ${maxChars} characters.</p>`;
                progress.classList.remove('visible');
                return;
            }
            await sendFile(file, mediaType, action, compressionLevel, message, output, outputPreview, progress, progressBar);
        };
        img.onerror = () => {
            output.innerHTML = '<p class="error">Failed to load image for validation</p>';
            progress.classList.remove('visible');
        };
    } else {
        await sendFile(file, mediaType, action, compressionLevel, message, output, outputPreview, progress, progressBar);
    }
}

async function sendFile(file, mediaType, action, compressionLevel, message, output, outputPreview, progress, progressBar) {
    let progressValue = 0;
    const progressInterval = setInterval(() => {
        progressValue += 10;
        progressBar.style.width = `${progressValue}%`;
        if (progressValue >= 80) clearInterval(progressInterval);
    }, 200);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('media_type', mediaType);
    formData.append('action', action);
    if (action === 'compress') {
        formData.append('compression_level', compressionLevel);
    }
    if (action === 'embed') {
        formData.append('message', message);
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
            if (action === 'extract') {
                output.innerHTML = `<p class="extracted-message">Extracted Message: ${result.message}</p>`;
            } else {
                output.innerHTML = `<p>${result.message}</p><a href="${result.file}" download>Download Result</a>`;
                if (mediaType === 'image' && result.file) {
                    setTimeout(async () => {
                        try {
                            const outputFile = await fetch(result.file);
                            if (!outputFile.ok) {
                                outputPreview.innerHTML = '<p class="error">Failed to load output preview</p>';
                                return;
                            }
                            const blob = await outputFile.blob();
                            displayPreview(URL.createObjectURL(blob), 'outputPreview', mediaType);
                        } catch (error) {
                            outputPreview.innerHTML = '<p class="error">Error loading output preview</p>';
                        }
                    }, 500);
                }
            }
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

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    toggleCompressionLevel();
    toggleOptions();
});