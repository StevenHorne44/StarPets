console.log("JS is connected");

window.currentPetId = null;
window.currentUserCommentId = null;
window.currentUserCommentText = "";

// ------ SIDEBAR CONTROL FUNCTIONS ------
window.openCommentSidebar = function(petId) {
    window.currentPetId = petId;

    const sidebar = document.getElementById('commentSidebar');
    const overlay = document.getElementById('overlay');
    const form = document.getElementById('commentForm');
    if (form) {
        form.dataset.mode = "add";
        form.dataset.editId = "";
        const submitBtn = document.getElementById('submitBtn');
        if (submitBtn) submitBtn.textContent = "Post Comment";
        const textarea = document.querySelector('.comment-textarea');
        if (textarea) textarea.value = "";
    }

    if (sidebar && overlay) {
        sidebar.classList.add('open');
        sidebar.style.right = '0';
        overlay.style.display = 'block';
        window.loadComments(petId);
    } 
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
};

//-------------- DATA FETCHING & DISPLAY ----------
window.loadComments = function(petId) {    
    fetch(`/get-comments/${petId}/`)
        .then(response => response.json())
        .then(data => {
            window.displayComments(data.comments);
            window.currentUserCommentText = data.user_text || "";
            window.currentUserCommentId = data.user_comment_id;

            const formContainer = document.getElementById('commentFormContainer');
            const alreadyMsg = document.getElementById('alreadyCommentedMsg');
            
            if (data.user_commented) {
                formContainer.style.display = 'none';
                alreadyMsg.style.display = 'block';
            } else {
                formContainer.style.display = 'block';
                alreadyMsg.style.display = 'none';
            }
        })
        .catch(err => console.error("Error loading comments:", err));
    };

window.displayComments = function(comments) {
    const commentsList = document.getElementById('commentsList');
    
    if (!commentsList) return;
    
    if (comments.length === 0) {
        commentsList.innerHTML = '<p class="no-comments">No comments yet. Be the first to comment!</p>';
        return;
    }
    commentsList.innerHTML = comments.map(c => `
        <div class="comment mb-3 p-2 border-bottom">
            <small class="fw-bold">${c.username}</small>
            <small class="text-muted float-end">${c.created_at}</small>
            <p class="mb-0">${c.content}</p>
        </div>
    `).join('');
};


// -------- ACTION FUNCTIONS (EDIT,DELETE,CANCEL) ------------

window.enableCommentEdit = function() {
    console.log("Edit Mode Activated");

    const form = document.getElementById('commentForm');
    const textarea = document.querySelector('.comment-textarea') || document.getElementById('id_content');
    const submitBtn = document.getElementById('submitBtn');
    
    if (!textarea) {
        console.error("Could not find the textarea.");
        return;
    }

    document.getElementById('alreadyCommentedMsg').style.display = 'none';
    document.getElementById('commentFormContainer').style.display = 'block';
    document.getElementById('cancelEditBtn').style.display = 'block';

    textarea.value = window.currentUserCommentText;
    form.dataset.mode = "edit";
    form.dataset.editId = window.currentUserCommentId;
    if (submitBtn) submitBtn.textContent = "Update Comment";
    textarea.focus();
};

window.cancelEdit = function() {    
    const commentForm = document.getElementById('commentForm');
    commentForm.dataset.mode = "add";
    document.getElementById('commentFormContainer').style.display = 'none';
    document.getElementById('alreadyCommentedMsg').style.display = 'block';
}

window.deleteComment = function() {
    console.log("Delete attempt for ID:" , window.currentUserCommentId);

    if(!window.currentUserCommentId) {
        alert("Could not find comment ID to delete.");
        return;
    }

    if (confirm("Are you sure you want to delete your comment?")) {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/delete-comment/${window.currentUserCommentId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.loadComments(window.currentPetId);
            } else {
                alert(data.error || "Something went wrong.");
            }
        })
        .catch(error => console.error("Error:" , error));
    }
};



//------- DOM READY EVENT LISTENERS ------------
document.addEventListener('DOMContentLoaded', function() {    
    const commentForm = document.getElementById('commentForm');

    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
                        
            const editId = commentForm.dataset.editId;
            const mode = commentForm.dataset.mode;
            const url = (mode === "edit") ? `/edit-comment/${editId}/` : `/comment/${window.currentPetId}/`;

            const textarea = document.querySelector('.comment-textarea');
            if (!textarea) return;

            const content = textarea.value;

            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({content: content})
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw err; });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    textarea.value = '';
                    commentForm.dataset.mode = "add";
                    document.getElementById('submitBtn').textContent = "Post Comment";
                    const cancelBtn = document.getElementById('cancelEditBtn');
                    if (cancelBtn) cancelBtn.style.display = 'none';

                    window.loadComments(window.currentPetId);
                }
            })
            .catch(err => {
                console.error("Submit error:", err);
                alert(err.error || "Unexpected error occured.");
            });
        });
    }

    const commentTextarea = document.querySelector('.comment-textarea');
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