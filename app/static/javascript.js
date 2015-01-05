// Delete modal
$('#deleteModal').on('show.bs.modal', function (event) {
    var trigger = $(event.relatedTarget) // tag that triggered the modal
    var element = trigger.data('element')
    var type = trigger.data('type')
    var id = trigger.data('id')
    var modal = $(this)
    modal.find('.modal-message').text('Are you sure you want to delete ' + element + ' ' + type + '?')
    modal.data('id', id)
    modal.data('type', type)
});

$('#deleteModal-button').click(function () {
    var id = $('#deleteModal').data('id')
    var type = $('#deleteModal').data('type')
    document.location.href = '/' + type + '/delete/' + id
    $('#deleteModal').modal('hide')
});

// End Delete modal

// Photo modal
$('#photoModal').on('show.bs.modal', function (event) {
    var trigger = $(event.relatedTarget) // tag that triggered the modal
    var id = trigger.data('id')
    var modal = $(this)
    modal.data('id', id)
    modal.find('.photo').attr('src', '/photo/thumb/' + id + '/900x600')
    modal.find('.btn-open').attr('href', '/photo/view/' + id)
    modal.find('.btn-edit').attr('href', '/photo/edit/' + id)
    modal.find('.btn-delete').attr('href', '/photo/delete/' + id)
    modal.find('.btn-download').attr('href', '/photo/raw/' + id)
});

$('.btn-more-info').on('click', function(event) {
        event.preventDefault();
        $( '.more-info' ).toggleClass( "hide" );
    })

// End Photo modal
