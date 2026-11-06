<#
.SYNOPSIS
    Robust, zero-dependency PWA Icon & Favicon Generator for Windows PowerShell.
.DESCRIPTION
    Uses native .NET System.Drawing classes to resize and generate high-quality 
    PWA icons (192x192, 512x512), Apple touch icon (180x180), favicons (16x16, 32x32),
    and a multi-resolution favicon.ico directly from a single high-resolution image.
.PARAMETER SourcePath
    Path to the source image (JPG or PNG). Defaults to 'source.jpg' or 'source.png'.
.PARAMETER TargetDir
    Target directory to save icons. Defaults to the project's 'public' folder.
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$SourcePath,

    [Parameter(Position = 1)]
    [string]$TargetDir
)

# Load native .NET Drawing assembly
Add-Type -AssemblyName System.Drawing

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "       PWA ICON & FAVICON GENERATION UTILITY                " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Resolve Project Root and Target Directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

if ([string]::IsNullOrWhiteSpace($TargetDir)) {
    # Check if ./public exists relative to project root or current directory
    if (Test-Path (Join-Path $ProjectRoot "public")) {
        $TargetDir = Join-Path $ProjectRoot "public"
    } elseif (Test-Path (Join-Path $PWD "public")) {
        $TargetDir = Join-Path $PWD "public"
    } else {
        $TargetDir = Join-Path $ProjectRoot "public"
    }
}

