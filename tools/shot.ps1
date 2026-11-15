# Saves a screenshot of the running game window (PrintWindow works while the monitor sleeps).
param([string]$Out = "$PSScriptRoot\..\out\shot.png", [int]$ProcessId = 0)
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public static class Win {
    [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr hwnd, IntPtr hdc, uint flags);
    [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr hwnd, out RECT rect);
    [DllImport("user32.dll")] public static extern bool SetProcessDpiAwarenessContext(IntPtr value);
    public struct RECT { public int Left, Top, Right, Bottom; }
}
'@
[void][Win]::SetProcessDpiAwarenessContext([IntPtr](-4))  # per-monitor v2: real pixels
$p = if ($ProcessId) { Get-Process -Id $ProcessId -ErrorAction SilentlyContinue } else {
    Get-Process bb-probe -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1 }
if (-not $p) { Write-Error 'No game window'; exit 1 }
$r = New-Object Win+RECT
[void][Win]::GetClientRect($p.MainWindowHandle, [ref]$r)
$bmp = New-Object System.Drawing.Bitmap ([Math]::Max(1, $r.Right)), ([Math]::Max(1, $r.Bottom))
$g = [System.Drawing.Graphics]::FromImage($bmp)
$hdc = $g.GetHdc()
[void][Win]::PrintWindow($p.MainWindowHandle, $hdc, 3)
$g.ReleaseHdc($hdc)
$bmp.Save((New-Item -ItemType File -Force $Out).FullName, [System.Drawing.Imaging.ImageFormat]::Png)
"Saved $Out ($($r.Right)x$($r.Bottom))"
