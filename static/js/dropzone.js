const dropzone = document.querySelector('.dropzone');
const filename = document.querySelector('.filename');
const dropzoneHint = document.querySelector('.dropzone-hint');
const droparea = document.querySelector('.droparea');

dropzone.addEventListener('dragover', e => {
    e.preventDefault();
    dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', e => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
});

dropzone.addEventListener('drop', e => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    const fileInput = document.querySelector('input[type="file"]');
    fileInput.files = e.dataTransfer.files;
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            console.log('File uploaded successfully');
        } else {
            console.error('Error uploading file');
        }
    })
    .catch(error => console.error(error));
    filename.textContent = fileInput.files[0].name;
    dropzoneHint.classList.add('hidden');
    droparea.classList.remove('bg-white');
    droparea.classList.add('greenarea');
    submitBtn.disabled = false;
});
