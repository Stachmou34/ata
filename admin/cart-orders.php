<?php

require_once "includes.php";

Configuration::getControlPanel()->accessOrRedirect();

// Load the cart
$ecommerce = Configuration::getCart();
$ecommerce->deleteTemporaryFiles("../");

// Execute the required actions
if (isset($_GET['delete'])) {
	$ecommerce->deleteOrderFromDb($_GET['delete']);
}
if (isset($_GET['waiting'])) {
	$ecommerce->moveOrderToWaiting($_GET['waiting']);
}
if (isset($_GET['inbox'])) {
	$ecommerce->moveOrderToInbox($_GET['inbox']);
}
$evadeResult = null;
if (isset($_GET['evade'])) {
	$tracking_code = (isset($_GET['track_code']) && $_GET['track_code'] !== '') ? $_GET['track_code'] : null;
	$force = false;
	if ( isset( $_GET['force'] ) && $_GET['force'] == true ) {
		$force = true;
	}
	$evadeResult = $ecommerce->evadeOrder( $_GET['evade'], '', $tracking_code, $force );
}
if ( isset( $_GET['remind'] ) ) {
	$ecommerce->sendPaymentReminder( $_GET['remind'] );
}
if (isset($_GET['unevade'])) {
	$ecommerce->unevadeOrder($_GET['unevade']);
}

// Get the required status page and pick the right color
$status = '';
$color = 4;
switch (isset($_GET['status']) ? $_GET['status'] : 'inbox') {	
	case 'waiting': $status = 'waiting'; $color = 2; break;
	case 'evaded': $status = 'evaded'; $color = 3; break;
	default: $status = 'inbox'; $color = 4; break;
}

// Load the DB data
$pagination_length = 15;
$pagination_start = (isset($_GET['page']) ? $_GET['page'] * $pagination_length : 0);
$orders = $ecommerce->getOrders($pagination_start, $pagination_length, @$_GET['search'], $status);

$reminders = $ecommerce->getPaymentReminders( $orders );

// load the shipping data from the configuration
foreach ($orders['orders'] as &$order) {
	if (isset($order['shipping_id'])) {
		$shipping_data = Configuration::getCart()->getShippingData([$order['shipping_id']]);
		if (count($shipping_data) > 0 && isset($shipping_data[$order['shipping_id']])) {
			$order['shipping_data'] = $shipping_data[$order['shipping_id']];
		}
	}
}

// Load the main template
$mainT = Configuration::getControlPanel()->getMainTemplate();
$mainT->stylesheets = array("css/cart.css");
$mainT->scripts = array("js/orders.js");
$mainT->pagetitle = l10n("admin_cart_title", "E-Commerce");
$contentT = new Template("templates/common/box.php");
$contentT->cssClass = "cart";
$contentT->content = "";

// Add the table tabs
$tabsT = new Template("templates/cart/tabs.php");
$tabsT->borderColorClass = "border-color-$color";
$tabsT->selectedBgColorClass = "background-color-$color";
$tabsT->unselectedBgColorClass = "background-mute";
$tabsT->status = $status;
$contentT->content .= $tabsT->render();

// Show the orders table
$tableT = new Template("templates/cart/table.php");
$tableT->orders = $orders;
$tableT->status = $status;
$tableT->search = @$_GET['search'];
$tableT->colorClass = "fore-color-$color";
$tableT->pagination_length = $pagination_length;
$tableT->pagination_start = $pagination_start;
$tableT->reminders = $reminders;
$contentT->content .= $tableT->render();

if ( $evadeResult != null && strlen ( trim ( $evadeResult ) ) > 0 ) {

	$evadeResultContent = "<script> ";
	$evadeResultContent .= "console.log( '" . $evadeResult. "' ); ";
	$evadeResultContent .= "if ( confirm ( '" . l10n( "cart_evade_order_error_generic", "Error occured. Continue with order evasion?" ) . "' ) ) { ";
	$evadeResultContent .= "window.location.href += '&force=true';";
	$evadeResultContent .= "} ";
	$evadeResultContent .= "</script>";

	$contentT->content .= $evadeResultContent;
}

$mainT->content = $contentT->render();

echo $mainT->render();

