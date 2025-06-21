<?php
ini_set('default_socket_timeout', 1200);
ini_set('post_max_size', '64M');
ini_set('upload_max_filesize', '64M');
set_time_limit(0);

// Include markdown converter
require_once 'markdown_converter.php';

$ctx = stream_context_create(array('http'=>
    array(
        'timeout' => 1200,  //1200 Seconds is 20 Minutes
    )
));

$folderName = './uploads/';
if (file_exists($folderName)) {
    foreach (new DirectoryIterator($folderName) as $fileInfo) {
        if ($fileInfo->isDot()) {
            continue;
        }
        if ($fileInfo->isFile() && time() - $fileInfo->getCTime() >= 2*24*60*60) {
            unlink($fileInfo->getRealPath());
        }
    }
}

if(!(isset($_POST['Titel']) && isset($_POST['Author']) && isset($_POST['Verlag']) && isset($_POST['Thema']) && isset($_POST['Themen']))) exit();

$themen = explode(PHP_EOL, $_POST['Themen']);
foreach($themen as $i => $t) $themen[$i] = trim($t);
$titel = $_POST['Titel'];
$author = $_POST['Author'];
$verlag = $_POST['Verlag'];
$thema = $_POST['Thema'];

// Generate book content using Python AI generator
try {
    $command = "python3 ai_generator.py book " . 
               escapeshellarg($author) . " " . 
               escapeshellarg($thema) . " " . 
               "German";
    
    $output = shell_exec($command . " 2>&1");
    if ($output === null) {
        throw new Exception("Failed to execute Python script");
    }
    
    $book_data = json_decode($output, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception("Invalid JSON response from Python script");
    }
    
    if (isset($book_data['error'])) {
        throw new Exception($book_data['error']);
    }
    
    // Use generated book title if available
    if (!empty($book_data['title'])) {
        $titel = $book_data['title'];
    }
    
    // Download cover image if available
$bild = './uploads/'.uniqid().'.png';
    if (!empty($book_data['cover_image'])) {
        $bilddaten = file_get_contents($book_data['cover_image'], false, $ctx);
        if ($bilddaten !== false) {
            file_put_contents($bild, $bilddaten, false, $ctx);
        }
    }
    
} catch (Exception $e) {
    // Fallback to original method if AI generation fails
    $bild = './uploads/'.uniqid().'.png';
$bilddaten = file_get_contents("https://askgpt.bilke-projects.com/image_1.php?".http_build_query(array("ask" => $thema)), false, $ctx);
file_put_contents($bild, $bilddaten, false, $ctx);

    // Load existing content files
foreach($themen as $t) 
if($t) {
 $text[$t] = file_get_contents('uploads/'.$t, false, $ctx);
    }
}

$html = '
<html>
<head>
<style>'.file_get_contents('css/document-style.css').'</style>
</head>

<body>
<div class="site">
<h1 align="center">'.$titel.'</h1>
<div style="text-align:center; align-items:center;">
<img src="'.$bild.'" style="width:80%;" width="400">
</div>
<p style="text-align:right;"><strong>Datum: </strong>'.date("d.m.y").'</p>
<p style="text-align:right;"><strong>Autor: </strong>'.$author.'</p>
<p style="text-align:right;"><strong>Verlag: </strong>'.$verlag.'</p>
</div>
<br pagebreak="true"/>
<div class="site">
<h1>Inhaltsverzeichnis</h1>
';

// Use AI-generated table of contents if available
if (isset($book_data['table_of_contents'])) {
    $html .= '<div>'.MarkdownConverter::convertSafe($book_data['table_of_contents']).'</div>';
} else {
    // Fallback to original table of contents
    $html .= '<ol>
    <li>Einleitung</li>';

foreach($themen as $i => $t) 
if($t && !str_contains($t, 'vorwort') && !str_contains($t, 'nachwort'))
  $html .= '<li>Kapitel '.($i).': '.str_replace(".html", "", $t).'</li>';

$html .= '
<li>Schluss</li>
    </ol>';
}

$html .= '</div>';

