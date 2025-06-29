<?php
/**
 * Enhanced Book Generator v2.0
 * Improved version with better error handling and cross-platform compatibility
 */

require_once 'config.php';
require_once 'markdown_converter.php';

// Set error handling
if (APP_DEBUG) {
    error_reporting(0);
    ini_set('display_errors', 1);
}

// Validate input
if (!isset($_POST['author']) || !isset($_POST['topics']) || !isset($_POST['language'])) {
    http_response_code(400);
    die(json_encode(['error' => 'Missing required fields: author, topics, language']));
}

$author = trim($_POST['author']);
$topics = trim($_POST['topics']);
$language = trim($_POST['language']);
$publisher = trim($_POST['publisher'] ?? 'AI Book Generator');

// Validate input
if (empty($author) || empty($topics)) {
    http_response_code(400);
    die(json_encode(['error' => 'Author and topics are required']));
}

// Sanitize inputs
$author = htmlspecialchars($author, ENT_QUOTES, 'UTF-8');
$topics = htmlspecialchars($topics, ENT_QUOTES, 'UTF-8');
$language = htmlspecialchars($language, ENT_QUOTES, 'UTF-8');
$publisher = htmlspecialchars($publisher, ENT_QUOTES, 'UTF-8');

try {
    // Generate book content using Python AI generator
    $command = sprintf(
        '%s %s book %s %s %s',
        PYTHON_COMMAND,
        escapeshellarg(PYTHON_SCRIPT),
        escapeshellarg($author),
        escapeshellarg($topics),
        escapeshellarg($language)
    );
    
    $output = shell_exec($command . " 2>&1");
    
    if ($output === null) {
        throw new Exception("Failed to execute Python script");
    }
    
    $book_data = json_decode($output, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception("Invalid JSON response from Python script: " . substr($output, 0, 200));
    }
    
    if (isset($book_data['error'])) {
        throw new Exception($book_data['error']);
    }
    
    // Download cover image if available
    $cover_image_path = '';
    if (!empty($book_data['cover_image'])) {
        $cover_image_path = downloadImage($book_data['cover_image'], 'cover');
    }
    
    // Download chapter images
    if (isset($book_data['chapters'])) {
        foreach ($book_data['chapters'] as &$chapter) {
            if (!empty($chapter['image'])) {
                $chapter['local_image'] = downloadImage($chapter['image'], 'chapter');
            }
        }
    }
    
    // Generate PDF
    $pdf_filename = generatePDF($book_data, $author, $publisher, $cover_image_path);
    
    // Return success response
    echo json_encode([
        'success' => true,
        'pdf_url' => 'uploads/' . $pdf_filename,
        'book_data' => [
            'title' => htmlentities($book_data['title']),
            'author' => htmlentities($book_data['author']),
            'total_words' => htmlentities($book_data['total_words']),
            'chapter_count' => htmlentities($book_data['chapter_count'])
        ]
    ]);
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'error' => $e->getMessage(),
        'timestamp' => date('Y-m-d H:i:s')
    ]);
}

/**
 * Download image from URL and save locally
 */
function downloadImage($image_url, $type) {
    $ctx = stream_context_create([
        'http' => [
            'timeout' => 60,
            'user_agent' => 'BookGenerator/2.0'
        ]
    ]);
    
    $image_data = file_get_contents($image_url, false, $ctx);
    if ($image_data === false) {
        return '';
    }
    
    $filename = $type . '_' . uniqid() . '.png';
    $filepath = UPLOADS_PATH . '/' . $filename;
    
    if (file_put_contents($filepath, $image_data) === false) {
        return '';
    }
    
    return $filepath;
}

/**
 * Generate PDF from book data
 */
