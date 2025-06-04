document.addEventListener('DOMContentLoaded', function() {
    const photoInput = document.getElementById('photo');
    const profileImage = document.getElementById('profileImage');
    const profileImagePlaceholder = document.getElementById('profileImagePlaceholder');
    const updatePhotoBtn = document.getElementById('updatePhotoBtn');
    const cancelUploadBtn = document.getElementById('cancelUpload');
    const form = document.getElementById('profilePhotoForm');
    let selectedFile = null;

    // Handle file selection
    if (photoInput) {
        photoInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validate file type
                const validTypes = ['image/jpeg', 'image/png', 'image/gif'];
                if (!validTypes.includes(file.type)) {
                    alert('Please select a valid image file (JPEG, PNG, or GIF)');
                    return;
                }

                // Validate file size (5MB max)
                if (file.size > 5 * 1024 * 1024) {
                    alert('File size must be less than 5MB');
                    return;
                }

                selectedFile = file;
                updatePhotoBtn.disabled = false;
                cancelUploadBtn.style.display = 'inline-block';

                // Show preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    if (profileImage) {
                        profileImage.src = e.target.result;
                    } else if (profileImagePlaceholder) {
                        const img = document.createElement('img');
                        img.id = 'profileImage';
                        img.src = e.target.result;
                        img.className = 'img-thumbnail rounded-circle';
                        img.style.width = '150px';
                        img.style.height = '150px';
                        img.style.objectFit = 'cover';
                        profileImagePlaceholder.replaceWith(img);
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Handle cancel upload
    if (cancelUploadBtn) {
        cancelUploadBtn.addEventListener('click', function() {
            if (photoInput) {
                photoInput.value = '';
                selectedFile = null;
                updatePhotoBtn.disabled = true;
                cancelUploadBtn.style.display = 'none';
            }
        });
    }

    // Handle form submission
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!selectedFile) {
                e.preventDefault();
                alert('Please select a file to upload');
                return false;
            }
            // Show loading state
            updatePhotoBtn.disabled = true;
            updatePhotoBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Uploading...';
            return true;
        });
    }
});
