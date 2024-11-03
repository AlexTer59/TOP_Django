function loadNotes() {
    let postId = $('.task_container').data('task-id')
    let baseUrl = 'http://127.0.0.1:8000/'

    $.ajax({
        type: 'GET',
        url: baseUrl + `/api/rest/tasks/${postId}/notes`,
        success: function(response) {
            let notesHtml = ''
            $.each(response.notes, function(index, note) {
                notesHtml += `
                    <div class="note mb-4">
                        <p class="fw-bolder mb-0">${note.profile}</p>
                        <p class="note-date">Дата: ${note.created_at}</p>
                        <p class="note-text mb-0">${note.note}</p>
                        <a class="like_button d-inline-block" href="${baseUrl}/api/tasks/${postId}/notes/${note.id}/like">
                `
                if (note.is_liked) {
                    notesHtml += `
                            <div class="like_container liked d-flex justify-content-between align-items-center px-2 py-1 my-2">
                                <div class="like_icon">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="White"
                                         class="bi bi-heart-fill" viewBox="0 0 16 16">
                                        <path fill-rule="evenodd"
                                              d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
                                    </svg>
                                </div>
                                <p class="mb-0 like_counter liked">${note.likes_count}</p>
                            </div>
                        </a>
                    `
                } else {
                    notesHtml += `
                            <div class="like_container d-flex justify-content-between align-items-center px-2 py-1 my-2">
                                <div class="like_icon">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="Gray"
                                         class="bi bi-heart-fill" viewBox="0 0 16 16">
                                        <path fill-rule="evenodd"
                                              d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314"/>
                                    </svg>
                                </div>
                                <p class="mb-0 like_counter">${note.likes_count}</p>
                            </div>
                        </a>
                    `
                }
                notesHtml += '</div>'
            });
            $('.notes_counter').text(`Заметки (${response.notes.length})`)
            $('.note_container').html(notesHtml)
        }
    });
}


$(document).ready(function (){
    loadNotes();
})

$(document).on('click', '.like_button', function(e) {
    e.preventDefault();

    let likeButton = $(this);
    let url = likeButton.attr('href');

    $.ajax({
        url: url,
        type: 'GET',
        success: function(response) {
            let isLiked = response.is_liked;
            let likesCount = response.likes_count;

            if (isLiked) {
                likeButton.find('.like_container').addClass('liked');
                likeButton.find('.like_counter').addClass('liked');
                likeButton.find('.like_icon svg').attr('fill', 'white');
            } else {
                likeButton.find('.like_container').removeClass('liked');
                likeButton.find('.like_counter').removeClass('liked');
                likeButton.find('.like_icon svg').attr('fill', 'Gray');

            }

            likeButton.find('.like_counter').text(likesCount);

        },
    });
});

$('#NoteForm').on('submit', function(e) {
    e.preventDefault();

    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: {
            note: $('#id_note').val(),
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
        },

        success: function(response) {
            loadNotes();
            $('#NoteForm')[0].reset();
            $('.error_container').html('');
        },

        error: function(response) {
            const errors = response.responseJSON;
            let err = '';
            for (let field in errors) {
                for (let error of errors[field]) {
                    err += '<p>' + error + '</p>'
                }
            }
            $('error_container').html(err)
        },
    })
})