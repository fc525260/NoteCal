using Microsoft.UI.Xaml.Controls;
using NoteCal_WinUI.ViewModels;

namespace NoteCal_WinUI.Pages;

public sealed partial class SummaryPage : Page
{
    private readonly SummaryViewModel _viewModel = new();

    public SummaryPage()
    {
        InitializeComponent();
        DataContext = _viewModel;
        Loaded += SummaryPage_Loaded;
    }

    private async void SummaryPage_Loaded(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        Loaded -= SummaryPage_Loaded;
        await _viewModel.LoadAsync();
    }

    private void Copy_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        if (_viewModel.HasSummary)
        {
            var package = new Windows.ApplicationModel.DataTransfer.DataPackage();
            package.SetText(_viewModel.SummaryText);
            Windows.ApplicationModel.DataTransfer.Clipboard.SetContent(package);
        }
    }

    private async void ClearSelection_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
    {
        await _viewModel.ClearSelectionAsync();
    }
}
