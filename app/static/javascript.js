document.querySelector('.delete-album').onclick = function(){
    swal({
        title: "Are you sure?",
        text: "You will not be able to recover album!",
        type: "error",
        showCancelButton: true,
        confirmButtonClass: 'btn-danger',
        confirmButtonText: 'Delete!'
    },

    function(){
        var url = document.getElementsByClassName('delete-album')[0].getAttribute("data");
	document.location.href = url;
    });
};