function generatePDF($book_data, $author, $publisher, $cover_image_path) {
    // Include TCPDF
    require_once(TCPDF_PATH . '/tcpdf.php');
    
    // Create custom PDF class
    class BookPDF extends TCPDF {
        private $book_title;
        private $book_author;
        
        public function __construct($title, $author) {
            parent::__construct(PDF_PAGE_ORIENTATION, PDF_UNIT, PDF_PAGE_FORMAT, true, 'UTF-8', false);
            $this->book_title = $title;
            $this->book_author = $author;
        }
        
        public function Header() {
            if ($this->getPage() > 1) {
                $this->SetFont(PDF_FONT_NAME, 'B', 8);
                $this->Cell(0, 10, $this->book_title, 0, false, 'C');
            }
        }
        
        public function Footer() {
            $this->SetY(-15);
            $this->SetFont(PDF_FONT_NAME, 'I', 8);
            $this->Cell(0, 10, 'Page ' . $this->getAliasNumPage() . '/' . $this->getAliasNbPages(), 0, false, 'C');
        }
    }
    
    // Create PDF
    $pdf = new BookPDF($book_data['title'], $book_data['author']);
    
    // Set document information
    $pdf->SetCreator(APP_NAME . ' v' . APP_VERSION);
    $pdf->SetAuthor($book_data['author']);
    $pdf->SetTitle($book_data['title']);
    $pdf->SetSubject(implode(', ', $book_data['topics']));
    $pdf->SetKeywords(implode(', ', $book_data['topics']));
    
    // Set margins
    $pdf->SetMargins(PDF_MARGIN_LEFT, PDF_MARGIN_TOP, PDF_MARGIN_RIGHT);
    //$pdf->SetHeaderMargin(PDF_MARGIN_TOP);
    //$pdf->SetFooterMargin(PDF_MARGIN_BOTTOM);
    
    // Set auto page breaks
    $pdf->SetAutoPageBreak(TRUE, PDF_MARGIN_BOTTOM);
    
    // Set image scale factor
    $pdf->setImageScale(PDF_IMAGE_SCALE_RATIO);
    
    // Set font
    $pdf->SetFont(PDF_FONT_NAME, '', PDF_FONT_SIZE);
    
    // Add cover page
    $pdf->AddPage();
    $pdf->SetFont(PDF_FONT_NAME, 'B', 12);
    $pdf->writeHTML('<br/><br/><br/><div style="text-align: center; line-height: 1.6;">'.MarkdownConverter::convertSafe($book_data['title']).'</div>', true, false, true, false, '');
    // $pdf->Cell(0, 30, '', 0, 1, 'C');
    $pdf->Cell(0, 10, 'By ' . $book_data['author'], 0, 1, 'R');
    $pdf->Cell(0, 10, $publisher, 0, 1, 'R');
    $pdf->Cell(0, 10, date('F Y'), 0, 1, 'R');
    
    if ($cover_image_path && file_exists($cover_image_path)) {
        $pdf->Image($cover_image_path, 30, 120, 150);
    }
    
    

    // Add table of contents
    $pdf->AddPage();
    $pdf->SetFont(PDF_FONT_NAME, 'B', 12);
    $pdf->Cell(0, 10, 'Table of Contents', 0, 1, 'L');
    $pdf->SetFont(PDF_FONT_NAME, '', 12);
    
    $toc_lines = explode("\n", $book_data['table_of_contents']);
    foreach ($toc_lines as $line) {
        $line = trim($line);
        if (!empty($line)) {
            $pdf->Cell(0, 8, $line, 0, 1, 'L');
        }
    }
    
    // Add chapters
    foreach ($book_data['chapters'] as $i => $chapter) {
        $pdf->AddPage();
        
        // Chapter title
        // $pdf->SetFont(PDF_FONT_NAME, 'B', 12);
        // $pdf->Cell(0, 10, 'Chapter ' . ($i + 1) . ': ' . $chapter['title'], 0, 1, 'L');
        // $pdf->Ln(5);
        
        // Chapter image
        if (!empty($chapter['local_image']) && file_exists($chapter['local_image'])) {
            $pdf->Image($chapter['local_image'], 30, $pdf->GetY(), 0, 150, resize: true, dpi: 300, align: 'C');
            $pdf->Ln(60);
        }
        
        // Chapter content
        $pdf->SetFont(PDF_FONT_NAME, '', 12);
        $pdf->writeHTML('<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><div style="text-align: justify; line-height: 1.6;">' . 
                       MarkdownConverter::convertSafe($chapter['content']) . '</div>', true, false, true, false, '');
    }
    
    // Add afterword
    if (!empty($book_data['afterword'])) {
        $pdf->AddPage();
        //$pdf->SetFont(PDF_FONT_NAME, 'B', 12);
        //$pdf->Cell(0, 10, 'Afterword', 0, 1, 'L');
        //$pdf->Ln(5);
        
        $pdf->SetFont(PDF_FONT_NAME, '', 12);
        $pdf->writeHTML('<div style="text-align: justify; line-height: 1.6;">' . 
                       MarkdownConverter::convertSafe($book_data['afterword']) . '</div>', true, false, true, false, '');
    }
    
    // Generate filename and save
    $filename = 'book_' . uniqid() . '.pdf';
    $filepath = UPLOADS_PATH . '/' . $filename;
    
    $pdf->Output($filepath, 'F');
    
    return $filename;
}
?> 