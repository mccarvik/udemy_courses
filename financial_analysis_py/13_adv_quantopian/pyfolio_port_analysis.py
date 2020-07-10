#!/usr/bin/env python
# coding: utf-8

# # PyFolio Portfolio Analysis
import pyfolio as pf
import matplotlib.pyplot as plt
import empyrical
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/13_adv_quantopian/figs/'

# ## Set A Benchmark Algo for SPY
def initialize(context):
    context.spy = sid(8554)
    set_max_leverage(1.01)
    schedule_function(rebalance,date_rules.every_day(),time_rules.market_open())
    
def rebalance(context,data):
    order_target_percent(context.spy,1)

# Get benchmark returns
benchmark_rets = get_backtest('5986c511c94d014fc81acf7b')
bm_returns = benchmark_rets.daily_performance['returns']
bm_positions = benchmark_rets.pyfolio_positions
bm_transactions = benchmark_rets.pyfolio_transactions


# ### Use Algo from Leverage Lecture
# Use same algo as in the Leverage Lecture!
bt = get_backtest('5986b969dbab994fa4264696')
bt_returns = bt.daily_performance['returns']
bt_positions = bt.pyfolio_positions
bt_transactions = bt.pyfolio_transactions

bt_returns.plot()
plt.savefig(PATH + 'rets.png', dpi=300)
plt.close()

print(empyrical.beta(bt_returns,bm_returns))

# # PyFolio Plots
benchmark_rets = bm_returns

# Cumulative Returns
plt.subplot(2,1,1)
pf.plotting.plot_rolling_returns(bt_returns, benchmark_rets)

# Daily, Non-Cumulative Returns
plt.subplot(2,1,2)
pf.plotting.plot_returns(bt_returns)
plt.tight_layout()
plt.savefig(PATH + 'daily_and_cum_rets.png', dpi=300)
plt.close()

fig = plt.figure(1)
plt.subplot(1,3,1)
pf.plot_annual_returns(bt_returns)
plt.subplot(1,3,2)
pf.plot_monthly_returns_dist(bt_returns)
plt.subplot(1,3,3)
pf.plot_monthly_returns_heatmap(bt_returns)
plt.tight_layout()
fig.set_size_inches(15,5)
plt.savefig(PATH + 'returns_charts.png', dpi=300)
plt.close()

pf.plot_return_quantiles(bt_returns);
plt.savefig(PATH + 'quantiles.png', dpi=300)
plt.close()

pf.plot_rolling_beta(bt_returns, benchmark_rets);
plt.savefig(PATH + 'roll_beta.png', dpi=300)
plt.close()

pf.plot_rolling_sharpe(bt_returns);
plt.savefig(PATH + 'roll_sharpe.png', dpi=300)
plt.close()

pf.plot_rolling_fama_french(bt_returns);
plt.savefig(PATH + 'fama_french.png', dpi=300)
plt.close()

pf.plot_drawdown_periods(bt_returns);
plt.savefig(PATH + 'drawdown.png', dpi=300)
plt.close()

pf.plot_drawdown_underwater(bt_returns);
plt.savefig(PATH + 'underwater.png', dpi=300)
plt.close()

pf.plot_gross_leverage(bt_returns, bt_positions);
plt.savefig(PATH + 'gross_lev.png', dpi=300)
plt.close()

pos_percent = pf.pos.get_percent_alloc(bt_positions)
pf.plotting.show_and_plot_top_positions(bt_returns, pos_percent);
plt.savefig(PATH + 'top_pos.png', dpi=300)
plt.close()

pf.plot_turnover(bt_returns, bt_transactions, bt_positions);
plt.savefig(PATH + 'turnover.png', dpi=300)
plt.close()

pf.plotting.plot_daily_turnover_hist(bt_transactions, bt_positions);
plt.savefig(PATH + 'turnover_hist.png', dpi=300)
plt.close()

pf.plotting.plot_daily_volume(bt_returns, bt_transactions);
plt.savefig(PATH + 'daily_vol.png', dpi=300)
plt.close()

pf.create_round_trip_tear_sheet(bt_returns, bt_positions, bt_transactions);
plt.savefig(PATH + 'tear_sheet.png', dpi=300)
plt.close()
