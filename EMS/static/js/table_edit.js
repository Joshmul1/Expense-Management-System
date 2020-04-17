$(document).ready(function () {

    $('#table_id').DataTable({
        language: {
            paginate: {
            next: '&#8594;',
            previous: '&#8592;'
            }
        },
        buttons: [
            'print'
        ]
    })

});