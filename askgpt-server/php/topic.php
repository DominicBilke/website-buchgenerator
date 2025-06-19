<?php
/**
 * AskGPT Server - Chapter Generation Endpoint
 * 
 * This endpoint generates chapter content using OpenAI GPT API
 * Used for generating main chapter content with structured format
 */

// Set headers
header('Content-Type: text/plain; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');
header('Access-Control-Allow-Headers: Content-Type');

// Error handling
function handleError($message, $code = 500) {
    http_response_code($code);
    error_log("AskGPT Topic Error: " . $message);
    echo "Error: " . $message;
    exit;
}

// Get OpenAI API key
$apiKey = getenv('OPENAI_API_KEY');
if (!$apiKey) {
    handleError('OpenAI API key not configured', 500);
}

// Get the 'ask' parameter
$ask = $_GET['ask'] ?? '';
if (empty($ask)) {
    handleError('Missing "ask" parameter', 400);
}

// Validate input
if (strlen($ask) > 1000) {
    handleError('Topic too long (max 1000 characters)', 400);
}

try {
    // Create a detailed prompt for chapter generation
    $prompt = "Schreibe ein ausführliches, informatives Kapitel zum Thema: {$ask}

Das Kapitel sollte enthalten:
- Eine klare Einführung zum Thema
- Detaillierte Erklärungen und Beispiele
- Praktische Anwendungen oder Fallstudien
- Eine Zusammenfassung der wichtigsten Punkte

Schreibe in einem professionellen, aber verständlichen Stil. Verwende Überschriften, Aufzählungspunkte und strukturierte Absätze für bessere Lesbarkeit.

Formatierung:
- Verwende <h2> für Hauptüberschriften
- Verwende <h3> für Unterüberschriften
- Verwende <ul> und <li> für Aufzählungen
- Verwende <p> für Absätze
- Verwende <strong> für wichtige Begriffe";

    // Prepare the API request
    $url = 'https://api.openai.com/v1/chat/completions';
    $data = [
        'model' => 'gpt-3.5-turbo',
        'messages' => [
            [
                'role' => 'system',
                'content' => 'Du bist ein erfahrener Fachautor. Schreibe strukturierte, informative Kapitel mit klarer Gliederung und HTML-Formatierung.'
            ],
            [
                'role' => 'user',
                'content' => $prompt
            ]
        ],
        'max_tokens' => 2048,
        'temperature' => 0.7
    ];

    // Make the API request
    $ch = curl_init();
    curl_setopt_array($ch, [
        CURLOPT_URL => $url,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode($data),
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $apiKey
        ],
        CURLOPT_TIMEOUT => 120,
        CURLOPT_CONNECTTIMEOUT => 30
    ]);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);

    if ($error) {
        handleError('cURL error: ' . $error);
    }

    if ($httpCode !== 200) {
        handleError('OpenAI API error (HTTP ' . $httpCode . '): ' . $response);
    }

    $result = json_decode($response, true);
    if (!$result || !isset($result['choices'][0]['message']['content'])) {
        handleError('Invalid response from OpenAI API');
    }

    // Return the generated chapter content
    $generatedText = trim($result['choices'][0]['message']['content']);
    
    // Log the request (optional)
    error_log("AskGPT Topic: Generated chapter for topic: " . substr($ask, 0, 100) . "...");
    
    echo $generatedText;

} catch (Exception $e) {
    handleError('Unexpected error: ' . $e->getMessage());
}
?> 