// Add chapters
if (isset($book_data['chapters'])) {
    // Use AI-generated chapters
    foreach ($book_data['chapters'] as $i => $chapter) {
        $html .= '
        <br pagebreak="true"/>
        <div class="site">
        <h1>Kapitel '.($i+1).': '.htmlspecialchars($chapter['title']).'</h1>';
        
        if (!empty($chapter['image'])) {
            $html .= '<div style="text-align:center; margin: 20px 0;">
            <img src="'.htmlspecialchars($chapter['image']).'" style="max-width: 80%; height: auto;">
            </div>';
        }
        
        $html .= '<blockquote>'.MarkdownConverter::convertSafe($chapter['content']).'</blockquote>
        </div>';
    }
} else {
    // Fallback to original chapters
foreach($themen as $i => $t) 
if($t && str_contains($t, 'vorwort'))
$html .= '
<br pagebreak="true"/>
<div class="site">
<h1>Einleitung</h1>
<blockquote>'.$text[$t].'</blockquote>
    </div>';

foreach($themen as $i => $t) 
if($t && !str_contains($t, 'vorwort') && !str_contains($t, 'nachwort')) {
$html .= '
<br pagebreak="true"/>
<div class="site">
<h1>Kapitel '.($i).': '.str_replace(".html", "", $t).'</h1>
<blockquote>'.str_replace("<form", '<form action="#"', $text[$t]).'</blockquote>
</div>';
    }
}

// Add afterword
if (isset($book_data['afterword'])) {
    $html .= '
    <br pagebreak="true"/>
    <div class="site">
    <h1>Nachwort</h1>
    <blockquote>'.MarkdownConverter::convertSafe($book_data['afterword']).'</blockquote>
    </div>';
} else {
    // Fallback to original afterword
foreach($themen as $i => $t) 
if($t && str_contains($t, 'nachwort'))
$html .= '
<br pagebreak="true"/>
<div class="site">
<h1>Schluss</h1>
<blockquote>'.$text[$t].'</blockquote>
    </div>';
}

$html .= '</body>
</html>';

// Include the main TCPDF library (search for installation path).
define('K_PATH_MAIN', '/var/www/vhosts/bilke-projects.com/buchgenerator.bilke-projects.com/tcpdf/');
define('K_PATH_IMAGES', '/var/www/vhosts/bilke-projects.com/buchgenerator.bilke-projects.com/uploads/');
require_once('tcpdf/tcpdf.php');

// Extend the TCPDF class to create custom Header and Footer
class MYPDF extends TCPDF {

    //Page header
    public function Header() {
        // Set font
        $this->SetFont('freesans', 'B', 18);
        // Title
        $this->Cell(0, 50, $GLOBALS['titel'].' | Author: '.$GLOBALS['author'], 0, false, 'C', 0, '', 0, false, 'M', 'M');
    }

    // Page footer
    public function Footer() {
        // Position at 15 mm from bottom
        $this->SetY(-15);
        // Set font
        $this->SetFont('freesans', 'I', 10);
        // Page number
        $this->Cell(0, 10, 'Seite '.$this->getAliasNumPage().'/'.$this->getAliasNbPages(), 0, false, 'C', 0, '', 0, false, 'T', 'M');
    }
}

// create new PDF document
$pdf = new MYPDF(PDF_PAGE_ORIENTATION, PDF_UNIT, PDF_PAGE_FORMAT, true, 'UTF-8', false);

// set document information
$pdf->SetCreator(PDF_CREATOR);
$pdf->SetAuthor($author);
$pdf->SetTitle($titel);
$pdf->SetSubject($thema);
$pdf->SetKeywords($thema);

// set default header data
$pdf->SetHeaderData(PDF_HEADER_LOGO, PDF_HEADER_LOGO_WIDTH, PDF_HEADER_TITLE, PDF_HEADER_STRING);

// set header and footer fonts
$pdf->setHeaderFont(Array(PDF_FONT_NAME_MAIN, '', PDF_FONT_SIZE_MAIN));
$pdf->setFooterFont(Array(PDF_FONT_NAME_DATA, '', PDF_FONT_SIZE_DATA));

// set default monospaced font
$pdf->SetDefaultMonospacedFont(PDF_FONT_MONOSPACED);

// set margins
$pdf->SetMargins(PDF_MARGIN_LEFT, PDF_MARGIN_TOP, PDF_MARGIN_RIGHT);
$pdf->SetHeaderMargin(PDF_MARGIN_HEADER);
$pdf->SetFooterMargin(PDF_MARGIN_FOOTER);

// set auto page breaks
$pdf->SetAutoPageBreak(TRUE, PDF_MARGIN_BOTTOM);

// set image scale factor
$pdf->setImageScale(PDF_IMAGE_SCALE_RATIO);

// ---------------------------------------------------------

// set font
$pdf->SetFont('freesans', 'B', 11);

// add a page
$pdf->AddPage();

// output the HTML content
$pdf->writeHTML($html, true, 0, true, 0);

// reset pointer to the last page
$pdf->lastPage();

// ---------------------------------------------------------

//Close and output PDF document
$pdf->Output('buch_'.uniqid().'.pdf', 'I');

?>
