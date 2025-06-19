<?php
ini_set('default_socket_timeout', 1200);
set_time_limit(0);

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
$bild = './uploads/'.uniqid().'.png';

// Generate cover image
file_put_contents($bild, file_get_contents("https://bookgpt.bilke-projects.com/image_1.php?".http_build_query(array("ask" => $thema)), false, $ctx));

// Fetch content for each topic
foreach($themen as $t) 
if($t) {
 $text[$t] = file_get_contents('./uploads/'.$t, false, $ctx);
}

// Modern HTML template with contemporary styling
$html = '
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #2d3748;
            margin: 0;
            padding: 0;
        }
        .page-break {
            page-break-before: always;
        }
        .cover-page {
            text-align: center;
            padding: 60px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .cover-title {
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            line-height: 1.2;
        }
        .cover-image {
            max-width: 300px;
            max-height: 200px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            margin: 30px 0;
        }
        .cover-meta {
            margin-top: 40px;
            font-size: 1.1em;
            opacity: 0.9;
        }
        .cover-meta p {
            margin: 8px 0;
        }
        .content-page {
            padding: 40px;
            max-width: 800px;
            margin: 0 auto;
        }
        .chapter-title {
            font-size: 2em;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        .toc-title {
            font-size: 2.5em;
            font-weight: 700;
            text-align: center;
            margin-bottom: 40px;
            color: #2d3748;
        }
        .toc-list {
            list-style: none;
            padding: 0;
        }
        .toc-list li {
            padding: 12px 0;
            border-bottom: 1px solid #e2e8f0;
            font-size: 1.1em;
        }
        .toc-list li:last-child {
            border-bottom: none;
        }
        .toc-list a {
            color: #2d3748;
            text-decoration: none;
            display: block;
            transition: color 0.2s;
        }
        .toc-list a:hover {
            color: #667eea;
        }
        .chapter-content {
            font-size: 1.1em;
            line-height: 1.8;
            text-align: justify;
        }
        .chapter-content h1, .chapter-content h2, .chapter-content h3 {
            color: #2d3748;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        .chapter-content h1 {
            font-size: 1.8em;
            font-weight: 600;
        }
        .chapter-content h2 {
            font-size: 1.5em;
            font-weight: 600;
        }
        .chapter-content h3 {
            font-size: 1.3em;
            font-weight: 600;
        }
        .chapter-content p {
            margin-bottom: 15px;
        }
        .chapter-content blockquote {
            border-left: 4px solid #667eea;
            padding-left: 20px;
            margin: 20px 0;
            font-style: italic;
            background: #f7fafc;
            padding: 20px;
            border-radius: 0 8px 8px 0;
        }
        .chapter-content ul, .chapter-content ol {
            margin: 15px 0;
            padding-left: 30px;
        }
        .chapter-content li {
            margin-bottom: 8px;
        }
        .preface, .afterword {
            background: #f7fafc;
            padding: 30px;
            border-radius: 10px;
            border-left: 5px solid #667eea;
            margin: 20px 0;
        }
        .preface h1, .afterword h1 {
            color: #667eea;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>

<div class="cover-page">
    <h1 class="cover-title">'.$titel.'</h1>
    <img src="'.$bild.'" class="cover-image" alt="Cover Image">
    <div class="cover-meta">
        <p><strong>Autor:</strong> '.$author.'</p>
        <p><strong>Verlag:</strong> '.$verlag.'</p>
        <p><strong>Datum:</strong> '.date("d.m.Y").'</p>
    </div>
</div>

<div class="page-break"></div>
<div class="content-page">
    <h1 class="toc-title">Inhaltsverzeichnis</h1>
    <ul class="toc-list">
        <li><a href="#vorwort">Vorwort</a></li>';

foreach($themen as $i => $t) 
if($t && !str_contains($t, 'vorwort') && !str_contains($t, 'nachwort'))
  $html .= '<li><a href="#kapitel'.($i+1).'">Kapitel '.($i+1).': '.str_replace(".html", "", $t).'</a></li>';

$html .= '
        <li><a href="#nachwort">Nachwort</a></li>
    </ul>
</div>';

// Preface
foreach($themen as $i => $t) 
if($t && str_contains($t, 'vorwort'))
$html .= '
<div class="page-break"></div>
<div class="content-page">
    <div class="preface">
        <h1 id="vorwort">Vorwort</h1>
        <div class="chapter-content">
            '.$text[$t].'
        </div>
    </div>
</div>';

// Chapters
foreach($themen as $i => $t) 
if($t && !str_contains($t, 'vorwort') && !str_contains($t, 'nachwort')) {
$html .= '
<div class="page-break"></div>
<div class="content-page">
    <h1 id="kapitel'.($i+1).'" class="chapter-title">Kapitel '.($i+1).': '.str_replace(".html", "", $t).'</h1>
    <div class="chapter-content">
        '.$text[$t].'
    </div>
</div>';
}

// Afterword
foreach($themen as $i => $t) 
if($t && str_contains($t, 'nachwort'))
$html .= '
<div class="page-break"></div>
<div class="content-page">
    <div class="afterword">
        <h1 id="nachwort">Nachwort</h1>
        <div class="chapter-content">
            '.$text[$t].'
        </div>
    </div>
</div>
</body>
</html>';

// Include the main TCPDF library
require_once('tcpdf/tcpdf.php');

// Extend the TCPDF class to create custom Header and Footer
class ModernPDF extends TCPDF {
    private $bookTitle;
    private $bookAuthor;
    
    public function setBookInfo($title, $author) {
        $this->bookTitle = $title;
        $this->bookAuthor = $author;
    }

    // Page header
    public function Header() {
        // Set font
        $this->SetFont('helvetica', 'B', 10);
        // Title
        $this->Cell(0, 15, $this->bookTitle, 0, false, 'C', 0, '', 0, false, 'M', 'M');
        // Line break
        $this->Ln(20);
    }

    // Page footer
    public function Footer() {
        // Position at 15 mm from bottom
        $this->SetY(-15);
        // Set font
        $this->SetFont('helvetica', 'I', 8);
        // Page number
        $this->Cell(0, 10, 'Seite '.$this->getAliasNumPage().'/'.$this->getAliasNbPages(), 0, false, 'C', 0, '', 0, false, 'T', 'M');
    }
}

// Create new PDF document
$pdf = new ModernPDF(PDF_PAGE_ORIENTATION, PDF_UNIT, PDF_PAGE_FORMAT, true, 'UTF-8', false);

// Set document information
$pdf->SetCreator('Modern Book Generator');
$pdf->SetAuthor($author);
$pdf->SetTitle($titel);
$pdf->SetSubject($thema);
$pdf->SetKeywords($thema);

// Set book info for header/footer
$pdf->setBookInfo($titel, $author);

// Set default header data
$pdf->SetHeaderData(PDF_HEADER_LOGO, PDF_HEADER_LOGO_WIDTH, PDF_HEADER_TITLE, PDF_HEADER_STRING);

// Set header and footer fonts
$pdf->setHeaderFont(Array(PDF_FONT_NAME_MAIN, '', PDF_FONT_SIZE_MAIN));
$pdf->setFooterFont(Array(PDF_FONT_NAME_DATA, '', PDF_FONT_SIZE_DATA));

// Set default monospaced font
$pdf->SetDefaultMonospacedFont(PDF_FONT_MONOSPACED);

// Set margins
$pdf->SetMargins(PDF_MARGIN_LEFT, PDF_MARGIN_TOP, PDF_MARGIN_RIGHT);
$pdf->SetHeaderMargin(PDF_MARGIN_HEADER);
$pdf->SetFooterMargin(PDF_MARGIN_FOOTER);

// Set auto page breaks
$pdf->SetAutoPageBreak(TRUE, PDF_MARGIN_BOTTOM);

// Set image scale factor
$pdf->setImageScale(PDF_IMAGE_SCALE_RATIO);

// Set default font subsetting mode
$pdf->setFontSubsetting(true);

// Set font
$pdf->SetFont('helvetica', '', 11);

// Add a page
$pdf->AddPage();

// Output the HTML content
$pdf->writeHTML($html, true, 0, true, 0);

// Reset pointer to the last page
$pdf->lastPage();

// Close and output PDF document
$pdf->Output('modern_book_'.uniqid().'.pdf', 'I');
?>
