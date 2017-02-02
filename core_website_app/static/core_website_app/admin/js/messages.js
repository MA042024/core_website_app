var deleteMessageIdField = "#delete-message-id";

removeMessageOpenModal = function(event) {
    event.preventDefault();

    var messageId = $(this).parents('tr').attr("id");
    $(deleteMessageIdField).val(messageId);
    $("#delete-message-modal").modal("show");
};

removeMessageConfirm = function(event){
	event.preventDefault();
	var messageId = $(deleteMessageIdField).val();

    $.ajax({
        url: removeMessageUrl,
        type : "POST",
        data:{
        	messageid: messageId
        },
        dataType: "json",
        success: function(){
        	location.reload();
        }
    });
};

$(document).on('click', '.remove_message', removeMessageOpenModal);
$(document).on('click', '#btn-delete-message', removeMessageConfirm);