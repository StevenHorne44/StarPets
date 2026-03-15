console.log("🔥 comments.js loaded - START");
console.log("Timestamp:", new Date().toISOString());

// Test function to verify global scope
window.testCommentFunction = function() {
    console.log("✅ testCommentFunction called");
    alert("Comment JS is working!");
};

console.log("📝 Defining openCommentSidebar function");

// Global variable to store current pet ID
let currentPetId = null;

// Function to open the comment sidebar
window.openCommentSidebar = function(petId) {
    console.log("📝 openCommentSidebar called with petId:", petId);
    console.log("📝 Checking elements...");
    
    currentPetId = petId;
    
    const sidebar = document.getElementById('commentSidebar');
    const overlay = document.getElementById('overlay');
    
    console.log("📝 Sidebar element:", sidebar);
    console.log("📝 Overlay element:", overlay);
    
    if (!sidebar) {
        console.error("❌ Sidebar element not found!");
        return;
    }
    if (!overlay) {
        console.error("❌ Overlay element not found!");
        return;
    }
    
    sidebar.classList.add('open');
    overlay.classList.add('show');
    console.log("✅ Sidebar opened");
    
    // Load comments for this pet
    loadComments(petId);
};

// Function to close the comment sidebar
window.closeCommentSidebar = function() {
    console.log("📝 closeCommentSidebar called");
    
    const sidebar = document.getElementById('commentSidebar');
    const overlay = document.getElementById('overlay');
    
    if (sidebar) sidebar.classList.remove('open');
    if (overlay) overlay.classList.remove('show');
    
    currentPetId = null;
    console.log("✅ Sidebar closed");
};

// Function to load comments for a pet
function loadComments(petId) {
    console.log("📝 loadComments called for pet:", petId);
    
    fetch(`/get-comments/${petId}/`)
        .then(response => {
            console.log("📝 Fetch response status:", response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("📝 Comments data received:", data);
            displayComments(data.comments);
            
            // Update comment count
            const countSpan = document.querySelector(`.comment-count-${petId}`);
            if (countSpan) {
                countSpan.textContent = data.comments_count;
                console.log("✅ Updated comment count to:", data.comments_count);
            }
            
            // Show/hide form
            const formContainer = document.getElementById('commentFormContainer');
            const alreadyMsg = document.getElementById('alreadyCommentedMsg');
            
            if (formContainer && alreadyMsg) {
                if (data.user_commented) {
                    formContainer.style.display = 'none';
                    alreadyMsg.style.display = 'block';
                    console.log("✅ User already commented - hiding form");
                } else {
                    formContainer.style.display = 'block';
                    alreadyMsg.style.display = 'none';
                    console.log("✅ User can comment - showing form");
                }
            }
        })
        .catch(error => {
            console.error("❌ Error loading comments:", error);
            document.getElementById('commentsList').innerHTML = 
                '<p class="text-danger">Error loading comments. Please try again.</p>';
        });
}

// Function to display comments
function displayComments(comments) {
    console.log("📝 displayComments called with", comments.length, "comments");
    
    const commentsList = document.getElementById('commentsList');
    
    if (!commentsList) {
        console.error("❌ commentsList element not found");
        return;
    }
    
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
    console.log("✅ Comments displayed");
}

// Initialize when the page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log("📝 DOMContentLoaded event fired");
    console.log("✅ comments.js initialization complete");
    
    // Set up comment form submission
    const commentForm = document.getElementById('commentForm');
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log("📝 Comment form submitted");
            
            if (!currentPetId) {
                console.error("❌ No pet selected");
                return;
            }
            
            const content = document.getElementById('commentContent').value;
            if (!content.trim()) {
                alert('Please enter a comment');
                return;
            }
            
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch(`/comment/${currentPetId}/`, {
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
                console.log("📝 Comment submission response:", data);
                
                if (data.success) {
                    document.getElementById('commentContent').value = '';
                    document.getElementById('charCount').textContent = '0';
                    loadComments(currentPetId);
                } else if (data.error) {
                    alert(data.error);
                }
            })
            .catch(error => {
                console.error("❌ Error posting comment:", error);
                alert('An error occurred while posting your comment.');
            });
        });
    }
    
    // Character counter
    const commentTextarea = document.getElementById('commentContent');
    if (commentTextarea) {
        commentTextarea.addEventListener('input', function() {
            const charCount = document.getElementById('charCount');
            if (charCount) {
                charCount.textContent = this.value.length;
            }
        });
    }
});

console.log("🔥 comments.js loaded - END");

function openCommentSidebar(petId) {
    currentPetId = petId;
    document.getElementById('commentSidebar').classList.add('open');
    document.getElementById('overlay').classList.add('show');
    loadComments(petId);
}

function closeCommentSidebar() {
    document.getElementById('commentSidebar').classList.remove('open');
    document.getElementById('overlay').classList.remove('show');
    currentPetId = null;
}

function loadComments(petId) {
    fetch(`/get-comments/${petId}/`)
        .then(response => response.json())
        .then(data => {
            displayComments(data.comments);
            
            
            const countSpan = document.querySelector(`.comment-count-${petId}`);
            if (countSpan) {
                countSpan.textContent = data.comments_count;
            }
            
            
            if (data.user_commented) {
                document.getElementById('commentFormContainer').style.display = 'none';
                document.getElementById('alreadyCommentedMsg').style.display = 'block';
            } else {
                document.getElementById('commentFormContainer').style.display = 'block';
                document.getElementById('alreadyCommentedMsg').style.display = 'none';
            }
        });
}

function displayComments(comments) {
    const commentsList = document.getElementById('commentsList');
    
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
}


document.getElementById('commentForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (!currentPetId) return;
    
    const content = document.getElementById('commentContent').value;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/comment/${currentPetId}/`, {
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
            
        
            loadComments(currentPetId);
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while posting your comment.');
    });
});


document.getElementById('overlay').addEventListener('click', closeCommentSidebar);


document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && document.getElementById('commentSidebar').classList.contains('open')) {
        closeCommentSidebar();
    }
});