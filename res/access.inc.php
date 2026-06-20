<?php

// Users data
$imSettings['access']['users'] = array(
	'info@example.com' => array(
		'id' => '5yj5h4td',
		'groups' => array('0zqq4lz4'),
		'firstname' => 'Admin',
		'lastname' => '',
		'email' => 'info@example.com',
		'password' => '$2a$11$AzjPvQ.KDx.uhyaqtbVWyehLDDhwA3mi3XWIK0YnJZ8PgUcNgNhri',
		'crypt_encoding' => 'csharp_bcrypt',
		'db_stored' => false,
		'page' => false
	)
);

// Admins list
$imSettings['access']['admins'] = array('5yj5h4td');

// Page/Users permissions
$imSettings['access']['pages'] = array();

// PASSWORD CRYPT

$imSettings['access']['password_crypt'] = array(
	'encoding_id' => 'php_default',
	'encodings' => array(
		'no_crypt' => array(
			'encode' => function ($pwd) { return $pwd; },
			'check' => function ($input, $encoded) { return $input == $encoded; }
		),
		'php_default' => array(
			'encode' => function ($pwd) { return password_hash($pwd, PASSWORD_DEFAULT); },
			'check' => function ($input, $encoded) { return password_verify($input, $encoded); }
		),
		'csharp_bcrypt' => array(
			'encode' => function ($pwd) { return password_hash($pwd, PASSWORD_BCRYPT); },
			'check' => function ($input, $encoded) { return password_verify($input, $encoded); }
		)
	)
);

// End of file access.inc.php