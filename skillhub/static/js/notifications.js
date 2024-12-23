// static/js/notifications.js

function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return null;
}

function updateNotificationBadge(count) {
    const badge = document.querySelector('#notification-badge');
    if (badge) {
        if (count > 0) {
            badge.textContent = count;
            badge.style.display = 'inline-block';
        } else {
            badge.style.display = 'none';
        }
    }
}

function fetchNotifications() {
    fetch('/booking/notifications/', {
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
    })
    .then(response => response.json())
    .then(data => {
        const notificationsList = document.querySelector('#notifications-list');
        if (notificationsList) {
            notificationsList.innerHTML = '';

            data.notifications.forEach(notification => {
                const notificationItem = document.createElement('a');
                notificationItem.href = '#';
                notificationItem.className = 'dropdown-item';
                notificationItem.innerHTML = `
                    <h6 class="fw-normal mb-0">${notification.title}</h6>
                    <small>${notification.message}</small>
                `;

                notificationItem.addEventListener('click', (e) => {
                    e.preventDefault();
                    markNotificationAsRead(notification.id);
                });

                notificationsList.appendChild(notificationItem);
            });

            // Update the badge count
            updateNotificationBadge(data.notifications.length);
        }
    })
    .catch(error => {
        console.error('Error fetching notifications:', error);
    });
}

function markNotificationAsRead(notificationId) {
    fetch(`/booking/notifications/mark/${notificationId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Refresh notifications after marking as read
            fetchNotifications();
        }
    })
    .catch(error => {
        console.error('Error marking notification as read:', error);
    });
}

function handleBookingNotification(notificationId, bookingId) {
    const action = confirm("Would you like to accept this booking?");
    if (action !== null) {
        let status = action ? 'ACCEPTED' : 'REJECTED';
        let rejectionReason = action ? '' : prompt("Provide a rejection reason:");

        fetch(`/respond_to_booking/${bookingId}/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCSRFToken() },
            body: JSON.stringify({ status: status, rejection_reason: rejectionReason })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Response recorded');
                fetchNotifications();  // Refresh notifications
            }
        });
    }
}


document.addEventListener('DOMContentLoaded', () => {
    fetchNotifications();
    setInterval(fetchNotifications, 30000);
});
