from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates

from datetime import datetime, timedelta

from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from matplotlib.figure import Figure

from webapp.favorite_searches.models import StatisticItems


def plot_statistics(query_id):
    items_list = StatisticItems.query.filter(
        StatisticItems.query_id == query_id,
        StatisticItems.final_price.isnot(None)).order_by(
            StatisticItems.end_time.asc()).all()
    x_data = []
    y_data = []
    bids_data = []
    for item in items_list:
        x_data.append(item.end_time)
        y_data.append(item.final_price)
        bids_data.append(item.bids)

    colors = bids_data

    plt.style.use('seaborn')
    fig = Figure(figsize=(12, 5))
    axis = fig.add_subplot(1, 1, 1)
    im = axis.scatter(x_data, y_data, c=colors, cmap='Reds', edgecolor='black', linewidths=1)
    cbar = fig.colorbar(im)
    cbar.ax.set_ylabel('Количество ставок')

    axis.set_title('Статистика цен по запросу', fontdict={'fontsize': 20, 'fontweight': 'medium'})
    axis.set_xlabel('Время завершения аукциона, часовой пояс GMT', fontsize=12)
    axis.set_ylabel('Итоговая цена, USD', fontsize=12)
    fig.autofmt_xdate()
    date_format = mpl_dates.DateFormatter('%d-%m-%Y %H:%M')
    axis.xaxis.set_major_formatter(date_format)
    fig.tight_layout()
    return fig


def plot_histogram(query_id):
    items_list = StatisticItems.query.filter(
        StatisticItems.query_id == query_id,
        StatisticItems.final_price.isnot(None)).order_by(
            StatisticItems.end_time.asc()).all()
    final_prices = []
    for item in items_list:
        final_prices.append(item.final_price)

    plt.style.use('seaborn')
    fig = Figure(figsize=(10, 5))
    axis = fig.add_subplot(1, 1, 1)
    im = axis.hist(final_prices, bins=8, edgecolor='black')

    axis.set_title('Статистика цен по запросу', fontdict={'fontsize': 20, 'fontweight': 'medium'})
    axis.set_xlabel('Итоговая цена, USD', fontsize=12)
    axis.set_ylabel('Количество лотов', fontsize=12)
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig
