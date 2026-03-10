// --- JavaScript for handling bookmark toggling and rating ---
// Wait for the page to fully load
document.addEventListener('DOMContentLoaded', function () {

    const buttons = document.querySelectorAll('.toggle-bookmark-btn');
    const starWrappers = document.querySelectorAll('.interactive-rating .star-rating-wrapper');

    // --- BOOKMARK LOGIC ---
    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();

            const petId = this.getAttribute('data-pet-id');
            const btn = this;

            fetch(`${BOOKMARK_URL}${petId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
                .then(response => {
                    if (!response.ok) { throw new Error(`HTTP error! status: ${response.status}`); }
                    return response.json();
                })
                .then(data => {
                    if (typeof data.is_bookmarked !== 'undefined') {
                        if (data.is_bookmarked === true) {
                            btn.classList.replace('btn-bookmark', 'btn-unbookmark');
                            btn.textContent = 'Unbookmark';
                        } else {
                            btn.classList.replace('btn-unbookmark', 'btn-bookmark');
                            btn.textContent = 'Bookmark';
                        }
                    } else {
                        console.error("Backend did not return 'is_bookmarked'.", data);
                    }
                })
                .catch(error => console.error('Fetch Error:', error));
        });
    });

    // --- RATING LOGIC ---
    starWrappers.forEach(wrapper => {
        wrapper.addEventListener('click', function (e) {

            const rect = this.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            let newRating = Math.ceil((clickX / rect.width) * 5);

            if (newRating < 1) newRating = 1;
            if (newRating > 5) newRating = 5;

            const parentContainer = this.closest('.interactive-rating');
            const petId = parentContainer.getAttribute('data-pet-id');

            fetch(`${RATE_URL}${petId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ 'rating': newRating })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const goldStars = parentContainer.querySelector('.gold-stars-overlay');
                        const fillPercentage = (data.new_average / 5.0) * 100;
                        goldStars.style.width = `${fillPercentage}%`;

                        const ratingText = parentContainer.querySelector('.rating-text');
                        ratingText.textContent = `(${data.new_average.toFixed(1)}/5.0)`;
                    }
                })
                .catch(error => console.error('Error:', error));
        });
    });

    //-----------PROFILE DROPDOWN MENU------------------
    const menuButton = document.getElementById('profile-dropdown');
    const dropDownMenu = document.getElementById('dropdown-menu');

    //prevent error if used not logged in
    if (menuButton && dropDownMenu) {}
        menuButton.addEventListener('click', (e) => {
            dropDownMenu.classList.toggle('show'); //toggle display dropdown
            e.stopPropagation(); //stop closing immediately
        });

    // close menu if click outside it
    window.addEventListener('click', () => {
        if (dropDownMenu.classList.contains('show')){
            dropDownMenu.classList.remove('show');
        }
    });



});


// --- Stnadart Django Helper function to manage cookies ---
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;

}