if (-not (Test-Path $TargetDir)) {
    Write-Host "[INFO] Creating target directory: $TargetDir" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

$TargetDir = (Resolve-Path $TargetDir).Path

# 2. Locate Source Image
if ([string]::IsNullOrWhiteSpace($SourcePath)) {
    $PotentialSources = @(
        (Join-Path $ProjectRoot "source.jpg"),
        (Join-Path $ProjectRoot "source.png"),
        (Join-Path $PWD "source.jpg"),
        (Join-Path $PWD "source.png"),
        (Join-Path $ScriptDir "source.jpg"),
        (Join-Path $ScriptDir "source.png")
    )

    foreach ($candidate in $PotentialSources) {
        if (Test-Path $candidate) {
            $SourcePath = $candidate
            break
        }
    }
}

if ([string]::IsNullOrWhiteSpace($SourcePath) -or -not (Test-Path $SourcePath)) {
    Write-Host "[ERROR] Source image not found! Please supply -SourcePath or place 'source.jpg' in project root." -ForegroundColor Red
    exit 1
}

$SourcePath = (Resolve-Path $SourcePath).Path
Write-Host "[OK] Source image: $SourcePath" -ForegroundColor Green
Write-Host "[OK] Target directory: $TargetDir" -ForegroundColor Green

# 3. Helper: Resize and Center-Crop Image to Square
function Create-SquareBitmap {
    param(
        [System.Drawing.Image]$SourceImg,
        [int]$TargetSize
    )

    $srcW = $SourceImg.Width
    $srcH = $SourceImg.Height

    # Determine square crop bounds (center crop)
    if ($srcW -gt $srcH) {
        $cropSize = $srcH
        $cropX = [int](($srcW - $srcH) / 2)
        $cropY = 0
    } else {
        $cropSize = $srcW
        $cropX = 0
        $cropY = [int](($srcH - $srcW) / 2)
    }

    $destBmp = New-Object System.Drawing.Bitmap($TargetSize, $TargetSize, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $destBmp.SetResolution($SourceImg.HorizontalResolution, $SourceImg.VerticalResolution)

    $g = [System.Drawing.Graphics]::FromImage($destBmp)
    try {
        # Configure High-Quality settings
        $g.InterpolationMode  = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $g.SmoothingMode      = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
        $g.PixelOffsetMode    = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $g.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
        $g.Clear([System.Drawing.Color]::Transparent)

        $srcRect  = New-Object System.Drawing.Rectangle($cropX, $cropY, $cropSize, $cropSize)
        $destRect = New-Object System.Drawing.Rectangle(0, 0, $TargetSize, $TargetSize)

        $g.DrawImage($SourceImg, $destRect, $srcRect, [System.Drawing.GraphicsUnit]::Pixel)
    } finally {
        $g.Dispose()
    }

    return $destBmp
}

# 4. Helper: Write Multi-Resolution ICO File from PNG byte streams
function Save-MultiResolutionIco {
    param(
        [byte[][]]$PngStreams,
        [int[]]$Dimensions,
        [string]$OutputPath
    )

    $numImages = $PngStreams.Count
    $headerSize = 6
    $dirEntrySize = 16
    $dataOffset = $headerSize + ($dirEntrySize * $numImages)

    $fs = [System.IO.File]::Create($OutputPath)
    $bw = New-Object System.IO.BinaryWriter($fs)

    try {
        # ICONDIR Header (6 bytes)
        $bw.Write([uint16]0)          # Reserved: 0
        $bw.Write([uint16]1)          # Type: 1 = Icon (.ICO)
        $bw.Write([uint16]$numImages) # Image count

        # ICONDIRENTRY list
        $currentOffset = $dataOffset
        for ($i = 0; $i -lt $numImages; $i++) {
            $dim = $Dimensions[$i]
            $bCount = $PngStreams[$i].Length

            $bw.Write([byte]($dim -band 0xFF)) # Width (0 = 256)
            $bw.Write([byte]($dim -band 0xFF)) # Height
            $bw.Write([byte]0)                 # Color Count
            $bw.Write([byte]0)                 # Reserved
            $bw.Write([uint16]1)               # Color Planes
            $bw.Write([uint16]32)              # Bits per pixel
            $bw.Write([uint32]$bCount)         # Byte size of image data
            $bw.Write([uint32]$currentOffset)  # Offset to image data

            $currentOffset += $bCount
        }

        # Write actual PNG payloads
        for ($i = 0; $i -lt $numImages; $i++) {
            $bw.Write($PngStreams[$i])
        }
    } finally {
        $bw.Close()
        $fs.Dispose()
    }
}

# 5. Process and Generate Assets
try {
    # Load source image using file stream to prevent file lock
    $fs = [System.IO.File]::OpenRead($SourcePath)
    $sourceImg = [System.Drawing.Image]::FromStream($fs)
    Write-Host "[INFO] Source dimensions: $($sourceImg.Width) x $($sourceImg.Height) px" -ForegroundColor Cyan

    # Target Icon specifications
    $IconSpecs = @(
        @{ Name = "icon-192.png";          Size = 192; Desc = "PWA Standard Icon (Mobile)" },
        @{ Name = "icon-512.png";          Size = 512; Desc = "PWA Splash & Desktop Icon" },
        @{ Name = "apple-touch-icon.png";  Size = 180; Desc = "Apple iOS Home Screen Icon" },
        @{ Name = "favicon-32x32.png";     Size = 32;  Desc = "Standard Favicon 32x32" },
        @{ Name = "favicon-16x16.png";     Size = 16;  Desc = "Standard Favicon 16x16" }
    )

    $ico16Bytes = $null
    $ico32Bytes = $null

    foreach ($spec in $IconSpecs) {
        $outFile = Join-Path $TargetDir $spec.Name
        Write-Host "  -> Generating $($spec.Name) ($($spec.Size)x$($spec.Size)) for $($spec.Desc)..." -NoNewline
        
        $bmp = Create-SquareBitmap -SourceImg $sourceImg -TargetSize $spec.Size
        try {
            $ms = New-Object System.IO.MemoryStream
            $bmp.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
            $bytes = $ms.ToArray()
            [System.IO.File]::WriteAllBytes($outFile, $bytes)
            $ms.Dispose()

            if ($spec.Size -eq 16) { $ico16Bytes = $bytes }
            if ($spec.Size -eq 32) { $ico32Bytes = $bytes }

            Write-Host " [DONE]" -ForegroundColor Green
        } finally {
            $bmp.Dispose()
        }
    }

    # Generate multi-frame favicon.ico (16x16 + 32x32)
    $icoPath = Join-Path $TargetDir "favicon.ico"
    Write-Host "  -> Generating multi-resolution favicon.ico (16x16, 32x32)..." -NoNewline
    Save-MultiResolutionIco -PngStreams @($ico16Bytes, $ico32Bytes) -Dimensions @(16, 32) -OutputPath $icoPath
    Write-Host " [DONE]" -ForegroundColor Green

    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "🎉 SUCCESS! All icons and favicons generated in: $TargetDir" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
}
catch {
    Write-Host "`n[FATAL ERROR] An unexpected error occurred:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host $_.ScriptStackTrace -ForegroundColor DarkRed
    exit 1
}
finally {
    if ($null -ne $sourceImg) { $sourceImg.Dispose() }
    if ($null -ne $fs) { $fs.Dispose() }
}
