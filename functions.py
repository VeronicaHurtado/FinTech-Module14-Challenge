from constants import SIGNALS_COLUMNS


def direct_rule_of_three(a, b, c):
    return (b * c) / a


def generate_moving_average(df, window):
    return df[SIGNALS_COLUMNS.CLOSE].rolling(window=window).mean()


# Visualise the entry positions relative to the given relative_column (e.g. 'CLOSE' for close price)
def get_entry_plot(df, relative_column, ylabel):
    return df[df[SIGNALS_COLUMNS.ENTRY_EXIT] == 1.0][SIGNALS_COLUMNS[relative_column]].hvplot.scatter(
        color='purple',
        marker='^',
        legend=False,
        ylabel=ylabel,
        width=1000,
        height=400
    )


# Visualise the exit positions relative to the given relative_column (e.g. 'CLOSE' for close price)
def get_exit_plot(df, relative_column, ylabel):
    return df[df[SIGNALS_COLUMNS.ENTRY_EXIT] == -1.0][SIGNALS_COLUMNS[relative_column]].hvplot.scatter(
        color='yellow',
        marker='v',
        legend=False,
        ylabel=ylabel,
        width=1000,
        height=400
    )


# Visualise the "dynamic_column"
def get_dynamic_column_plot(df, dynamic_column, ylabel):
    return df[[SIGNALS_COLUMNS[dynamic_column]]].hvplot(
        line_color='lightgray',
        ylabel=ylabel,
        width=1000,
        height=400
    )


def plot_entry_exit_by_moving_averages(df, moving_avg_columns, relative_column, ylabel):
    entry_plot = get_entry_plot(df, relative_column, ylabel)
    exit_plot = get_exit_plot(df, relative_column, ylabel)

    # Visualise the "relative_column" for the investment
    relative_column_plot = get_dynamic_column_plot(df, relative_column, ylabel)

    # Visualise the moving averages
    moving_avgs = df[moving_avg_columns].hvplot(
        ylabel=ylabel,
        width=1000,
        height=400
    )

    # Overlay the plots
    return relative_column_plot * moving_avgs * entry_plot * exit_plot


def plot_entry_exit(df, relative_column, ylabel):
    entry_plot = get_entry_plot(df, relative_column, ylabel)
    exit_plot = get_exit_plot(df, relative_column, ylabel)

    # Visualise the "relative_column" for the investment
    relative_column_plot = get_dynamic_column_plot(df, relative_column, ylabel)

    # Overlay the plots
    return relative_column_plot * entry_plot * exit_plot


# Backtest the Trading Strategy
def get_position(df, share_size):
    return share_size * df[SIGNALS_COLUMNS.SIGNAL]


# Find the points-in-time where the share position is bought or sold
def get_entry_exit_position(df):
    return df[SIGNALS_COLUMNS.POSITION].diff()


# Multiply share price by entry/exit positions and get the cumulative sum
def get_portfolio_holdings(df):
    return (
        df[SIGNALS_COLUMNS.CLOSE] * df[SIGNALS_COLUMNS.POSITION].cumsum()
    )


# Subtract the initial capital by the portfolio holdings to get the amount of liquid cash in the portfolio
def get_portfolio_cash(df, initial_capital):
    return (
        initial_capital - (df[SIGNALS_COLUMNS.CLOSE] * df[SIGNALS_COLUMNS.ENTRY_EXIT_POSITION]).cumsum()
    )


# Get the total portfolio value by adding the cash amount by the portfolio holdings (or investments)
def get_portfolio_total(df):
    return (
        df[SIGNALS_COLUMNS.PORTFOLIO_CASH] + df[SIGNALS_COLUMNS.PORTFOLIO_HOLDINGS]
    )


# Calculate the portfolio daily returns
def get_portfolio_daily_returns(df):
    return df[SIGNALS_COLUMNS.PORTFOLIO_TOTAL].pct_change()


# Calculate the cumulative returns
def get_portfolio_cumulative_returns(df):
    return (
        1 + df[SIGNALS_COLUMNS.PORTFOLIO_DAILY_RETURNS]
    ).cumprod() - 1

