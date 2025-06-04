document.addEventListener('DOMContentLoaded', function() {
    const passwordForm = document.getElementById('passwordForm');
    const updatePasswordBtn = document.getElementById('updatePasswordBtn');
    let spinner;
    let errorContainer;
    
    if (updatePasswordBtn) {
        spinner = updatePasswordBtn.querySelector('.spinner-border');
        errorContainer = document.getElementById('passwordFormErrors');
        
        // Handle form submission
        passwordForm.addEventListener('submit', function(e) {
            // Prevent default form submission
            e.preventDefault();
            e.stopPropagation();
            
            // Reset UI
            errorContainer.classList.add('d-none');
            updatePasswordBtn.disabled = true;
            if (spinner) spinner.classList.remove('d-none');
            
            // Clear previous error states
            document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
            document.querySelectorAll('.invalid-feedback').forEach(el => el.textContent = '');
            
            // Process the form
            processForm();
        });
    }
    
    async function processForm() {
        try {
            const formData = new FormData(passwordForm);
            // Get the CSRF token from the form
            const csrfToken = document.querySelector('input[name="csrf_token"]').value;
            
            const response = await fetch('/staff/change-password', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                // Show success message using Bootstrap's toast
                const toastEl = document.getElementById('successToast');
                if (toastEl) {
                    const toastBody = toastEl.querySelector('.toast-body');
                    if (toastBody) {
                        toastBody.textContent = data.message || 'Password updated successfully';
                    }
                    const toast = new bootstrap.Toast(toastEl);
                    toast.show();
                }
                
                // Close the modal after a short delay
                setTimeout(() => {
                    const modal = bootstrap.Modal.getInstance(document.getElementById('changePasswordModal'));
                    if (modal) {
                        modal.hide();
                    }
                    // Reset the form
                    passwordForm.reset();
                }, 1500);
            } else {
                // Handle form errors
                if (data.errors) {
                    // Show field-specific errors
                    Object.entries(data.errors).forEach(([field, message]) => {
                        const input = passwordForm.querySelector(`[name="${field}"]`);
                        if (input) {
                            input.classList.add('is-invalid');
                            const feedback = input.nextElementSibling;
                            if (feedback && feedback.classList.contains('invalid-feedback')) {
                                feedback.textContent = message;
                            }
                        }
                    });
                } else if (data.error) {
                    // Show general error
                    errorContainer.textContent = data.error;
                    errorContainer.classList.remove('d-none');
                }
            }
        } catch (error) {
            console.error('Error:', error);
            errorContainer.textContent = 'An unexpected error occurred. Please try again.';
            errorContainer.classList.remove('d-none');
        } finally {
            updatePasswordBtn.disabled = false;
            if (spinner) spinner.classList.add('d-none');
        }
    }
});
