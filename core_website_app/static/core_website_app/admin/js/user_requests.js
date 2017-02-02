var getRequestId = function($btn) {
    return $btn.parent().parent().attr("id");
};

var acceptRequest = function(event) {
    event.preventDefault();
    var requestId = getRequestId($(this));

    $.ajax({
        url : acceptUserRequestUrl,
        type : "POST",
        dataType: "json",
        data : {
        	requestid : requestId
        },
        success: function(data){
        	location.reload();
        },
        error: function() {
            console.log("error");
        }
    });
};

var denyRequestIdField = '#deny-request-id';

var denyRequestOpenModal = function(event) {
    event.preventDefault();
    var requestId = getRequestId($(this));

    $(denyRequestIdField).val(requestId);
    $('#deny-request-modal').modal('show');
};

var denyRequestConfirm = function(event) {
    event.preventDefault();
    var requestId = $(denyRequestIdField).val();

    $(denyRequestIdField).val("");

    $.ajax({
        url : denyUserRequestUrl,
        type : "POST",
        dataType: "json",
        data : {
        	requestid : requestId
        },
        success: function(){
        	location.reload();
        },
        error: function() {}
    });
};

$(document).on('click', '.accept_request', acceptRequest);
$(document).on('click', '.deny_request', denyRequestOpenModal);
$(document).on('click', '#btn-deny-request', denyRequestConfirm);

