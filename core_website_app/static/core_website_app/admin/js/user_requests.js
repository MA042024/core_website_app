let noCustomEmailForm = false;
let jqTextarea = $("#custom-email-textarea");
let jqEmailSubject = $("#custom-email-subject");
let intialEmailSubject = "";
let getRequestId = function($btn) {
    return $btn.parent().parent().attr("id");
};
let denyRequestIdField = '#deny-request-id';

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
        error: function(error) {
            console.log(error);
        }
    });
};


/**
 * Open the modal and edit the default email template with the user information
 */
var denyRequestOpenModal = function(event) {
    event.preventDefault();

    // set the selected request id in thw form
    let requestId = getRequestId($(this));
    $(denyRequestIdField).val(requestId);

    // retrieve the email template only if needed
    if(!noCustomEmailForm) {
        $.ajax({
            url : denyGetEmailTemplateUrl,
            data: {
                requestid: requestId
            },
            type : "GET",
            success: function(data){
                // inject the template content in the DOM
                jqTextarea.val(data.template);
            },
            error: function(error) {
                console.log(error);
            }
        });
    }

    $('#deny-request-modal').modal('show');
};

    /**
     * denyRequestConfirm send a request to the backend to confirm the deletion
     * @param: event {object} MouseClick event
     * @param: sendEmail {boolean} send an email
     */
var denyRequestConfirm = function(event, sendEmail) {
    // stop event spread
    event.preventDefault();
    // reset the last error container
    $(".error-container").hide();

    let emailParams;
    let requestId = $(denyRequestIdField).val();

    // check which button triggered this event
    if(sendEmail) {
        emailParams = {
            subject: jqEmailSubject.val(),
            body: jqTextarea.val()
        }
    }


    $.ajax({
        url : denyUserRequestUrl,
        type : "POST",
        dataType: "json",
        data : {
        	requestid: requestId,
        	sendEmail: sendEmail,
        	emailParams: emailParams
        },
        success: function(){
        	location.reload();
        },
        error: function(error) {
            let errorMessage;

            if(error.status === 400 && error.responseText.indexOf("Unsafe") !== -1) {
                errorMessage = "This HTML is unsafe, please delete all the embedded scripts and try again.";
            } else if (error.status === 400) {
                errorMessage = "HTML is not generated properly, please check your HTML syntax!";
            } else {
                errorMessage = "Impossible to deny this account request, please retry.";
            }

            // display the error
            $(".error-container").show();
            $("#error-text").html(errorMessage);
        }
    });
};

// create the listeners and save the initial email template
$(document).ready(function() {
    $(document).on('click', '.accept_request', acceptRequest);
    $(document).on('click', '.deny_request', denyRequestOpenModal);
    $(document).on('click','#btn-deny-request-email', e=>denyRequestConfirm(e, true));
    $(document).on('click','#btn-deny-request', e=>denyRequestConfirm(e, false));

    // if the custom email field is displayed init the form
    if($("#custom-email-textarea").length > 0) {
        jqTextarea = $("#custom-email-textarea");
        jqEmailSubject = $("#custom-email-subject");

        $('#deny-request-modal').on('hide.bs.modal', function (e) {
            // reset the email subject
            jqEmailSubject.val(intialEmailSubject);
        });
        intialEmailSubject = jqEmailSubject.val();
    } else {
        noCustomEmailForm = true;
    }

});

