<div id="loading-notifications-settings">Loading...</div>
<div id="installation-needed" style="display: none">
    <h2><?php echo $installationTitle ?></h2>
    <p><?php echo $installationBody ?></p>
</div>
<div id="denied-notifications" style="display: none">
    <h2><?php echo $deniedTitle ?></h2>
    <p><?php echo $deniedBody ?></p>
    <a class="fore-color-1 text-underline" href="<?php echo $deniedUrl ?>" target="_blank"><?php echo $deniedCta ?></a>
</div>
<div id="activate-notifications" style="display: none">
    <h2><?php echo $activateTitle ?></h2>
    <p><?php echo $activateBody ?></p>
    <button id="activate-notifications-button" class="button fore-white background-color-1"><?php echo $activateCta ?></button>
</div>
<div id="set-notifications" style="display: none">
    <h2><?php echo $settingsTitle ?></h2>
    <p><?php echo $settingsBody ?></p>
    <form id="set-notifications-form">
        <label><input id="ecommerce_check" class="border border-mute-light background-transparent" type="checkbox"<?php if (isset($userSettings["ecommerce"]) && $userSettings["ecommerce"] == true) echo " checked"; ?> /> <?php echo $settingsTypeEcommerce ?></label><br />
        <label><input id="low_stock_check" class="border border-mute-light background-transparent" type="checkbox"<?php if (isset($userSettings["low_stock"]) && $userSettings["low_stock"] == true) echo " checked"; ?> /> <?php echo $settingsTypeLowStock ?></label><br />
        <label><input id="blog_comments_check" class="border border-mute-light background-transparent" type="checkbox"<?php if (isset($userSettings["blog_comments"]) && $userSettings["blog_comments"] == true) echo " checked"; ?> /> <?php echo $settingsTypeBlogComments ?></label><br />
        <label><input id="products_comments_check" class="border border-mute-light background-transparent" type="checkbox"<?php if (isset($userSettings["products_comments"]) && $userSettings["products_comments"] == true) echo " checked"; ?> /> <?php echo $settingsTypeProductsComments ?></label><br />
        <label><input id="pages_comments_check" class="border border-mute-light background-transparent" type="checkbox"<?php if (isset($userSettings["pages_comments"]) && $userSettings["pages_comments"] == true) echo " checked"; ?> /> <?php echo $settingsTypePagesComments ?></label><br />
        <label><input id="users_check" class="border border-mute-light background-transparent" type="checkbox"<?php if (isset($userSettings["users"]) && $userSettings["users"] == true) echo " checked"; ?> /> <?php echo $settingsTypeUsers ?></label><br />
        <input type="submit" class="button fore-white background-color-1" value="<?php echo $settingsCta ?>" />
    </form>
</div>
<div id="error-notifications" style="display: none">
    <h2><?php echo $genericErrorTitle ?></h2> 
    <p><?php echo $genericErrorBody ?></p>
</div>
<div id="subscription-error-notifications" style="display: none">
    <h2><?php echo $subscriptionErrorTitle ?></h2> 
    <p><?php echo $subscriptionErrorBody ?></p>
    <a class="fore-color-1 text-underline" href="<?php echo $subscriptionErrorUrl ?>" target="_blank"><?php echo $subscriptionErrorCta ?></a>
</div>
<script>
    const pushOptions = {
        userVisibleOnly: true,
        applicationServerKey: '<?php echo $vapidKey ?>'
    };
</script>
<script src="js/notifications.js"></script>
