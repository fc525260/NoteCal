using Microsoft.UI.Windowing;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using NoteCal_WinUI.Pages;
using NoteCal_WinUI.Services;
using System.Runtime.InteropServices;
using Windows.Graphics;
using Windows.UI;
using WinRT.Interop;

// To learn more about WinUI, the WinUI project structure,
// and more about our project templates, see: http://aka.ms/winui-project-info.

namespace NoteCal_WinUI;

public sealed partial class MainWindow : Window
{
    public static MainWindow? ActiveWindow { get; private set; }

    private readonly IntPtr _hwnd;
    private readonly NativeMethods.SUBCLASSPROC _subclassProc;
    private IntPtr _trayIconHandle;
    private bool _isTrayIconVisible;
    private bool _isExiting;

    private static string AppIconPath => Path.Combine(AppContext.BaseDirectory, "Assets", "AppIcon.ico");

    public MainWindow()
    {
        ActiveWindow = this;
        InitializeComponent();
        _hwnd = WindowNative.GetWindowHandle(this);
        _subclassProc = WindowSubclassProc;

        ExtendsContentIntoTitleBar = true;
        SetTitleBar(AppTitleBar);
        AppWindow.TitleBar.PreferredHeightOption = TitleBarHeightOption.Tall;
        AppWindow.SetIcon(AppIconPath);
        AppWindow.Resize(new SizeInt32(1120, 720));
        NativeMethods.SetWindowSubclass(_hwnd, _subclassProc, UIntPtr.Zero, UIntPtr.Zero);
        AppWindow.Changed += AppWindow_Changed;
        AppWindow.Closing += AppWindow_Closing;
        Closed += MainWindow_Closed;
        RootGrid.Loaded += RootGrid_Loaded;
    }

    public void ApplyTheme(string theme)
    {
        var isDarkTheme = string.Equals(theme, "dark", StringComparison.OrdinalIgnoreCase);
        RootGrid.RequestedTheme = isDarkTheme ? ElementTheme.Dark : ElementTheme.Light;
        ApplyTitleBarButtonTheme(isDarkTheme);
    }

    private void ApplyTitleBarButtonTheme(bool isDarkTheme)
    {
        var titleBar = AppWindow.TitleBar;
        titleBar.ButtonBackgroundColor = Color.FromArgb(0, 0, 0, 0);
        titleBar.ButtonInactiveBackgroundColor = Color.FromArgb(0, 0, 0, 0);

        if (isDarkTheme)
        {
            titleBar.ButtonForegroundColor = Color.FromArgb(255, 255, 255, 255);
            titleBar.ButtonInactiveForegroundColor = Color.FromArgb(255, 150, 150, 150);
            titleBar.ButtonHoverBackgroundColor = Color.FromArgb(255, 48, 48, 48);
            titleBar.ButtonHoverForegroundColor = Color.FromArgb(255, 255, 255, 255);
            titleBar.ButtonPressedBackgroundColor = Color.FromArgb(255, 72, 72, 72);
            titleBar.ButtonPressedForegroundColor = Color.FromArgb(255, 255, 255, 255);
            return;
        }

        titleBar.ButtonForegroundColor = Color.FromArgb(255, 32, 32, 32);
        titleBar.ButtonInactiveForegroundColor = Color.FromArgb(255, 112, 112, 112);
        titleBar.ButtonHoverBackgroundColor = Color.FromArgb(255, 229, 229, 229);
        titleBar.ButtonHoverForegroundColor = Color.FromArgb(255, 0, 0, 0);
        titleBar.ButtonPressedBackgroundColor = Color.FromArgb(255, 204, 204, 204);
        titleBar.ButtonPressedForegroundColor = Color.FromArgb(255, 0, 0, 0);
    }

    private async void RootGrid_Loaded(object sender, RoutedEventArgs e)
    {
        RootGrid.Loaded -= RootGrid_Loaded;
        await AppState.Current.LoadAsync();
        ApplyTheme(AppState.Current.Settings.Theme);
    }

    private void AppWindow_Changed(AppWindow sender, AppWindowChangedEventArgs args)
    {
        if (_isExiting || !AppState.Current.Settings.MinimizeToTray)
        {
            return;
        }

        if (sender.Presenter is OverlappedPresenter presenter &&
            presenter.State == OverlappedPresenterState.Minimized)
        {
            EnsureTrayIcon();
            sender.Hide();
        }
    }

    private void AppWindow_Closing(AppWindow sender, AppWindowClosingEventArgs args)
    {
        if (_isExiting || !AppState.Current.Settings.MinimizeToTray)
        {
            return;
        }

        args.Cancel = true;
        EnsureTrayIcon();
        sender.Hide();
    }

