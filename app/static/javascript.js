// Delete modal
$('#deleteModal').on('show.bs.modal', function (event) {
    var trigger = $(event.relatedTarget) // tag that triggered the modal
    var message = trigger.data('message')
    var url = trigger.data('url')
    var modal = $(this)
    modal.find('.modal-message').text(message)
    modal.data('url', url)
});

$('#deleteModal-button').click(function () {
    var url = $('#deleteModal').data('url')
    document.location.href = url
    $('#deleteModal').modal('hide')
});

// End Delete modal

// Photo modal
$('#photoModal').on('show.bs.modal', function (event) {
    var trigger = $(event.relatedTarget) // tag that triggered the modal
    var id = trigger.data('id')
    var modal = $(this)
    modal.data('id', id)
    modal.find('.photo').attr('src', '/gallery/photo/thumb/' + id + '/900x600')
    modal.find('.btn-open').attr('href', '/gallery/photo/view/' + id)
    modal.find('.btn-edit').attr('href', '/gallery/photo/edit/' + id)
    modal.find('.btn-download').attr('href', '/gallery/photo/raw/' + id)
    $.getJSON('/gallery/json/photo/' + id, function(data,status) {
        if (data.title != null){
            $('#image-title').text((data.title))
        }
        if (data.caption != null){
            $('#image-caption').text(data.caption)
        }
    });
});

$('.btn-more-info').on('click', function(event) {
        event.preventDefault();
        $( '.more-info' ).toggleClass( "hide" );
    })

// End Photo modal
