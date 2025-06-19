<?php
/**
 * AskGPT Server - Health Check Endpoint
 * 
 * This endpoint provides health status and system information
 */

// Set headers
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');
header('Access-Control-Allow-Headers: Content-Type');

// Get system information
$status = 'healthy';
$openaiKeyConfigured = !empty(getenv('OPENAI_API_KEY'));
$timestamp = date('c');

// Check if required extensions are available
$extensions = [
    'curl' => extension_loaded('curl'),
    'json' => extension_loaded('json')
];

$allExtensionsAvailable = array_reduce($extensions, function($carry, $loaded) {
    return $carry && $loaded;
}, true);

if (!$allExtensionsAvailable) {
    $status = 'unhealthy';
}

// Check if uploads directory is writable
$uploadsDir = '../uploads';
$uploadsWritable = is_dir($uploadsDir) && is_writable($uploadsDir);

if (!$uploadsWritable) {
    $status = 'degraded';
}

// Prepare response
$response = [
    'status' => $status,
    'timestamp' => $timestamp,
    'openai_key_configured' => $openaiKeyConfigured,
    'extensions' => $extensions,
    'uploads_writable' => $uploadsWritable,
    'server_info' => [
        'php_version' => PHP_VERSION,
        'server_software' => $_SERVER['SERVER_SOFTWARE'] ?? 'Unknown',
        'memory_limit' => ini_get('memory_limit'),
        'max_execution_time' => ini_get('max_execution_time')
    ]
];

// Set HTTP status code
if ($status === 'healthy') {
    http_response_code(200);
} elseif ($status === 'degraded') {
    http_response_code(200); // Still 200 but with degraded status
} else {
    http_response_code(503);
}

// Output JSON response
echo json_encode($response, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
?> 