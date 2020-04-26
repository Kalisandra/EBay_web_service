from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates


from datetime import datetime, timedelta


# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import datetime as dt

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
    fig = plt.figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.scatter(x_data, y_data, c=colors, cmap='Reds', edgecolor='black', linewidths=1)
    plt.gcf().autofmt_xdate()
    date_format = mpl_dates.DateFormatter('%d-%m-%Y %H:%M')
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.title('Статистика цен по запросу')
    plt.xlabel('Время завершения аукциона')
    plt.ylabel('Итоговая цена, USD')

    # cbar = plt.colorbar()
    # cbar.set_label('Количество ставок')
    return fig




    # plt.style.use('seaborn')
    # plt.scatter(x_data, y_data, c=colors, cmap='Reds', edgecolor='black', linewidths=1)





    # plt.plot_date(x_data, y_data)

    plt.gcf().autofmt_xdate()
    date_format = mpl_dates.DateFormatter('%d-%m-%Y %H:%M')
    plt.gca().xaxis.set_major_formatter(date_format)
    # plt.tight_layout()
    plt.show()
    # return plt.savefig("diagram.png")




# np.random.seed(19680801)
# data = np.random.randn(2, 100)

# fig, axs = plt.subplots(2, 2, figsize=(5, 5))
# axs[0, 0].hist(data[0])
# axs[1, 0].scatter(data[0], data[1])
# axs[0, 1].plot(data[0], data[1])
# axs[1, 1].hist2d(data[0], data[1])

# plt.show()

# data_date = statistic_data.query.filter(final_price==True, filter_by(end_time)