    private void EnsureTrayIcon()
    {
        if (_isTrayIconVisible)
        {
            return;
        }

        _trayIconHandle = NativeMethods.LoadImage(
            IntPtr.Zero,
            AppIconPath,
            NativeMethods.IMAGE_ICON,
            0,
            0,
            NativeMethods.LR_LOADFROMFILE | NativeMethods.LR_DEFAULTSIZE);

        var data = CreateNotifyIconData();
        data.uFlags = NativeMethods.NIF_MESSAGE | NativeMethods.NIF_ICON | NativeMethods.NIF_TIP;
        data.hIcon = _trayIconHandle;
        data.uCallbackMessage = NativeMethods.WM_TRAYICON;
        data.szTip = "NoteCal 0.7.2";
        NativeMethods.Shell_NotifyIcon(NativeMethods.NIM_ADD, ref data);
        _isTrayIconVisible = true;
    }

    private void RestoreFromTray()
    {
        RemoveTrayIcon();
        AppWindow.Show();
        if (AppWindow.Presenter is OverlappedPresenter presenter)
        {
            presenter.Restore();
        }

        NativeMethods.SetForegroundWindow(_hwnd);
    }

    private void ExitFromTray()
    {
        _isExiting = true;
        RemoveTrayIcon();
        Close();
    }

    private void ShowTrayMenu()
    {
        var menu = NativeMethods.CreatePopupMenu();
        if (menu == IntPtr.Zero)
        {
            RestoreFromTray();
            return;
        }

        try
        {
            NativeMethods.AppendMenu(menu, NativeMethods.MF_STRING, new UIntPtr(NativeMethods.ID_TRAY_OPEN), "打开");
            NativeMethods.AppendMenu(menu, NativeMethods.MF_SEPARATOR, UIntPtr.Zero, null);
            NativeMethods.AppendMenu(menu, NativeMethods.MF_STRING, new UIntPtr(NativeMethods.ID_TRAY_EXIT), "退出");
            NativeMethods.GetCursorPos(out var point);
            NativeMethods.SetForegroundWindow(_hwnd);
            var command = NativeMethods.TrackPopupMenu(
                menu,
                NativeMethods.TPM_RETURNCMD | NativeMethods.TPM_RIGHTBUTTON,
                point.X,
                point.Y,
                0,
                _hwnd,
                IntPtr.Zero);

            if (command == NativeMethods.ID_TRAY_OPEN)
            {
                RestoreFromTray();
            }
            else if (command == NativeMethods.ID_TRAY_EXIT)
            {
                ExitFromTray();
            }
        }
        finally
        {
            NativeMethods.DestroyMenu(menu);
        }
    }

    private void MainWindow_Closed(object sender, WindowEventArgs args)
    {
        _isExiting = true;
        RemoveTrayIcon();
        AppWindow.Closing -= AppWindow_Closing;
        NativeMethods.RemoveWindowSubclass(_hwnd, _subclassProc, UIntPtr.Zero);
    }

    private void RemoveTrayIcon()
    {
        if (_isTrayIconVisible)
        {
            var data = CreateNotifyIconData();
            NativeMethods.Shell_NotifyIcon(NativeMethods.NIM_DELETE, ref data);
            _isTrayIconVisible = false;
        }

        if (_trayIconHandle != IntPtr.Zero)
        {
            NativeMethods.DestroyIcon(_trayIconHandle);
            _trayIconHandle = IntPtr.Zero;
        }
    }

    private NativeMethods.NOTIFYICONDATA CreateNotifyIconData()
    {
        return new NativeMethods.NOTIFYICONDATA
        {
            cbSize = (uint)Marshal.SizeOf<NativeMethods.NOTIFYICONDATA>(),
            hWnd = _hwnd,
            uID = 1
        };
    }

    private IntPtr WindowSubclassProc(
        IntPtr hWnd,
        uint msg,
        UIntPtr wParam,
        IntPtr lParam,
        UIntPtr uIdSubclass,
        UIntPtr dwRefData)
    {
        if (msg == NativeMethods.WM_TRAYICON && lParam.ToInt32() == NativeMethods.WM_LBUTTONDBLCLK)
        {
            RestoreFromTray();
            return IntPtr.Zero;
        }

        if (msg == NativeMethods.WM_TRAYICON && lParam.ToInt32() == NativeMethods.WM_RBUTTONUP)
        {
            ShowTrayMenu();
            return IntPtr.Zero;
        }

        return NativeMethods.DefSubclassProc(hWnd, msg, wParam, lParam);
    }

