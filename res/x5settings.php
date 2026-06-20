<?php

/*
|-------------------------------
|	GENERAL SETTINGS
|-------------------------------
*/

$imSettings['general'] = array(
	'site_id' => 'E7158431A3B1D6F94AFD52AEDFD67D53',
	'url' => 'https://assurancetemporaireauto.com/',
	'homepage_url' => 'https://assurancetemporaireauto.com/index.html',
	'icon' => '',
	'version' => '2026.2.2.0',
	'sitename' => 'assurancetemporaireauto.com',
	'lang_code' => 'fr-FR',
	'rtl' => false,
	'public_folder' => '',
	'salt' => 'p4hm04oxqupvbjlzjczhaykw5l624z6keos461k7mgeqz33a23q50chrk',
	'common_email_sender_addres' => 'administrateur@australdev.eu',
	'enable_sender_header' => true,
	'date_format' => 'dd MMM yyyy',
	'date_format_ext' => 'dddd dd MMM yyyy',
	'date_format_no_day' => 'MMM yyyy',
	'date_format_no_day_ext' => 'MMM yyyy'
);
/*
|-------------------------------
|	BREAKPOINTS
|-------------------------------
*/

$imSettings['breakpoints'] = array(
	array("name" => "Desktop", "hash" => "ea2f0ee4d5cbb25e1ee6c7c4378fee7b", "start" => "max", "end" => 1150.0, "fluid" => false),
	array("name" => "Breakpoint 1", "hash" => "d2f9bff7f63c0d6b7c7d55510409c19b", "start" => 1149.9, "end" => 720.0, "fluid" => false),
	array("name" => "Mobile", "hash" => "72e5146e7d399bc2f8a12127e43469f1", "start" => 719.9, "end" => 480.0, "fluid" => false),
	array("name" => "Mobile Fluid", "hash" => "5ecdcca63de80fd3d4fbb36295d22b7d", "start" => 479.9, "end" => 0.0, "fluid" => true),
);
/*
|-------------------------------
|	PASSWORD POLICY
|-------------------------------
*/

$imSettings['password_policy'] = array(
	'required_policy' => false,
	'minimum_characters' => '6',
	'include_uppercase' => false,
	'include_numeric' => false,
	'include_special' => false
);
/*
|-------------------------------
|	Captcha
|-------------------------------
*/ImTopic::$captcha_code = "		<div class=\"x5captcha-wrap\">
			<label for=\"eaoixxc5-imCpt\">Code de sécurité :</label><br />
			<input type=\"text\" id=\"eaoixxc5-imCpt\" class=\"imCpt\" name=\"imCpt\" maxlength=\"5\" />
		</div>
";


$imSettings['admin'] = array(
	'icon' => 'admin/images/logo_21jdgunf.png',
	'notification_public_key' => 'BATkV1Q31SKS5-6ZPs7R2i-nQc_Ec4GWxnj74EySvK_ZJhuYzL5oYdph6tN1ErvPKYkWEkU1Hyhz5wloMWb8B2I',
	'notification_private_key' => 'Jc95jpDx_Q69mUmqRURR0mu_g7ddIkMLokx1Kzzzm4E',
	'notification_dbprefix' => 'w5_ad1c1560_notifications_',
	'enable_notifications' => false,
	'theme' => 'orange',
	'extra-dashboard' => array(),
	'extra-links' => array()
);


/*
|--------------------------------------------------------------------------------------
|	DATABASES SETTINGS
|--------------------------------------------------------------------------------------
*/

