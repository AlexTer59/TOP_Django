

$('#feedback_form').on('submit', function(e) {
    e.preventDefault();

    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: {
            name: $('#id_name').val(),
            text: $('#id_text').val(),
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
        },
        success: function(response) {
            $('.page_title').text('Обратная свзяь отправлена!');
            $('.form_container').hide()
        },
        error: function(response) {
            const errors = response.responseJSON.errors;
            let err = ''
            for (let field in errors) {
                for (let error of errors[field]) {
                    err += '<p>' + error + '</p>'
                }
            }
            $('.formErrors').html(err)
        }

    });

})

