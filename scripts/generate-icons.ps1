Add-Type -AssemblyName System.Drawing

function Create-AppIcon([int]$size, [string]$outputPath) {
    $bmp = New-Object System.Drawing.Bitmap($size, $size)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

    $rect = New-Object System.Drawing.Rectangle(0, 0, $size, $size)
    $c1 = [System.Drawing.Color]::FromArgb(255, 99, 102, 241)
    $c2 = [System.Drawing.Color]::FromArgb(255, 139, 92, 246)
    $brush = New-Object System.Drawing.Drawing2D.LinearGradientBrush($rect, $c1, $c2, 45.0)

    $radius = [int]($size * 0.22)
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $path.AddArc(0, 0, $radius*2, $radius*2, 180, 90)
    $path.AddArc($size - $radius*2, 0, $radius*2, $radius*2, 270, 90)
    $path.AddArc($size - $radius*2, $size - $radius*2, $radius*2, $radius*2, 0, 90)
    $path.AddArc(0, $size - $radius*2, $radius*2, $radius*2, 90, 90)
    $path.CloseFigure()

    $g.FillPath($brush, $path)

    $fontSize = [float]($size * 0.48)
    $font = New-Object System.Drawing.Font("Arial", $fontSize, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
    $textBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
    
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center

    $textRect = New-Object System.Drawing.RectangleF(0, [float]($size * 0.03), [float]$size, [float]$size)
    $g.DrawString("L", $font, $textBrush, $textRect, $sf)

    $bmp.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $bmp.Dispose()
    Write-Host "Generated $outputPath ($size x $size)"
}

Create-AppIcon 192 "public/icon-192.png"
Create-AppIcon 512 "public/icon-512.png"
