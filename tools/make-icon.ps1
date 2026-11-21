# Draws the Day Counter registry icon: the action bar's "DAY 12" over a hotbar.
# The registry's icons are mostly 256x256 PNG under 256 KiB, so that is the target.
param(
    [string]$Out = "$PSScriptRoot\..\icon.png"
)

Add-Type -AssemblyName System.Drawing

$size = 256
$bmp = New-Object System.Drawing.Bitmap($size, $size, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic

# A dark, slightly lifted background, like the HUD sits on.
$bg = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
    (New-Object System.Drawing.Rectangle(0, 0, $size, $size)),
    [System.Drawing.Color]::FromArgb(255, 42, 44, 49),
    [System.Drawing.Color]::FromArgb(255, 20, 21, 24),
    [System.Drawing.Drawing2D.LinearGradientMode]::Vertical)
$g.FillRectangle($bg, 0, 0, $size, $size)

function New-RoundedPath([int]$x, [int]$y, [int]$w, [int]$h, [int]$r) {
    $p = New-Object System.Drawing.Drawing2D.GraphicsPath
    $d = $r * 2
    $p.AddArc($x, $y, $d, $d, 180, 90)
    $p.AddArc($x + $w - $d, $y, $d, $d, 270, 90)
    $p.AddArc($x + $w - $d, $y + $h - $d, $d, $d, 0, 90)
    $p.AddArc($x, $y + $h - $d, $d, $d, 90, 90)
    $p.CloseFigure()
    return $p
}

# The action bar: a translucent dark pill with a thin light edge.
$pill = New-RoundedPath 24 66 208 78 14
$g.FillPath((New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(170, 0, 0, 0))), $pill)
$edge = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(90, 190, 196, 204), 1.5)
$g.DrawPath($edge, $pill)

# "DAY 12" — the number the mod actually shows.
$font = New-Object System.Drawing.Font("Consolas", 38, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$fmt = New-Object System.Drawing.StringFormat
$fmt.Alignment = [System.Drawing.StringAlignment]::Center
$fmt.LineAlignment = [System.Drawing.StringAlignment]::Center
$box = New-Object System.Drawing.RectangleF(24, 66, 208, 78)
$g.DrawString("DAY 12", $font, (New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)), $box, $fmt)

# The hotbar the number sits above: nine slots.
$slotBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 58, 60, 66))
$slotEdge = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 104, 108, 116), 1)
$slotTop = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(70, 255, 255, 255), 1)
$selectedEdge = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 235, 235, 235), 2)

$slot = 20
$gap = 3
$total = 9 * $slot + 8 * $gap
$left = [int](($size - $total) / 2)
$top = 192
for ($i = 0; $i -lt 9; $i++) {
    $x = $left + $i * ($slot + $gap)
    $g.FillRectangle($slotBrush, $x, $top, $slot, $slot)
    $g.DrawRectangle($slotEdge, $x, $top, $slot, $slot)
    # A lighter top edge so the slot reads as recessed rather than flat.
    $g.DrawLine($slotTop, $x + 1, $top + 1, $x + $slot - 2, $top + 1)
}
# The selected slot, as vanilla draws it.
$sel = $left + 4 * ($slot + $gap)
$g.DrawRectangle($selectedEdge, $sel - 1, $top - 1, $slot + 2, $slot + 2)

$dir = Split-Path -Parent $Out
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)

$g.Dispose(); $bmp.Dispose()
$info = Get-Item $Out
Write-Output "$($info.FullName) $([int]($info.Length / 1KB)) KiB"
