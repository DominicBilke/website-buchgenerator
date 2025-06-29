<?php
/**
 * Configuration file for Book Generator
 * Centralized settings for the entire application
 */

// Application settings
define('APP_NAME', 'AI Book Generator');
define('APP_VERSION', '2.2.0');
define('APP_DEBUG', true);

// File paths (cross-platform compatible)
define('ROOT_PATH', __DIR__);
define('UPLOADS_PATH', ROOT_PATH . '/uploads');
define('TCPDF_PATH', ROOT_PATH . '/tcpdf');
define('CSS_PATH', ROOT_PATH . '/css');
define('IMG_PATH', ROOT_PATH . '/img');

// Python settings
define('PYTHON_SCRIPT', ROOT_PATH . '/ai_generator_v2.py');
define('PYTHON_COMMAND', 'python3'); // Change to 'python' on Windows if needed

// OpenAI settings
define('OPENAI_MODEL', 'gpt-4');
define('OPENAI_MAX_TOKENS', 2000);
define('OPENAI_TEMPERATURE', 0.7);
define('DALL_E_SIZE', '1024x1024');

// PDF settings
define('PDF_MARGIN_LEFT', 20);
define('PDF_MARGIN_TOP', 20);
define('PDF_MARGIN_RIGHT', 20);
define('PDF_MARGIN_BOTTOM', 20);
define('PDF_FONT_SIZE', 11);
define('PDF_FONT_NAME', 'freesans');

// File cleanup settings (in seconds)
define('FILE_CLEANUP_AGE', 2 * 24 * 60 * 60); // 2 days

// Error reporting
if (APP_DEBUG) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
} else {
    error_reporting(0);
    ini_set('display_errors', 0);
}

// Time limits
ini_set('max_execution_time', 1200); // 20 minutes
ini_set('default_socket_timeout', 1200);
ini_set('post_max_size', '64M');
ini_set('upload_max_filesize', '64M');

// Create uploads directory if it doesn't exist
if (!is_dir(UPLOADS_PATH)) {
    mkdir(UPLOADS_PATH, 0755, true);
}

// Clean up old files
function cleanupOldFiles() {
    if (is_dir(UPLOADS_PATH)) {
        foreach (new DirectoryIterator(UPLOADS_PATH) as $fileInfo) {
            if ($fileInfo->isDot()) continue;
            if ($fileInfo->isFile() && time() - $fileInfo->getCTime() >= FILE_CLEANUP_AGE) {
                unlink($fileInfo->getRealPath());
            }
        }
    }
}

// Run cleanup
cleanupOldFiles();
?> 