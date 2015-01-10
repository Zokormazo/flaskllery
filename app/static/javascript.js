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
            $('#image-title').text(data.title)
        }
        if (data.caption != null){
            $('#image-caption').text(data.caption)
        }
        if (data.filename != null){
            $('#image-file').text(data.filename)
        }
        if (data.size != null){
            $('#image-size').text(data.size)
        }
        if (data.format != null){
            $('#image-format').text(data.format)
        }
        if (data.width != null && data.height != null){
            $('#image-resolution').text(data.width + 'x' + data.height)
        }
        if (data.mode != null){
            $('#image-mode').text(data.mode)
        }
    });
    $.getJSON('/gallery/json/photo/' + id + '/exif', function(data,status) {
        if (data.aperture != null){
            $('#exif-aperture').text(data.aperture[0] + '/' + data.aperture[1])
        }
        if (data.camera_make != null){
            $('#exif-camera-make').text(data.camera_make)
        }
        if (data.camera_model != null){
            $('#exif-camera-model').text(data.camera_model)
        }
        if (data.focal_length){
            $('#exif-focal-length').text(data.focal_length[0] + '/' + data.focal_length[1])
        }
        if (data.iso){
            $('#exif-iso').text(data.iso)
        }
        if (data.taken_at){
            $('#exif-taken-at').text(data.taken_at)
        }
        if (data.orientation){
            $('#exif-orientation').text(data.orientarion)
        }
        if (data.latitude){
            $('#exif-latitude').text(data.latitude)
        }
        if (data.longitude){
            $('#exif-longitude').text(data.longitude)
        }
    });
});

$('.btn-more-info').on('click', function(event) {
        event.preventDefault();
        $( '.more-info' ).toggleClass( "hide" );
    })

// End Photo modal
