from datetime import datetime, timedelta

from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from matplotlib.figure import Figure

from webapp.favorite_searches.models import Statistic_items


def plot_statistics(query_id):
    items_list = Statistic_items.query.filter(
        Statistic_items.query_id == query_id, Statistic_items.final_price.isnot(None)).order_by(Statistic_items.end_time.asc()).all()
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
