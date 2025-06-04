// This will initialize flatpickr on all date inputs
window.addEventListener('DOMContentLoaded', function() {
    if (window.flatpickr) {
        flatpickr('input[type="date"], .datepicker', {
            dateFormat: 'Y-m-d',
            allowInput: true,
            altInput: true,
            altFormat: 'F j, Y',
            placeholder: 'Select a date',
        });
    }
});
