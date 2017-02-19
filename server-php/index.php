<?php

require_once __DIR__ . '/vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

echo " [x] Sending task \n";

$connection = new AMQPStreamConnection('192.168.99.100', 5672, 'guest', 'guest');
$channel = $connection->channel();

$channel->queue_declare('task_queue', false, true, false, false);

// get the HTTP method, path and body of the request
$method = $_SERVER['REQUEST_METHOD'];
$request = explode('/', trim($_SERVER['PATH_INFO'], '/'));
$input = json_decode(file_get_contents('php://input'), true);


$msg = new AMQPMessage($data,
                        array('delivery_mode' => 2) # make message persistent
                      );

$channel->basic_publish($msg, '', 'task_queue');

echo " [x] Sent ", $data, "\n";


$channel->close();
$connection->close();
