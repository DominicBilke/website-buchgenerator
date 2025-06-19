<?php
/**
 * AskGPT Server - Image Generation Endpoint
 * 
 * This endpoint generates book cover images using OpenAI DALL-E API
 * Used for generating book cover images based on the main topic
 */

// Error handling
function handleError($message, $code = 500) {
    http_response_code($code);
    error_log("AskGPT Image Error: " . $message);
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
    // Create a descriptive prompt for book cover generation
    $dallePrompt = "Ein modernes, professionelles Buchcover zum Thema: {$ask}

Das Cover sollte enthalten:
- Moderne, saubere Gestaltung
- Passende Farben und Typografie
- Professionelles Layout
- Kein Text auf dem Bild (nur visuelle Elemente)
- Hochwertige, ansprechende Darstellung

Stil: Modern, minimalistisch, professionell";

    // Prepare the API request for DALL-E
    $url = 'https://api.openai.com/v1/images/generations';
    $data = [
        'prompt' => $dallePrompt,
        'n' => 1,
        'size' => '512x512'
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
    if (!$result || !isset($result['data'][0]['url'])) {
        handleError('Invalid response from OpenAI DALL-E API');
    }

    $imageUrl = $result['data'][0]['url'];

    // Download the generated image
    $ch = curl_init();
    curl_setopt_array($ch, [
        CURLOPT_URL => $imageUrl,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 60,
        CURLOPT_CONNECTTIMEOUT => 30,
        CURLOPT_FOLLOWLOCATION => true
    ]);

    $imageData = curl_exec($ch);
    $imageHttpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $imageError = curl_error($ch);
    curl_close($ch);

    if ($imageError) {
        handleError('Error downloading image: ' . $imageError);
    }

    if ($imageHttpCode !== 200) {
        handleError('Error downloading image (HTTP ' . $imageHttpCode . ')');
    }

    // Create uploads directory if it doesn't exist
    $uploadDir = '../uploads';
    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0755, true);
    }

    // Save the image with unique filename
    $filename = 'cover_' . uniqid() . '.png';
    $filepath = $uploadDir . '/' . $filename;
    
    if (file_put_contents($filepath, $imageData) === false) {
        handleError('Error saving image to disk');
    }

    // Set headers for image response
    header('Content-Type: image/png');
    header('Cache-Control: public, max-age=3600');
    header('Access-Control-Allow-Origin: *');
    header('Access-Control-Allow-Methods: GET');
    header('Access-Control-Allow-Headers: Content-Type');

    // Log the request (optional)
    error_log("AskGPT Image: Generated image for topic: " . substr($ask, 0, 100) . "... -> " . $filename);

    // Output the image
    echo $imageData;

} catch (Exception $e) {
    handleError('Unexpected error: ' . $e->getMessage());
}
?> 