using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using NoteCal_WinUI.ViewModels;

namespace NoteCal_WinUI.Pages;

public sealed partial class HomePage : Page
{
    private readonly DashboardViewModel _viewModel = new();

    public HomePage()
    {
        InitializeComponent();
        DataContext = _viewModel;
        Loaded += HomePage_Loaded;
    }

    private async void HomePage_Loaded(object sender, RoutedEventArgs e)
    {
        Loaded -= HomePage_Loaded;
        await _viewModel.LoadAsync();
    }

    private async void CalendarGrid_ItemClick(object sender, ItemClickEventArgs e)
    {
        if (e.ClickedItem is DashboardDayViewModel day)
        {
            await _viewModel.SelectDateAsync(day);
        }
    }

    private async void PreviousMonth_Click(object sender, RoutedEventArgs e)
    {
        await _viewModel.PreviousMonthAsync();
    }

    private async void Today_Click(object sender, RoutedEventArgs e)
    {
        await _viewModel.GoToTodayAsync();
    }

    private async void NextMonth_Click(object sender, RoutedEventArgs e)
    {
        await _viewModel.NextMonthAsync();
    }

    private async void ToggleSummarySelection_Click(object sender, RoutedEventArgs e)
    {
        await _viewModel.ToggleSummarySelectionModeAsync();
    }

    private async void SaveSelected_Click(object sender, RoutedEventArgs e)
    {
        await _viewModel.SaveSelectedAsync();
    }

    private async void ClearSelected_Click(object sender, RoutedEventArgs e)
    {
        await _viewModel.ClearSelectedAsync();
    }

    private async void ShowSummary_Click(object sender, RoutedEventArgs e)
    {
        var summary = await _viewModel.BuildSelectedSummaryAsync();
        var selectedDates = _viewModel.SelectedSummaryDatesText;
        var summaryBox = new TextBox
        {
            AcceptsReturn = true,
            IsReadOnly = true,
            Text = string.IsNullOrWhiteSpace(summary)
                ? "当前没有可汇总的所选日期。请点击“选择日期”后选择要汇总的日期。"
                : summary,
            TextWrapping = TextWrapping.Wrap,
            MinWidth = 520,
            MinHeight = 220,
            MaxHeight = 360,
        };

        var panel = new StackPanel { Spacing = 10 };
        panel.Children.Add(new TextBlock
        {
            Text = selectedDates,
            TextWrapping = TextWrapping.Wrap,
        });
        panel.Children.Add(summaryBox);

        var dialog = new ContentDialog
        {
            Title = "工作总结",
            Content = panel,
            PrimaryButtonText = "复制",
            CloseButtonText = "关闭",
            XamlRoot = XamlRoot,
            DefaultButton = ContentDialogButton.Primary,
        };

        var result = await dialog.ShowAsync();
        if (result == ContentDialogResult.Primary && !string.IsNullOrWhiteSpace(summary))
        {
            var package = new Windows.ApplicationModel.DataTransfer.DataPackage();
            package.SetText(summary);
            Windows.ApplicationModel.DataTransfer.Clipboard.SetContent(package);
        }
    }
}
