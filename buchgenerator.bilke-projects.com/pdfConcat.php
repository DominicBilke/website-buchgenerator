require_once("tcpdf/tcpdf.php");
require_once("fpdi/src/Tcpdf/Fpdi.php");

class concat_pdf extends FPDI {
     var $files = array();
     function setFiles($files) {
          $this->files = $files;
     }
     function concat() {
          foreach($this->files AS $file) {
               $pagecount = $this->setSourceFile($file);
               for ($i = 1; $i <= $pagecount; $i++) {
                    $tplidx = $this->ImportPage($i);
                    $s = $this->getTemplatesize($tplidx);
                    $this->AddPage(’P', array($s['w'], $s['h']));
                    $this->useTemplate($tplidx);
               }
          }
     }
}

include_once("pdfConcat.php");
$pdf =& new concat_pdf();
$pdf->setFiles(array("doc.pdf","pauta.pdf", "4bp.pdf", "5bp.pdf"));
$pdf->concat();
$pdf->Output("newpdf.pdf", "I");