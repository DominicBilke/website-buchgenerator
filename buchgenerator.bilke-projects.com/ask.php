<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

// Get the request data
$input = json_decode(file_get_contents('php://input'), true);
$prompt = $input['prompt'] ?? $_GET['prompt'] ?? '';

if (empty($prompt)) {
    http_response_code(400);
    echo json_encode(['error' => 'Prompt is required']);
    exit;
}

try {
    // Call the Python script
    $command = "python3 ai_generator.py text " . escapeshellarg($prompt);
    $output = shell_exec($command . " 2>&1");
    
    if ($output === null) {
        throw new Exception("Failed to execute Python script");
    }
    
    $result = json_decode($output, true);
    
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception("Invalid JSON response from Python script: " . $output);
    }
    
    if (isset($result['error'])) {
        throw new Exception($result['error']);
    }
    
    echo json_encode([
        'success' => true,
        'text' => $result['text'] ?? '',
        'timestamp' => date('Y-m-d H:i:s')
    ]);
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'error' => $e->getMessage(),
        'timestamp' => date('Y-m-d H:i:s')
    ]);
}
?> 