// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

using Microsoft.UI.Xaml.Controls;
using NoteCal_WinUI.ViewModels;

// To learn more about WinUI, the WinUI project structure,
// and more about our project templates, see: http://aka.ms/winui-project-info.

namespace NoteCal_WinUI.Pages;

public sealed partial class SettingsPage : Page
{
    private readonly SettingsViewModel _viewModel = new();

    public SettingsPage()
    {
        InitializeComponent();
        DataContext = _viewModel;
        Loaded += SettingsPage_Loaded;
        _viewModel.ThemeChanged += SettingsViewModel_ThemeChanged;
    }

    private async void SettingsPage_Loaded(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        Loaded -= SettingsPage_Loaded;
        await _viewModel.LoadAsync();
        ThemeSelector.SelectedIndex = _viewModel.IsDarkTheme ? 1 : 0;
    }

    private async void ThemeSelector_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        if (ThemeSelector.SelectedItem is ComboBoxItem item && item.Tag is string theme)
        {
            await _viewModel.SetThemeAsync(theme);
        }
    }

    private static void SettingsViewModel_ThemeChanged(object? sender, string theme)
    {
        MainWindow.ActiveWindow?.ApplyTheme(theme);
    }
}
