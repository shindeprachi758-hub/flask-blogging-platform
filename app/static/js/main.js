/**
 * BlogCraft - Main JavaScript Application File
 * Integrates Quill Rich Text Editor, dynamic form handlers, and micro-interactions.
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Auto dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // 2. Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 3. Initialize Quill Rich Text Editor if editor container is present
    const editorContainer = document.getElementById('editor-container');
    const contentTextarea = document.getElementById('content-textarea');

    if (editorContainer && contentTextarea) {
        const quill = new Quill('#editor-container', {
            theme: 'snow',
            placeholder: 'Compose your insightful article here...',
            modules: {
                toolbar: [
                    [{ 'header': [1, 2, 3, false] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    ['blockquote', 'code-block'],
                    [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                    [{ 'color': [] }, { 'background': [] }],
                    ['link', 'clean']
                ]
            }
        });

        // Prefill existing content from hidden textarea
        if (contentTextarea.value.trim().length > 0) {
            quill.root.innerHTML = contentTextarea.value;
        }

        // On parent form submission, sync Quill HTML to textarea
        const form = contentTextarea.closest('form');
        if (form) {
            form.addEventListener('submit', function () {
                contentTextarea.value = quill.root.innerHTML;
            });
        }
    }
});

