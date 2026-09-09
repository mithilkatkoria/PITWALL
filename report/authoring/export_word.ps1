$ErrorActionPreference = 'Stop'
$reportRoot = Split-Path -Parent $PSScriptRoot
$reportDocx = Join-Path $reportRoot 'PITWALL_Mithil_Katkoria_H446_NEA_MASTER.docx'
$reportPdf = Join-Path $reportRoot 'PITWALL_Mithil_Katkoria_H446_NEA_MASTER.pdf'
$reportWord = New-Object -ComObject Word.Application
$reportWord.Visible = $false
$reportWord.DisplayAlerts = 0
try {
    $reportDocument = $reportWord.Documents.Open($reportDocx)
    $reportDocument.Fields.Update() | Out-Null
    foreach ($reportToc in $reportDocument.TablesOfContents) { $reportToc.Update() }
    $reportDocument.Repaginate()
    foreach ($reportToc in $reportDocument.TablesOfContents) { $reportToc.UpdatePageNumbers() }
    $reportDocument.Save()
    $reportDocument.ExportAsFixedFormat($reportPdf, 17, $false, 1)
    Write-Output "Exported pages: $($reportDocument.ComputeStatistics(2))"
    $reportDocument.Close(0)
} finally { $reportWord.Quit() }
