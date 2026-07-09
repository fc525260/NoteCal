param(
    [int]$TimeoutSeconds = 20
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type @"
using System;
using System.Runtime.InteropServices;

public static class NativeMouse {
    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int x, int y);

    [DllImport("user32.dll")]
    public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, UIntPtr dwExtraInfo);

    public const uint LEFTDOWN = 0x0002;
    public const uint LEFTUP = 0x0004;
}
"@

$repoRoot = Split-Path -Parent $PSScriptRoot
$packageRoot = Join-Path $repoRoot "dist\NoteCal-0.7.2-winui3-win-x64-portable"
$exe = Join-Path $packageRoot "NoteCal.exe"

if (-not (Test-Path -LiteralPath $exe)) {
    & (Join-Path $PSScriptRoot "smoke-winui-release.ps1") | Out-Host
}

$dataDir = Join-Path $packageRoot "user"
if ((Resolve-Path $packageRoot).Path -notlike (Join-Path (Resolve-Path $repoRoot).Path "*")) {
    throw "Package directory is outside the repository: $packageRoot"
}

Get-Process -Name "NoteCal", "NoteCal.WinUI" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 500
Remove-Item -LiteralPath $dataDir -Recurse -Force -ErrorAction SilentlyContinue

function Wait-Until {
    param(
        [scriptblock]$Probe,
        [string]$Description
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    do {
        $result = & $Probe
        if ($null -ne $result) {
            return $result
        }

        Start-Sleep -Milliseconds 250
    } while ((Get-Date) -lt $deadline)

    throw "Timed out waiting for $Description."
}

function Find-ByAutomationId {
    param(
        [System.Windows.Automation.AutomationElement]$Root,
        [string]$AutomationId
    )

    $condition = New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::AutomationIdProperty,
        $AutomationId)
    $found = $Root.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $condition)
    if ($null -ne $found) {
        return $found
    }

    return Find-ByAutomationIdRecursive -Root $Root -AutomationId $AutomationId -Depth 0
}

function Find-ByAutomationIdRecursive {
    param(
        [System.Windows.Automation.AutomationElement]$Root,
        [string]$AutomationId,
        [int]$Depth
    )

    if ($Depth -gt 20 -or $null -eq $Root) {
        return $null
    }

    if ($Root.Current.AutomationId -eq $AutomationId) {
        return $Root
    }

    $walker = [System.Windows.Automation.TreeWalker]::ControlViewWalker
    $child = $walker.GetFirstChild($Root)
    while ($null -ne $child) {
        $found = Find-ByAutomationIdRecursive -Root $child -AutomationId $AutomationId -Depth ($Depth + 1)
        if ($null -ne $found) {
            return $found
        }

        $child = $walker.GetNextSibling($child)
    }

    return $null
}

function Find-ByName {
    param(
        [System.Windows.Automation.AutomationElement]$Root,
        [string]$Name
    )

    $condition = New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::NameProperty,
        $Name)
    return $Root.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $condition)
}

function Require-ByAutomationId {
    param(
        [System.Windows.Automation.AutomationElement]$Root,
        [string]$AutomationId
    )

    return Wait-Until -Description "AutomationId=$AutomationId" -Probe {
        $found = Find-ByAutomationId -Root $Root -AutomationId $AutomationId
        if ($null -ne $found) {
            return $found
        }

        $freshRoot = Find-NoteCalWindow
        if ($null -eq $freshRoot) {
            return $null
        }

        return Find-ByAutomationId -Root $freshRoot -AutomationId $AutomationId
    }
}

function Find-NoteCalWindow {
    $desktop = [System.Windows.Automation.AutomationElement]::RootElement
    $windows = $desktop.FindAll(
        [System.Windows.Automation.TreeScope]::Children,
        [System.Windows.Automation.Condition]::TrueCondition)
    foreach ($candidate in $windows) {
        if ($candidate.Current.Name -like "NoteCal*" -and
            $null -ne (Find-ByAutomationId -Root $candidate -AutomationId "MainNavigation")) {
            return $candidate
        }
    }

    return $null
}

function Invoke-Control {
    param([System.Windows.Automation.AutomationElement]$Element)

    try {
        $pattern = $Element.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
        $pattern.Invoke()
    }
    catch {
        Click-Control -Element $Element
    }
}

function Toggle-Control {
    param([System.Windows.Automation.AutomationElement]$Element)

    try {
        $pattern = $Element.GetCurrentPattern([System.Windows.Automation.TogglePattern]::Pattern)
        $pattern.Toggle()
    }
    catch {
        Click-Control -Element $Element
    }
}

function Click-Control {
    param([System.Windows.Automation.AutomationElement]$Element)

    $rect = $Element.Current.BoundingRectangle
    if ($rect.IsEmpty) {
        throw "Cannot click element with empty bounding rectangle."
    }

    $x = [int]($rect.Left + ($rect.Width / 2))
    $y = [int]($rect.Top + ($rect.Height / 2))
    [NativeMouse]::SetCursorPos($x, $y) | Out-Null
    Start-Sleep -Milliseconds 100
    [NativeMouse]::mouse_event([NativeMouse]::LEFTDOWN, 0, 0, 0, [UIntPtr]::Zero)
    [NativeMouse]::mouse_event([NativeMouse]::LEFTUP, 0, 0, 0, [UIntPtr]::Zero)
    Start-Sleep -Milliseconds 250
}

