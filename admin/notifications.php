<?php

include "includes.php";

Configuration::getControlPanel()->accessOrRedirect();
$settings = Configuration::getSettings();
$notifier = Configuration::getNotifier();
$login = Configuration::getPrivateArea();

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_GET['permission'])) {
    $body = file_get_contents("php://input");
    $json = json_decode($body, true);
    $notifier->savePermission($json, $login->whoIsLogged());
	exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_GET['settings'])) {
    $body = file_get_contents("php://input");
    $json = json_decode($body, true);
    $notifier->saveSettings($json, $login->whoIsLogged());
	exit;
}

// Load the main template
$mainT = Configuration::getControlPanel()->getMainTemplate();
$mainT->pagetitle = l10n("notifications_title", "Notifications");
$mainT->stylesheets = array("css/notifications.css");
$mainT->content = "<div class=\"notifications-container\">";

// Intro
$introBoxT = new Template("templates/common/box.php");
$introBoxT->cssClass = "notifications-intro";
$introBoxT->content = "";
$introT = new Template("templates/notifications/intro.php");
$introT->title = l10n('admin_notifications_intro_title', 'Welcome to Notifications section');
$introT->body1 = l10n('admin_notifications_intro_body_1', 'Stay updated in real time on your website\'s activities and get a notification every time users register, comment or place an order.');
$introT->body2 = l10n('admin_notifications_intro_body_2', 'Here you can configure your browser to receive the Notifications.');
$introBoxT->content .= $introT->render();
$mainT->content .= $introBoxT->render();

// Settings
$userSettings = $notifier->loadSettings($login->whoIsLogged());
$settingsBoxT = new Template("templates/common/box.php");
$settingsBoxT->cssClass = "notifications-settings";
$settingsBoxT->content = "";
$settingsT = new Template("templates/notifications/settings.php");
$settingsT->installationTitle = l10n('admin_notifications_installation_title', 'Installation needed');
$settingsT->installationBody = l10n('admin_notifications_installation_body', 'In order to receive the notifications, you need to install the admin on the device.');
$settingsT->deniedTitle = l10n('admin_notifications_denied_title', 'Notifications not allowed');
$settingsT->deniedBody = l10n('admin_notifications_denied_body', 'In order to receive the notifications, you need to reset the permission.');
$settingsT->deniedCta = l10n('admin_notifications_denied_cta', 'Find out how');
$settingsT->deniedUrl = l10n('admin_notifications_denied_url', 'https://example.com/');
$settingsT->activateTitle = l10n('admin_notifications_activate_title', 'Enable the Notifications');
$settingsT->activateBody = l10n('admin_notifications_activate_body', 'In order to receive the notifications, you need to give permissions.');
$settingsT->activateCta = l10n('admin_notifications_activate_cta', 'Turn on the Notifications');
$settingsT->settingsTitle = l10n('admin_notifications_settings_title', 'Settings');
$settingsT->settingsBody = l10n('admin_notifications_settings_body', 'Choose what kind of notifications you want to receive.');
$settingsT->settingsCta = l10n('admin_notifications_settings_cta', 'Save');
$settingsT->settingsTypeEcommerce = l10n('admin_notifications_settings_type_ecommerce', 'E-Commerce');
$settingsT->settingsTypeLowStock = l10n('admin_notifications_settings_type_low_stock', 'Low Products Stock');
$settingsT->settingsTypeBlogComments = l10n('admin_notifications_settings_type_blog_comments', 'Blog Comments');
$settingsT->settingsTypeProductsComments = l10n('admin_notifications_settings_type_products_comments', 'Products Comments');
$settingsT->settingsTypePagesComments = l10n('admin_notifications_settings_type_pages_comments', 'Pages Comments');
$settingsT->settingsTypeUsers = l10n('admin_notifications_settings_type_users', 'Users');
$settingsT->genericErrorTitle = l10n('admin_notifications_generic_error_title', 'Error');
$settingsT->genericErrorBody = l10n('admin_notifications_generic_error_body', 'Something went wrong, please retry later.');
$settingsT->subscriptionErrorTitle = l10n('admin_notifications_subscription_error_title', 'Subscription Error');
$settingsT->subscriptionErrorBody = l10n('admin_notifications_subscription_error_body', 'In order to receive the notifications, you need to reset the permission.');
$settingsT->subscriptionErrorCta = l10n('admin_notifications_subscription_error_cta', 'Find out how');
$settingsT->subscriptionErrorUrl = l10n('admin_notifications_subscription_error_url', 'https://example.com/');
$settingsT->vapidKey = $settings["admin"]["notification_public_key"];
$settingsT->userSettings = $userSettings;
$settingsBoxT->content .= $settingsT->render();
$mainT->content .= $settingsBoxT->render();

// Help
$helpBoxT = new Template("templates/common/box.php");
$helpBoxT->cssClass = "notifications-help";
$helpBoxT->content = "";
$helpT = new Template("templates/notifications/help.php");
$helpT->title = l10n('admin_notifications_help_title', 'Help');
$helpT->body = l10n('admin_notifications_help_body', 'Find out how to install the Admin as an App.');
$helpT->cta = l10n('admin_notifications_help_cta', 'Let\'s find out');
$helpT->url = l10n('admin_notifications_help_url', 'https://example.com/');
$helpBoxT->content .= $helpT->render();
$mainT->content .= $helpBoxT->render() . "</div>";

echo $mainT->render();

