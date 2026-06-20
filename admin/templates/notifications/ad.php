<h2><?php echo $title; ?></h2>
<p><?php echo $body; ?></p>
<a class="fore-color-1 text-underline" href="notifications.php"><?php echo $cta; ?></a><br>
<span id="dashboard-notifications-bar-dismiss" class="fa fa-close icon-small dismiss"></span>
<span class="icon background-color-1"><img src="images/tick.png" /></span>
<script>
    !function () {
        const notificationsBar = document.querySelector('.dashboard-notifications-bar');
        document.getElementById('dashboard-notifications-bar-dismiss').addEventListener('click', () => {
            localStorage.setItem('dashboard-notifications-bar-dismissed', true);
            notificationsBar.style.display = 'none';
        });
        if (localStorage.getItem('dashboard-notifications-bar-dismissed') === null) {
            notificationsBar.style.display = 'block';
        }
    }();
</script>
