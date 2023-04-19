const dropzone = document.querySelector('.dropzone');

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
    const submitForm = document.querySelector('form');
    submitForm.submit();
});
