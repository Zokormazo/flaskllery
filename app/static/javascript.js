/**
 * Copyright 2014, Julen Landa Alustiza
 *
 * Licensed under the Eiffel Forum License 2.
 */

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