    private static class NativeMethods
    {
        public const uint ID_TRAY_OPEN = 1001;
        public const uint ID_TRAY_EXIT = 1002;
        public const int IMAGE_ICON = 1;
        public const int LR_LOADFROMFILE = 0x00000010;
        public const int LR_DEFAULTSIZE = 0x00000040;
        public const int NIF_MESSAGE = 0x00000001;
        public const int NIF_ICON = 0x00000002;
        public const int NIF_TIP = 0x00000004;
        public const int NIM_ADD = 0x00000000;
        public const int NIM_DELETE = 0x00000002;
        public const int WM_APP = 0x8000;
        public const int WM_TRAYICON = WM_APP + 1;
        public const int WM_LBUTTONDBLCLK = 0x0203;
        public const int WM_RBUTTONUP = 0x0205;
        public const uint MF_STRING = 0x00000000;
        public const uint MF_SEPARATOR = 0x00000800;
        public const uint TPM_RIGHTBUTTON = 0x0002;
        public const uint TPM_RETURNCMD = 0x0100;

        public delegate IntPtr SUBCLASSPROC(
            IntPtr hWnd,
            uint uMsg,
            UIntPtr wParam,
            IntPtr lParam,
            UIntPtr uIdSubclass,
            UIntPtr dwRefData);

        [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
        public struct NOTIFYICONDATA
        {
            public uint cbSize;
            public IntPtr hWnd;
            public uint uID;
            public uint uFlags;
            public uint uCallbackMessage;
            public IntPtr hIcon;

            [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 128)]
            public string szTip;
        }

        [StructLayout(LayoutKind.Sequential)]
        public struct POINT
        {
            public int X;
            public int Y;
        }

        [DllImport("comctl32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetWindowSubclass(
            IntPtr hWnd,
            SUBCLASSPROC pfnSubclass,
            UIntPtr uIdSubclass,
            UIntPtr dwRefData);

        [DllImport("comctl32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool RemoveWindowSubclass(
            IntPtr hWnd,
            SUBCLASSPROC pfnSubclass,
            UIntPtr uIdSubclass);

        [DllImport("comctl32.dll")]
        public static extern IntPtr DefSubclassProc(IntPtr hWnd, uint uMsg, UIntPtr wParam, IntPtr lParam);

        [DllImport("shell32.dll", CharSet = CharSet.Unicode)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool Shell_NotifyIcon(uint dwMessage, ref NOTIFYICONDATA lpData);

        [DllImport("user32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        public static extern IntPtr LoadImage(
            IntPtr hinst,
            string lpszName,
            int uType,
            int cxDesired,
            int cyDesired,
            int fuLoad);

        [DllImport("user32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool DestroyIcon(IntPtr hIcon);

        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetForegroundWindow(IntPtr hWnd);

        [DllImport("user32.dll", SetLastError = true)]
        public static extern IntPtr CreatePopupMenu();

        [DllImport("user32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool AppendMenu(IntPtr hMenu, uint uFlags, UIntPtr uIDNewItem, string? lpNewItem);

        [DllImport("user32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool DestroyMenu(IntPtr hMenu);

        [DllImport("user32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool GetCursorPos(out POINT lpPoint);

        [DllImport("user32.dll", SetLastError = true)]
        public static extern uint TrackPopupMenu(
            IntPtr hMenu,
            uint uFlags,
            int x,
            int y,
            int nReserved,
            IntPtr hWnd,
            IntPtr prcRect);
    }

    private void TitleBar_PaneToggleRequested(TitleBar sender, object args)
    {
        NavView.IsPaneOpen = !NavView.IsPaneOpen;
    }

    private void TitleBar_BackRequested(TitleBar sender, object args)
    {
        NavFrame.GoBack();
    }

    private void NavView_SelectionChanged(NavigationView sender, NavigationViewSelectionChangedEventArgs args)
    {
        if (args.IsSettingsSelected)
        {
            NavFrame.Navigate(typeof(SettingsPage));
        }
        else if (args.SelectedItem is NavigationViewItem item)
        {
            switch (item.Tag)
            {
                case "home":
                    NavFrame.Navigate(typeof(HomePage));
                    break;
                case "stats":
                    NavFrame.Navigate(typeof(StatsPage));
                    break;
                case "settings":
                    NavFrame.Navigate(typeof(SettingsPage));
                    break;
                default:
                    throw new InvalidOperationException($"Unknown navigation item tag: {item.Tag}");
            }
        }
    }
}
