<?php

// autoload_static.php @generated by Composer

namespace Composer\Autoload;

class ComposerStaticInit05d0f9f59b4df4c80f809c1551d3db61
{
    public static $prefixLengthsPsr4 = array (
        'P' => 
        array (
            'PhpAmqpLib\\' => 11,
        ),
    );

    public static $prefixDirsPsr4 = array (
        'PhpAmqpLib\\' => 
        array (
            0 => __DIR__ . '/..' . '/php-amqplib/php-amqplib/PhpAmqpLib',
        ),
    );

    public static function getInitializer(ClassLoader $loader)
    {
        return \Closure::bind(function () use ($loader) {
            $loader->prefixLengthsPsr4 = ComposerStaticInit05d0f9f59b4df4c80f809c1551d3db61::$prefixLengthsPsr4;
            $loader->prefixDirsPsr4 = ComposerStaticInit05d0f9f59b4df4c80f809c1551d3db61::$prefixDirsPsr4;

        }, null, ClassLoader::class);
    }
}