$imSettings['databases'] = array();
$ecommerce = Configuration::getCart();
// Setup the coupon data
$couponData = array();
$couponData['products'] = array();
// Setup the cart
$ecommerce->setPublicFolder('');
$ecommerce->setCouponData($couponData);
$ecommerce->setSettings(array(
	'page_url' => 'https://assurancetemporaireauto.com/',
	'force_sender' => false,
	'mail_btn_css' => 'display: inline-block; text-decoration: none; color: rgba(255, 255, 255, 1); background-color: rgba(255, 101, 1, 1); padding: 5px; border: solid; border-block-color: rgba(55, 71, 79, 1) rgba(55, 71, 79, 1); border-inline-color: rgba(55, 71, 79, 1) rgba(55, 71, 79, 1); border-width: 0px; border-radius: 0px; ',
	'email_opening' => 'Cher/chère client(e),<br /><br />Nous vous remercions de votre commande. Nous vous rappelons que le paiement n\'a pas encore été reçu.<br /><br />Vous trouverez ci-dessous la liste des produits commandés, les informations de facturation et de livraison les instructions pour effectuer le paiement.',
	'email_closing' => 'Nous contacter pour obtenir de plus amples informations.<br /><br />Nos meilleures salutations, Service commercial.',
	'email_payment_opening' => 'Cher/chère client(e),<br /><br />Nous vous remercions de votre achat, on vous confirme qu\'on a correctement reçu le paiement et que votre commande sera traitée dès que possible.<br /><br />Vous trouverez ci-dessous la liste des produits commandés et les informations de facturation et de livraison.',
	'email_payment_closing' => 'Nous restons à votre disposition pour toute information supplémentaire.<br /><br />Cordialement,<br />l’Équipe Commerciale<br />',
	'email_digital_shipment_opening' => 'Bonjour,<br /><br />Nous vous remercions pour votre achat et nous avons le plaisir de vous envoyer la liste des liens de téléchargement correspondant aux produits commandés :<br />',
	'email_digital_shipment_closing' => 'Nous restons à votre disposition pour toute information supplémentaire.<br /><br />Cordialement,<br />l’Équipe Commerciale<br />',
	'email_physical_shipment_opening' => 'Bonjour,<br /><br />Nous vous remercions pour votre achat et nous avons le plaisir de vous envoyer la liste des produits envoyés :',
	'email_physical_shipment_closing' => 'Nous restons à votre disposition pour toute information supplémentaire.<br /><br />Cordialement,<br />l’Équipe Commerciale',
	'sendEmailBeforePayment' => true,
	'sendEmailAfterPayment' => false,
	'useCSV' => false,
	'header_bg_color' => 'rgba(37, 58, 88, 1)',
	'header_text_color' => 'rgba(255, 255, 255, 1)',
	'cell_bg_color' => 'rgba(255, 255, 255, 1)',
	'cell_text_color' => 'rgba(0, 0, 0, 1)',
	'availability_reduction_type' => 1,
	'border_color' => 'rgba(211, 211, 211, 1)',
	'owner_email' => '',
	'vat_type' => 'included',
	'availability_image' => ''
));

$ecommerce->setPriceFormatData(array(
	'decimals' => 2,
	'decimal_sep' => '.',
	'thousands_sep' => '',
	'currency_to_right' => true,
	'currency_separator' => ' ',
	'show_zero_as' => '0',
	'currency_symbol' => '€',
	'currency_code' => 'EUR',
	'currency_name' => 'Euro',
));

$ecommerce->setDigitalProductsData(array());
$ecommerce->setProductsData(array());
$ecommerce->setSlugToProductIdMap(array());
$ecommerce->setCategoriesData(array(
	'unqwbo53' => array(
		'id' => 'unqwbo53',
		'name' => 'Nouvelle catégorie',
		'containsProductsWithProductPage' => false,
		'products' => array(),
		'categories' => array()
	)
));
$ecommerce->setCommentsData(array(
	'enabled' => false,
	'type' => "websitex5",
	'db' => '',
	'table' => 'w5_ad1c1560_products_comments',
	'prefix' => 'x5productPage_',
	'comment_type' => "commentandstars"
));
$ecommerce->setPaymentData(array(
	'8dkejfu5' => array(
		'id' => '8dkejfu5',
		'name' => 'Virement bancaire',
		'description' => 'Payer plus tard par virement bancaire.',
		'email_text' => 'Les données requises pour le paiement par virement bancaire sont les suivantes :

XXX YYY ZZZ

Remarque : au terme du paiement, il est nécessaire d\'envoyer une copie du reçu avec le Numéro de la commande.',
		'enableAfterPaymentEmail' => false
	)));
$ecommerce->setShippingData(array(
	'j48dn4la' => array(
		'id' => 'j48dn4la',
		'name' => 'Courrier',
		'description' => 'Les produits seront livrés dans 3-5 jours.',
		'email_text' => 'Expédition par Courrier.\\nLes produits seront livrés dans 3-5 jours.',
		'tracking_type' => 'none'
	),
	'hdj47dut' => array(
		'id' => 'hdj47dut',
		'name' => 'Livraison express',
		'description' => 'Les produits seront livrés dans 1-2 jours.',
		'email_text' => 'Expédition par Livraison express.\\nLes produits seront livrés dans 1-2 jours.',
		'tracking_type' => 'none'
	)));

