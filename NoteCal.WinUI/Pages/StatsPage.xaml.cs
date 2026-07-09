using Microsoft.UI.Xaml.Controls;
using NoteCal_WinUI.ViewModels;

namespace NoteCal_WinUI.Pages;

public sealed partial class StatsPage : Page
{
    private readonly StatsViewModel _viewModel = new();

    public StatsPage()
    {
        InitializeComponent();
        DataContext = _viewModel;
        Loaded += StatsPage_Loaded;
    }

    private async void StatsPage_Loaded(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        Loaded -= StatsPage_Loaded;
        await _viewModel.LoadAsync();
    }

    private async void PreviousMonth_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        await _viewModel.PreviousMonthAsync();
    }

    private async void CurrentMonth_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        await _viewModel.CurrentMonthAsync();
    }

    private async void NextMonth_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        await _viewModel.NextMonthAsync();
    }
}
