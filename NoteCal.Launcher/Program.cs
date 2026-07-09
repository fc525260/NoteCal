using System.Diagnostics;

var root = AppContext.BaseDirectory;
var runtimeExe = Path.Combine(root, "datas", "runtime", "NoteCal.WinUI.exe");
var userDir = Path.Combine(root, "user");
Directory.CreateDirectory(userDir);

if (!File.Exists(runtimeExe))
{
    File.WriteAllText(Path.Combine(userDir, "launcher-error.log"), $"缺少运行文件：{runtimeExe}");
    return 1;
}

var startInfo = new ProcessStartInfo
{
    FileName = runtimeExe,
    WorkingDirectory = Path.GetDirectoryName(runtimeExe)!,
    UseShellExecute = false,
};
startInfo.Environment["NOTECAL_PORTABLE_ROOT"] = root;

using var process = Process.Start(startInfo);
if (process is null)
{
    File.WriteAllText(Path.Combine(userDir, "launcher-error.log"), "无法启动 NoteCal。");
    return 1;
}

process.WaitForExit();
return process.ExitCode;
