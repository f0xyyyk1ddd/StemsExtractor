const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const processSection = document.getElementById('process-section');
const resultsSection = document.getElementById('results-section');
const stemsList = document.getElementById('stems-list');
const progressBar = document.getElementById('progress-bar');
const percentText = document.getElementById('percent-text');
const statusText = document.getElementById('status-text');
const stemOptions = document.querySelectorAll('.stem-option');
const resetBtn = document.getElementById('reset-btn');

let selectedStems = 2;

// Handle Stem Selection
stemOptions.forEach(btn => {
    btn.addEventListener('click', () => {
        stemOptions.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedStems = btn.dataset.stems;
    });
});

// Drag & Drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        handleFile(fileInput.files[0]);
    }
});

async function handleFile(file) {
    if (!file.type.startsWith('audio/')) {
        alert('Пожалуйста, загрузите аудиофайл.');
        return;
    }

    // UI Updates
    dropZone.classList.add('hidden');
    document.querySelector('.options-section').classList.add('hidden');
    processSection.classList.remove('hidden');

    // Upload & Process
    const formData = new FormData();
    formData.append('file', file);
    formData.append('stems', selectedStems);

    statusText.innerText = 'Загрузка и обработка...';
    simulateProgress();

    try {
        const response = await fetch('/api/separate', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.status === 'success') {
            showResults(data.result);
        } else {
            alert('Ошибка: ' + data.message);
            resetUI();
        }

    } catch (error) {
        console.error(error);
        alert('Произошла ошибка при обработке.');
        resetUI();
    }
}

function simulateProgress() {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 5;
        if (progress > 90) progress = 90; // Wait for real finish
        updateProgress(progress);
        if (!processSection.classList.contains('hidden') === false) clearInterval(interval);
    }, 500);
}

function updateProgress(val) {
    progressBar.style.width = val + '%';
    percentText.innerText = Math.round(val) + '%';
}

function showResults(stems) {
    updateProgress(100);
    setTimeout(() => {
        processSection.classList.add('hidden');
        resultsSection.classList.remove('hidden');

        stemsList.innerHTML = '';

        for (const [name, path] of Object.entries(stems)) {
            const item = document.createElement('div');
            item.className = 'stem-item';
            item.innerHTML = `
                <div class="stem-info">
                    <span>🎵</span>
                    <span class="stem-name">${name}</span>
                </div>
                <a href="${path}" download class="download-btn">Скачать WAV</a>
            `;
            stemsList.appendChild(item);
        }
    }, 500);
}

resetBtn.addEventListener('click', resetUI);

function resetUI() {
    fileInput.value = '';
    resultsSection.classList.add('hidden');
    processSection.classList.add('hidden');
    dropZone.classList.remove('hidden');
    document.querySelector('.options-section').classList.remove('hidden');
    progressBar.style.width = '0%';
    percentText.innerText = '0%';
}
