using System.ComponentModel;
using System.Runtime.CompilerServices;
using NoteCal_WinUI.Services;

namespace NoteCal_WinUI.ViewModels;

public sealed class SettingsViewModel : INotifyPropertyChanged
{
    private bool _isLoaded;
    private string _theme = "light";
    private bool _showLunar = true;
    private bool _minimizeToTray = true;
    private string _statusText = "设置会自动保存。";

    public event PropertyChangedEventHandler? PropertyChanged;

    public event EventHandler<string>? ThemeChanged;

    public string Theme
    {
        get => _theme;
        private set
        {
            if (_theme != value)
            {
                _theme = value;
                OnPropertyChanged();
                OnPropertyChanged(nameof(IsLightTheme));
                OnPropertyChanged(nameof(IsDarkTheme));
                OnPropertyChanged(nameof(ThemeLabel));
            }
        }
    }

    public bool IsLightTheme => Theme == "light";

    public bool IsDarkTheme => Theme == "dark";

    public string ThemeLabel => IsDarkTheme ? "深色" : "浅色";

    public bool ShowLunar
    {
        get => _showLunar;
        set
        {
            if (_showLunar != value)
            {
                _showLunar = value;
                OnPropertyChanged();
                SaveShowLunarAsync(value);
            }
        }
    }

    public bool MinimizeToTray
    {
        get => _minimizeToTray;
        set
        {
            if (_minimizeToTray != value)
            {
                _minimizeToTray = value;
                OnPropertyChanged();
                SaveMinimizeToTrayAsync(value);
            }
        }
    }

    public string StatusText
    {
        get => _statusText;
        private set
        {
            if (_statusText != value)
            {
                _statusText = value;
                OnPropertyChanged();
            }
        }
    }

    public async Task LoadAsync()
    {
        await AppState.Current.LoadAsync().ConfigureAwait(true);
        Theme = NormalizeTheme(AppState.Current.Settings.Theme);
        _showLunar = AppState.Current.Settings.ShowLunar;
        _minimizeToTray = AppState.Current.Settings.MinimizeToTray;
        _isLoaded = true;
        OnPropertyChanged(nameof(ShowLunar));
        OnPropertyChanged(nameof(MinimizeToTray));
    }

    public async Task SetThemeAsync(string theme)
    {
        theme = NormalizeTheme(theme);
        if (Theme == theme)
        {
            return;
        }

        Theme = theme;
        if (!_isLoaded)
        {
            return;
        }

        await AppState.Current.SetThemeAsync(theme).ConfigureAwait(true);
        ThemeChanged?.Invoke(this, theme);
        StatusText = $"已切换为{ThemeLabel}主题。";
    }

    private async void SaveShowLunarAsync(bool value)
    {
        if (!_isLoaded)
        {
            return;
        }

        await AppState.Current.SetShowLunarAsync(value).ConfigureAwait(true);
        StatusText = value ? "月历将显示农历日期。" : "月历将隐藏农历文本。";
    }

    private async void SaveMinimizeToTrayAsync(bool value)
    {
        if (!_isLoaded)
        {
            return;
        }

        await AppState.Current.SetMinimizeToTrayAsync(value).ConfigureAwait(true);
        StatusText = value ? "已保存最小化到托盘偏好。" : "已关闭最小化到托盘偏好。";
    }

    private static string NormalizeTheme(string theme)
    {
        return string.Equals(theme, "dark", StringComparison.OrdinalIgnoreCase) ? "dark" : "light";
    }

    private void OnPropertyChanged([CallerMemberName] string? propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