/*
|-------------------------------------------------------------------------------------------
|	GUESTBOOK SETTINGS
|-------------------------------------------------------------------------------------------
*/

$imSettings['guestbooks'] = array();

/*
|-------------------------------------------------------------------------------------------
|	Dynamic Objects SETTINGS
|-------------------------------------------------------------------------------------------
*/

$imSettings['dynamicobjects'] = array(	'template' => array(
),
	'pages' => array(

	));


/*
|-------------------------------
|	EMAIL SETTINGS
|-------------------------------
*/

$ImMailer->emailType = 'phpmailer';
$ImMailer->exposeWsx5 = false;
$ImMailer->header = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">' . "\n" . '<html>' . "\n" . '<head>' . "\n" . '<meta http-equiv="content-type" content="text/html; charset=utf-8">' . "\n" . '</head>' . "\n" . '<body bgcolor="#37474F" style="background-color: #37474F;">' . "\n\t" . '<table border="0" cellpadding="0" align="center" cellspacing="0" style="padding: 0; margin: 0 auto; width: 700px; border-collapse: separate;">' . "\n\t" . '<tr><td id="imEmailContent" style="min-height: 300px; font: normal normal normal calc(9pt - max(9pt - var(--min-text-size), 0pt) * var(--font-size-factor)) \'PT Sans Narrow\'; color: #000000; background-color: #FFFFFF; text-decoration: none; text-align: left; width: 700px; border-style: solid; border-color: rgba(0, 0, 0, 1) rgba(0, 0, 0, 1) rgba(0, 0, 0, 1) rgba(0, 0, 0, 1); border-top-width: 1px; border-right-width: 1px; border-bottom-width: 0; border-bottom: none; border-left-width: 1px;  padding-top: 25px;  padding-bottom: 25px; padding-left: 25px; padding-right: 25px;  background-color: #FFFFFF" width="700px">' . "\n\t\t";
$ImMailer->footer = "\n\t" . '</td></tr>' . "\n\t" . '<tr><td id="imEmailIcons" style="background-color: #FFFFFF;border-left: 1px solid rgba(0, 0, 0, 1); border-right: 1px solid rgba(0, 0, 0, 1); border-bottom-style: solid; border-bottom-color: #000000; border-bottom-width: 1px; border-bottom-left-radius: 0px; border-bottom-right-radius: 0px;  padding-top: 25px;  padding-bottom: 25px; padding-left: 15px; padding-right: 15px;  text-align: center;  min-height: 300px; " width="700"></td></tr>' . "\n\t" . '</table>' . "\n" . '<table width="100%"><tr><td id="imEmailFooter" style="font: normal normal normal calc(7pt - max(7pt - var(--min-text-size), 0pt) * var(--font-size-factor)) \'PT Sans Narrow\'; color: #FFFFFF; background-color: transparent; text-decoration: none; text-align: center;  margin-top: 5px; padding-top: 25px;  padding-bottom: 25px; padding-left: 25px; padding-right: 25px; background-color: transparent">' . "\n\t\t" . 'Ce courriel fournit des informations destinées uniquement au destinataire susmentionné.<br>Si vous n\'êtes par le destinataire de ce message, veuillez le signaler immédiatement à l\'expéditeur et le détruire, sans le copier.' . "\n\t" . '</td></tr></table>' . "\n\t" . '</body>' . "\n" . '</html>';
$ImMailer->bodyBackground = '#FFFFFF';
$ImMailer->bodyBackgroundEven = '#FFFFFF';
$ImMailer->bodyBackgroundOdd = '#F0F0F0';
$ImMailer->bodyBackgroundBorder = '#CDCDCD';
$ImMailer->bodyTextColorOdd = '#000000';
$ImMailer->bodySeparatorBorderColor = '#000000';
$ImMailer->emailBackground = '#37474F';
$ImMailer->emailContentStyle = 'font: normal normal normal calc(9pt - max(9pt - var(--min-text-size), 0pt) * var(--font-size-factor)) \'PT Sans Narrow\'; color: #000000; background-color: #FFFFFF; text-decoration: none; text-align: left; ';
$ImMailer->emailContentFontFamily = 'font-family: PT Sans Narrow;';

// End of file x5settings.php