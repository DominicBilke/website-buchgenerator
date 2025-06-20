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
$topic = $input['topic'] ?? $_GET['topic'] ?? '';
$author = $input['author'] ?? $_GET['author'] ?? '';
$language = $input['language'] ?? $_GET['language'] ?? 'German';

if (empty($topic) || empty($author)) {
    http_response_code(400);
    echo json_encode(['error' => 'Topic and author are required']);
    exit;
}

try {
    // Call the Python script for topic-based content
    $topics_array = explode(',', $topic);
    $topics_json = json_encode($topics_array);
    
    $command = "python3 ai_generator.py book " . 
               escapeshellarg($author) . " " . 
               escapeshellarg($topic) . " " . 
               escapeshellarg($language);
    
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
        'book_data' => $result,
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