$('.like_button').click(function(e) {
    e.preventDefault();

    let = likeButton = $(this);
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