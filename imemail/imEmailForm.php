<?php
if(substr(basename($_SERVER['PHP_SELF']), 0, 11) == "imEmailForm") {
	include '../res/x5engine.php';
	$form = new ImForm();

	$errorMessage = '';
	if(@$_POST['action'] != 'check_answer') {
	$form->setField('Nom', @$_POST['imObjectForm_21_1'], '', false);
	$form->setField('Numéro de téléphone', @$_POST['imObjectForm_21_2'], '', false);
	$form->setField('Adresse Mail', @$_POST['imObjectForm_21_3'], '', false);
	$form->setField('Votre Message', @$_POST['imObjectForm_21_4'], '', false);
		if(!isset($_POST['imJsCheck']) || $_POST['imJsCheck'] != '1B23A5438F4AD81E11060EE4C25611E4' || (isset($_POST['imSpProt']) && $_POST['imSpProt'] != ""))
			die(imPrintJsError());
		$form->mailToOwner('administrateur@australdev.eu', $_POST['imObjectForm_21_3'] != '' ? $_POST['imObjectForm_21_3'] : 'contact@mcj-courtage.com', 'contact@mcj-courtage.com', 'Mail provenant du site assurancetemporaireauto.com', "Ce message est adressé par le site \"Assurancetemporaireauto.com\"", false);
		@header('Location: ../index.html');
		exit();
	} else {
		echo $form->checkAnswer(@$_POST['id'], @$_POST['answer']) ? 1 : 0;
	}
}

// End of file