function Set-Text {
    param(
        [System.Windows.Automation.AutomationElement]$Element,
        [string]$Text
    )

    $pattern = $Element.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
    $pattern.SetValue($Text)
}

function Select-Nav {
    param(
        [System.Windows.Automation.AutomationElement]$Root,
        [string]$AutomationId
    )

    $item = Require-ByAutomationId -Root $Root -AutomationId $AutomationId
    try {
        $selection = $item.GetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern)
        $selection.Select()
    }
    catch {
        Invoke-Control -Element $item
    }
}

function Start-AppWindow {
    $script:process = Start-Process -FilePath $exe -WorkingDirectory $packageRoot -PassThru
    return Wait-Until -Description "NoteCal window" -Probe {
        Find-NoteCalWindow
    }
}

try {
    $window = Start-AppWindow
    try {
        $windowPattern = $window.GetCurrentPattern([System.Windows.Automation.WindowPattern]::Pattern)
        $windowPattern.SetWindowVisualState([System.Windows.Automation.WindowVisualState]::Maximized)
        Start-Sleep -Milliseconds 500
    }
    catch {
        Click-Control -Element $window
    }

    Require-ByAutomationId -Root $window -AutomationId "HomeCalendarGrid" | Out-Null
    $noteBox = Require-ByAutomationId -Root $window -AutomationId "HomeNoteTextBox"
    Set-Text -Element $noteBox -Text "UI acceptance note"
    Toggle-Control -Element (Require-ByAutomationId -Root $window -AutomationId "HomeLeaveCheckBox")
    Invoke-Control -Element (Require-ByAutomationId -Root $window -AutomationId "HomeSaveButton")
    Invoke-Control -Element (Require-ByAutomationId -Root $window -AutomationId "HomeToggleSummarySelectionButton")
    Invoke-Control -Element (Require-ByAutomationId -Root $window -AutomationId "HomeToggleSummarySelectionButton")
    Invoke-Control -Element (Require-ByAutomationId -Root $window -AutomationId "HomeShowSummaryButton")
    Wait-Until -Description "summary dialog" -Probe {
        Find-ByName -Root (Find-NoteCalWindow) -Name "工作总结"
    } | Out-Null
    $closeButton = Wait-Until -Description "summary dialog close button" -Probe {
        Find-ByName -Root (Find-NoteCalWindow) -Name "关闭"
    }
    Invoke-Control -Element $closeButton
    $notesPath = Join-Path $dataDir "NoteCal_notes.json"
    Wait-Until -Description "saved note JSON" -Probe {
        if (-not (Test-Path -LiteralPath $notesPath)) {
            return $null
        }

        $json = Get-Content -Raw -LiteralPath $notesPath | ConvertFrom-Json
        $todayKey = Get-Date -Format "yyyy-MM-dd"
        $todayEntry = $json.PSObject.Properties[$todayKey].Value
        if ($null -ne $todayEntry -and $todayEntry.content -eq "UI acceptance note" -and $todayEntry.leave -eq $true) {
            return $true
        }

        return $null
    } | Out-Null

    Select-Nav -Root $window -AutomationId "NavStats"
    Require-ByAutomationId -Root $window -AutomationId "StatsCommandBar" | Out-Null
    Require-ByAutomationId -Root $window -AutomationId "StatsCurrentMonthButton" | Out-Null

    Select-Nav -Root $window -AutomationId "NavSettings"
    Require-ByAutomationId -Root $window -AutomationId "SettingsThemeSelector" | Out-Null
    Require-ByAutomationId -Root $window -AutomationId "SettingsShowLunarSwitch" | Out-Null
    Require-ByAutomationId -Root $window -AutomationId "SettingsMinimizeToTraySwitch" | Out-Null

    Stop-Process -Id $process.Id -Force
    Start-Sleep -Milliseconds 500
    $window = Start-AppWindow
    $noteBox = Require-ByAutomationId -Root $window -AutomationId "HomeNoteTextBox"
    $valuePattern = $noteBox.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern)
    if ($valuePattern.Current.Value -ne "UI acceptance note") {
        throw "Saved note was not restored after restart."
    }

    [pscustomobject]@{
        WindowLaunched = $true
        HomeEditorAcceptedInput = $true
        LeaveToggleInvoked = $true
        SummarySelectionExitVerified = $true
        HomeSummaryDialogReachable = $true
        SavedJsonVerified = $true
        RestartReloadVerified = $true
        StatsPageReachable = $true
        SettingsPageReachable = $true
    } | Format-List
}
finally {
    if ($null -ne $process -and -not $process.HasExited) {
        Stop-Process -Id $process.Id -Force
    }

    Get-Process -Name "NoteCal" -ErrorAction SilentlyContinue | Stop-Process -Force
    Get-Process -Name "NoteCal.WinUI" -ErrorAction SilentlyContinue | Stop-Process -Force
}
