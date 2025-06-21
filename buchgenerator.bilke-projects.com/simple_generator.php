<?php
/**
 * Simple Book Generator v2.0
 * A working version that can be easily tested and improved
 */

require_once 'config.php';
require_once 'markdown_converter.php';

// Basic configuration
$config = [
    'python_script' => 'simple_generator.py',
    'python_command' => 'python', // Change to 'python3' on Linux/Mac
    'uploads_dir' => 'uploads',
    'debug' => true
];

// Error handling
if ($config['debug']) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
}

// Create uploads directory if it doesn't exist
if (!is_dir($config['uploads_dir'])) {
    mkdir($config['uploads_dir'], 0755, true);
}

// Set headers for JSON response
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

// Function to clean up old files
function cleanupOldFiles($dir, $maxAge = 86400) { // 24 hours
    if (is_dir($dir)) {
        foreach (new DirectoryIterator($dir) as $fileInfo) {
            if ($fileInfo->isDot()) continue;
            if ($fileInfo->isFile() && time() - $fileInfo->getCTime() >= $maxAge) {
                unlink($fileInfo->getRealPath());
            }
        }
    }
}

// Clean up old files
cleanupOldFiles($config['uploads_dir']);

// Function to download image
function downloadImage($imageUrl, $uploadDir) {
    $context = stream_context_create([
        'http' => [
            'timeout' => 60,
            'user_agent' => 'BookGenerator/2.0'
        ]
    ]);
    
    $imageData = file_get_contents($imageUrl, false, $context);
    if ($imageData === false) {
        return '';
    }
    
    $filename = 'image_' . uniqid() . '.png';
    $filepath = $uploadDir . '/' . $filename;
    
    if (file_put_contents($filepath, $imageData) === false) {
        return '';
    }
    
    return $filepath;
}

// Function to generate PDF
function generatePDF($bookData, $uploadDir) {
    // Simple HTML to PDF conversion
    $html = '<!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #333; text-align: center; }
            h2 { color: #666; border-bottom: 2px solid #eee; padding-bottom: 10px; }
            .chapter { margin-bottom: 30px; }
            .image { text-align: center; margin: 20px 0; }
            .image img { max-width: 80%; height: auto; }
            .afterword { font-style: italic; background: #f9f9f9; padding: 20px; border-radius: 5px; }
        </style>
    </head>
    <body>';
    
    // Title page
    $html .= '<h1>' . htmlspecialchars($bookData['title']) . '</h1>';
    $html .= '<p style="text-align: center; font-size: 18px;">By ' . htmlspecialchars($bookData['author']) . '</p>';
    $html .= '<p style="text-align: center; color: #666;">Generated on ' . date('F j, Y') . '</p>';
    $html .= '<hr style="margin: 40px 0;">';
    
    // Chapters
    foreach ($bookData['chapters'] as $chapter) {
        $html .= '<div class="chapter">';
        $html .= '<h2>' . htmlspecialchars($chapter['title']) . '</h2>';
        
        if (!empty($chapter['image'])) {
            $html .= '<div class="image"><img src="' . htmlspecialchars($chapter['image']) . '" alt="Chapter Image"></div>';
        }
        
        $html .= '<div>' . MarkdownConverter::convertSafe($chapter['content']) . '</div>';
        $html .= '</div>';
    }
    
    // Afterword
    if (!empty($bookData['afterword'])) {
        $html .= '<div class="afterword">';
        $html .= '<h2>Afterword</h2>';
        $html .= '<div>' . MarkdownConverter::convertSafe($bookData['afterword']) . '</div>';
        $html .= '</div>';
    }
    
    $html .= '</body></html>';
    
    // Save as HTML file (can be converted to PDF later)
    $filename = 'book_' . uniqid() . '.html';
    $filepath = $uploadDir . '/' . $filename;
    
    if (file_put_contents($filepath, $html) === false) {
        throw new Exception('Failed to save book file');
    }
    
    return $filename;
}

// Main processing
try {
    // Validate input
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        throw new Exception('Only POST requests are allowed');
    }
    
    $input = json_decode(file_get_contents('php://input'), true);
    if (!$input) {
        $input = $_POST; // Fallback to POST data
    }
    
    if (empty($input['author']) || empty($input['topics'])) {
        throw new Exception('Author and topics are required');
    }
    
    $author = trim($input['author']);
    $topics = trim($input['topics']);
    $language = trim($input['language'] ?? 'English');
    
    // Sanitize inputs
    $author = htmlspecialchars($author, ENT_QUOTES, 'UTF-8');
    $topics = htmlspecialchars($topics, ENT_QUOTES, 'UTF-8');
    $language = htmlspecialchars($language, ENT_QUOTES, 'UTF-8');
    
    // Generate book using Python script
    $command = sprintf(
        '%s %s book %s %s %s',
        $config['python_command'],
        escapeshellarg($config['python_script']),
        escapeshellarg($author),
        escapeshellarg($topics),
        escapeshellarg($language)
    );
    
    $output = shell_exec($command . ' 2>&1');
    
    if ($output === null) {
        throw new Exception('Failed to execute Python script');
    }
    
    $bookData = json_decode($output, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception('Invalid JSON response from Python script: ' . substr($output, 0, 200));
    }
    
    if (isset($bookData['error'])) {
        throw new Exception($bookData['error']);
    }
    
    // Download images
    foreach ($bookData['chapters'] as &$chapter) {
        if (!empty($chapter['image'])) {
            $localImage = downloadImage($chapter['image'], $config['uploads_dir']);
            if ($localImage) {
                $chapter['local_image'] = $localImage;
            }
        }
    }
    
    // Generate PDF/HTML
    $filename = generatePDF($bookData, $config['uploads_dir']);
    
    // Return success response
    echo json_encode([
        'success' => true,
        'file_url' => $config['uploads_dir'] . '/' . $filename,
        'book_data' => [
            'title' => $bookData['title'],
            'author' => $bookData['author'],
            'chapter_count' => count($bookData['chapters']),
            'generated_at' => $bookData['generated_at']
        ]
    ]);
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'error' => $e->getMessage(),
        'timestamp' => date('Y-m-d H:i:s')
    ]);
}
?> 