$ErrorActionPreference = 'Stop'
$finalRoot = Split-Path -Parent $PSScriptRoot
$finalDocx = Join-Path $finalRoot 'PITWALL_Mithil_Katkoria_H446_NEA_FINAL_MASTER.docx'
$finalPdf = Join-Path $finalRoot 'PITWALL_Mithil_Katkoria_H446_NEA_FINAL_MASTER.pdf'
$finalWord = New-Object -ComObject Word.Application
$finalWord.Visible = $false
$finalWord.DisplayAlerts = 0
try {
    $finalDocument = $finalWord.Documents.Open($finalDocx)
    $finalDocument.Fields.Update() | Out-Null
    foreach ($finalToc in $finalDocument.TablesOfContents) { $finalToc.Update() }
    $finalDocument.Repaginate()
    foreach ($finalToc in $finalDocument.TablesOfContents) { $finalToc.UpdatePageNumbers() }
    $finalDocument.Save()
    $finalDocument.ExportAsFixedFormat($finalPdf, 17, $false, 1)
    Write-Output "Exported pages: $($finalDocument.ComputeStatistics(2))"
    $finalDocument.Close(0)
} finally { $finalWord.Quit() }
