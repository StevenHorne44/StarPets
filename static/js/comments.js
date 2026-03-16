window.currentPetId = null;

window.openCommentSidebar = function(petId) {
    console.log('Opening sidebar for pet:', petId);
    window.currentPetId = petId;
    
    const sidebar = document.getElementById('commentSidebar');
    const overlay = document.getElementById('overlay');
    
    if (!sidebar || !overlay) {
        console.error('Sidebar or overlay not found');
        return;
    }
    
    sidebar.classList.add('open');
    sidebar.style.right = '0';
    overlay.classList.add('show');
    overlay.style.display = 'block';
    
    window.loadComments(petId);
};

window.closeCommentSidebar = function() {
    console.log('Closing sidebar');
    
    const sidebar = document.getElementById('commentSidebar');
    const overlay = document.getElementById('overlay');
    
    if (sidebar) {
        sidebar.classList.remove('open');
        sidebar.style.right = '-400px';
    }
    if (overlay) {
        overlay.classList.remove('show');
        overlay.style.display = 'none';
    }
    
    window.currentPetId = null;
};

window.loadComments = function(petId) {
    console.log('Loading comments for pet:', petId);
    
    fetch(`/get-comments/${petId}/`)
        .then(response => response.json())
        .then(data => {
            window.displayComments(data.comments);
            
            const countSpan = document.querySelector(`.comment-count-${petId}`);
            if (countSpan) {
                countSpan.textContent = data.comments_count;
            }
            
            const formContainer = document.getElementById('commentFormContainer');
            const alreadyMsg = document.getElementById('alreadyCommentedMsg');
            
            if (formContainer && alreadyMsg) {
                if (data.user_commented) {
                    formContainer.style.display = 'none';
                    alreadyMsg.style.display = 'block';
                } else {
                    formContainer.style.display = 'block';
                    alreadyMsg.style.display = 'none';
                }
            }
        })
        .catch(error => {
            console.error('Error loading comments:', error);
            const commentsList = document.getElementById('commentsList');
            if (commentsList) {
                commentsList.innerHTML = '<p class="text-danger">Error loading comments</p>';
            }
        });
};

window.displayComments = function(comments) {
    const commentsList = document.getElementById('commentsList');
    
    if (!commentsList) return;
    
    if (comments.length === 0) {
        commentsList.innerHTML = '<p class="no-comments">No comments yet. Be the first to comment!</p>';
        return;
    }
    
    let html = '';
    comments.forEach(comment => {
        html += `
            <div class="comment">
                <div class="comment-header">
                    <span class="comment-author">${comment.username}</span>
                    <span class="comment-date">${comment.created_at}</span>
                </div>
                <div class="comment-content">${comment.content}</div>
            </div>
        `;
    });
    
    commentsList.innerHTML = html;
};

document.addEventListener('DOMContentLoaded', function() {
    console.log('Comments.js DOMContentLoaded');
    
    const commentForm = document.getElementById('commentForm');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const petId = window.currentPetId;
            if (!petId) {
                console.error('No pet selected');
                return;
            }
            
            const content = document.getElementById('commentContent').value;
            if (!content.trim()) {
                alert('Please enter a comment');
                return;
            }
            
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch(`/comment/${petId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `content=${encodeURIComponent(content)}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('commentContent').value = '';
                    const charCount = document.getElementById('charCount');
                    if (charCount) charCount.textContent = '0';
                    window.loadComments(petId);
                } else if (data.error) {
                    alert(data.error);
                }
            })
            .catch(error => {
                console.error('Error posting comment:', error);
                alert('An error occurred while posting your comment.');
            });
        });
    }
    
    const commentTextarea = document.getElementById('commentContent');
    if (commentTextarea) {
        commentTextarea.addEventListener('input', function() {
            const charCount = document.getElementById('charCount');
            if (charCount) {
                charCount.textContent = this.value.length;
            }
        });
    }
    
    const overlay = document.getElementById('overlay');
    if (overlay) {
        overlay.addEventListener('click', function() {
            window.closeCommentSidebar();
        });
    }
    
    const closeBtn = document.querySelector('.close-btn');
    if (closeBtn) {
        closeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Close button clicked');
            window.closeCommentSidebar();
        });
    }
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const sidebar = document.getElementById('commentSidebar');
            if (sidebar && sidebar.classList.contains('open')) {
                window.closeCommentSidebar();
            }
        }
    });
});

console.log('Comments.js fully loaded');