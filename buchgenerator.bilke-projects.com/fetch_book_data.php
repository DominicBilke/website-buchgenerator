<?php
require_once 'config.php';
require_once 'markdown_converter.php';

header("Access-Control-Allow-Origin: *");
header('Content-Type: application/json; charset=utf-8');

function call_python_script($command) {
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
    
return $result;
}

ini_set('default_socket_timeout', 1200);
set_time_limit(0);

$ctx = stream_context_create(array('http'=>
    array(
        'timeout' => 1200,  //1200 Seconds is 20 Minutes
    )
));

$_GET['Thema'] = str_replace('.html', '', $_GET['Thema']);

try {
if(isset($_GET['Vorwort'])) {
        $prompt = 'Write a detailed introduction for the topic "' . $_GET['Thema'] . '" in ' . $_GET['Sprache'] . '!';
        $command = "python3 ai_generator.py text " . escapeshellarg($prompt);
        $result = call_python_script($command);
        
        $texthtml = $result['text'];
	file_put_contents('uploads/'.$_GET['Thema'].'_vorwort.html', $texthtml, false, $ctx);
        echo json_encode(['success' => true, 'file' => $_GET['Thema'].'_vorwort.html']);
}
else if(isset($_GET['Nachwort'])) {
        $prompt = 'Write a detailed finish for the topic "' . $_GET['Thema'] . '" in ' . $_GET['Sprache'] . '!';
        $command = "python3 ai_generator.py text " . escapeshellarg($prompt);
        $result = call_python_script($command);
        
        $texthtml = $result['text'];
	file_put_contents('uploads/'.$_GET['Thema'].'_nachwort.html', $texthtml, false, $ctx);
        echo json_encode(['success' => true, 'file' => $_GET['Thema'].'_nachwort.html']);
}
else if(isset($_GET['Thema'])) {
        // Generate complete book content
        $author = $_GET['Autor'] ?? 'Unknown Author';
        $topics = $_GET['Thema'];
        $language = $_GET['Sprache'] ?? 'German';
        
        $command = "python3 ai_generator.py book " . 
                   escapeshellarg($author) . " " . 
                   escapeshellarg($topics) . " " . 
                   escapeshellarg($language);
        
        $result = call_python_script($command);
        
        // Save the complete book data as JSON
        $book_data = json_encode($result, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        file_put_contents('uploads/'.$_GET['Thema'].'_book_data.json', $book_data, false, $ctx);
        
        // Also save as HTML for backward compatibility
        $html_content = "<h1>" . htmlspecialchars($result['title']) . "</h1>";
        $html_content .= "<h2>By " . htmlspecialchars($result['author']) . "</h2>";
        $html_content .= "<h3>Table of Contents</h3>";
        $html_content .= "<div>" . nl2br(htmlspecialchars($result['table_of_contents'])) . "</div>";
        
        foreach ($result['chapters'] as $chapter) {
            $html_content .= "<h2>" . htmlspecialchars($chapter['title']) . "</h2>";
            if (!empty($chapter['image'])) {
                $html_content .= "<img src='" . htmlspecialchars($chapter['image']) . "' alt='Chapter Image' style='max-width: 100%; height: auto;'><br><br>";
            }
            $html_content .= "<div>" . MarkdownConverter::convertSafe($chapter['content']) . "</div>";
        }
        
        $html_content .= "<h2>Afterword</h2>";
        $html_content .= "<div>" . MarkdownConverter::convertSafe($result['afterword']) . "</div>";
        
        file_put_contents('uploads/'.$_GET['Thema'].'.html', $html_content, false, $ctx);
        
        echo json_encode([
            'success' => true, 
            'file' => $_GET['Thema'].'.html',
            'book_data' => $result
        ]);
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'error' => $e->getMessage(),
        'timestamp' => date('Y-m-d H:i:s')
    ]);
}
?>