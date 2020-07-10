#!/usr/bin/env python
# coding: utf-8

# # Futures
# 
# Extra Resources: 
# 
# * https://en.wikipedia.org/wiki/Futures_contract
# * http://www.investopedia.com/terms/f/futurescontract.asp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
PATH = '/home/ec2-user/environment/udemy_courses/financial_analysis_py/13_adv_quantopian/figs/'

# ## Getting Futures
# 
# A reference to a futures contract is obtained via the symbols function. Futures
# contracts are denoted by a base symbol + a code for month/year of delivery. 
# CLF16 is a contract for crude oil (CL) with delivery in January (F) 2016 (16).
# 
# ### List of all Available Futures (on Quantopian)

# Symbol | Future |
# --- | --- | 
# BD | Big Dow
# BO | Soybean Oil
# CM | Corn E-Mini
# CN | Corn
# DJ | DJIA Futures
# ET | Ethanol
# FF | 30-Day Federal Funds
# FI | 5-Year Deliverable Interest Rate Swap Futures
# FS | 5-Year Interest Rate Swap Futures
# FV | 5-Year T-Note
# MB | Municipal Bonds
# MS | Soybeans E-Mini
# MW | Wheat E-Mini
# OA | Oats
# RR | Rough Rice
# SM | Soybean Meal
# SY | Soybeans
# TN | 10-Year Deliverable Interest Rate Swap Futures
# TS | 10-Year Interest Rate Swap Futures
# TU | 2-Year T-Note
# TY | 10-Year T-Note
# UB | Ultra Tbond
# US | 30-Year T-Bond
# WC | Wheat
# YM | Dow Jones E-mini
# VX | VIX Futures
# AD | Australian Dollar
# AI | Bloomberg Commodity Index Futures
# BP | British Pound
# CD | Canadian Dollar
# EC | Euro FX
# ED | Eurodollar
# EE | Euro FX E-mini
# ES | S&P 500 E-Mini
# EU | E-micro EUR/USD Futures
# FC | Feeder Cattle
# JE | Japanese Yen E-mini
# JY | Japanese Yen
# LB | Lumber
# LC | Live Cattle
# LH | Lean Hogs
# MD | S&P 400 MidCap Futures
# ME | Mexican Peso
# MI | S&P 400 MidCap E-Mini
# ND | NASDAQ 100 Futures
# NK | Nikkei 225 Futures
# NQ | NASDAQ 100 E-Mini
# NZ | New Zealand Dollar
# SF | Swiss Franc
# SP | S&P 500 Futures
# TB | TBills
# GC | Gold
# HG | Copper High Grade
# SV | Silver
# CL | Light Sweet Crude Oil
# HO | NY Harbor ULSD Futures
# HU | Unleaded Gasoline
# NG | Natural Gas
# PA | Palladium
# PL | Platinum
# PB | Pork Bellies
# QG | Natural Gas E-mini
# QM | Crude Oil E-Mini
# XB | RBOB Gasoline Futures
# EI | MSCI Emerging Markets Mini
# EL | Eurodollar NYSE LIFFE
# MG | MSCI EAFE Mini
# XG | Gold mini-sized
# YS | Silver mini-sized
# RM | Russell 1000 Mini
# SB | Sugar #11
# ER | Russell 2000 Mini

# ## List of Date/Time Codes

# Month | Code |
# --- | --- | 
# January | F
# February | G
# March | H
# April | J
# May | K
# June | M
# July | N
# August | Q
# September | U
# October | V
# November | X
# December | Z

# Let's grab the future contract data for Natural Gas for a maturity date 
# of January 2018. (If you are viewing this lecture some time in the future,
# choose a further out maturity date)
future_contract = symbols('NGF18')
print(future_contract.asset_name)

for key in future_contract.to_dict():
    print(key)
    print(future_contract.to_dict()[key])
    print('\n')

futures_position_value = get_pricing(future_contract, start_date = '2017-01-01', end_date = '2018-01-01', fields = 'price')
futures_position_value.name = futures_position_value.name.symbol
futures_position_value.plot()
plt.title('NG Futures Price')
plt.xlabel('Date')
plt.ylabel('Price');
plt.savefig(PATH + 'ng_price.png', dpi=300)
plt.close()

# ## Historical Data
from quantopian.research.experimental import history
print(history.__doc__)

ngf18 = future_contract
ngf18_data = history(ngf18, 
                     fields=['price', 'open_price', 'high', 'low', 'close_price', 'volume', 'contract'], 
                     frequency='daily', 
                     start_date='2017-06-01', 
                     end_date='2017-08-01')
print(ngf18_data.head())

# Notice the 4th of July!
ngf18_data['volume'].plot(kind='bar')
plt.savefig(PATH + 'ng_plot_bar.png', dpi=300)
plt.close()

# ## Comparison of Different Maturity Dates
ng_contracts = symbols(['NGF17', 'NGG17', 'NGH17', 'NGJ17', 'NGK17', 'NGM17'])

ng_consecutive_contract_volume = history(ng_contracts, 
                                         fields='volume', 
                                         frequency='daily', 
                                         start_date='2016-01-01', 
                                         end_date='2017-08-01')
ng_consecutive_contract_volume.plot()
plt.savefig(PATH + 'ng_cons.png', dpi=300)
plt.close()

ng_consecutive_contract_volume.plot(xlim=['2016-10-01','2017-08-01'])
plt.savefig(PATH + 'ng_cons_2017.png', dpi=300)
plt.close()

# Trading activity jumps from one contract to the next. Transitions happen just 
# prior to the delivery date of each contract.
# 
# This phenomenon can make it difficult to work with futures. Having to explicitly 
# reference a series of transient contracts when trading or simulating futures 
# can be a hassle.
# 
# In order to trade consecutive contracts for the same underlying future, we 
# can use what's called a "Continuous Future".

# # Continuous Futures
# 
# Continuous futures are abstractions over the 'underlying' commodities/assets/indexes 
# of futures. For example, if we wanted to trade crude oil, we could create a 
# reference to CL, instead of a series of CL contracts. Continuous futures 
# essentially maintain a reference to a 'current' contract deemed to be the 
# active contract for the particular underlying.
# 
# We use the continuous futures objects as part of the platform to get a 
# continuous chain of historical data for futures contracts, taking these 
# concerns into account. There are several ways to adjust for the cost of carry 
# when looking at historical data, though people differ on what they prefer. The 
# general consensus is that an adjustment should be done.
# 
# Continuous futures are not tradable assets. They maintain a reference to the 
# current active contract related to a given underlying.
from quantopian.research.experimental import continuous_future
print(continuous_future.__doc__)

# There are 4 arguments that we need to consider.
# 
# - **`root_symbol`**: The root symbol of the underlying. For example, 'CL' for crude oil.
# - **`offset`**: The distance from the primary contract. 0 = primary, 1 = secondary,
# etc. We'll get into this more later.
# - **`roll`**: How to determine the 'current' contract of the continuous future. 
# Current options are **`'volume'`** and **`'calendar'`**. The 'volume' approach 
# chooses the current active contract based on trading volume. The 'calendar' 
# approach chooses the current active contract based simply on the `auto_close_date`s of each contract.**
# - **`adjustment`**: How to adjust historical prices from earlier contracts. 
# We'll get into this more later. Options are **`'mul'`**, **`'add'`**, or **`'None'`**.
continuous_ng = continuous_future('NG', offset=0, roll='volume', adjustment='mul')
print(continuous_ng)

ng_cont_active = history(continuous_ng, 
                    fields=['contract','price','volume'] ,
                    frequency='daily', 
                    start_date='2016-10-01', 
                    end_date='2017-08-01')
print(ng_cont_active.head())

ng_cont_active['price'].plot()
plt.savefig(PATH + 'price.png', dpi=300)
plt.close()

ng_cont_active['volume'].plot()
plt.savefig(PATH + 'vol.png', dpi=300)
plt.close()

ng_consecutive_contract_volume = history(ng_contracts, 
                                         fields='volume', 
                                         frequency='daily', 
                                         start_date='2016-10-01', 
                                         end_date='2017-08-01')

ax = ng_cont_active['volume'].plot(ls='--',c='black',lw=3)
ng_consecutive_contract_volume.plot(ax=ax)
plt.savefig(PATH + 'cont_active.png', dpi=300)
plt.close()

ng_consecutive_contract_price = history(ng_contracts, 
                                         fields='price', 
                                         frequency='daily', 
                                         start_date='2016-10-01', 
                                         end_date='2017-08-01')
ng_continuous_active = history(continuous_ng, 
                    fields=['contract','price','volume'] ,
                    frequency='daily', 
                    start_date='2016-10-01', 
                    end_date='2017-08-01')
ng_consecutive_contract_price.plot()
plt.savefig(PATH + 'cons_cont_price.png', dpi=300)
plt.close()

ng_cont_active['price'].plot(c='black',lw=3)
plt.savefig(PATH + 'active_cont_ng.png', dpi=300)
plt.close()

# This represents the price of the underlying commodity, NG, on the most actively 
# traded contract. Much easier to look at.
# 
# You might notice that the price at the start of this plot exceeds 4.0, but 
# when we plotted the individual contracts, it barely made it above 3.6.
# This is because the historical price is getting adjusted for jumps between contracts.
# 
# The best way to explain this is to plot the prices history of the unadjusted continuous future.
continuous_ng_unadjusted = continuous_future('NG', offset=0, roll='volume', adjustment=None)
ng_unadjusted_history = history(continuous_ng_unadjusted, 
                                fields=['contract', 'price'], 
                                frequency='daily', 
                                start_date='2016-10-01', 
                                end_date='2017-08-01')
print(ng_unadjusted_history.head())

ng_unadjusted_history.plot()
plt.savefig(PATH + 'unadj_hist.png', dpi=300)
plt.close()

ng_consecutive_contract_price.plot()
plt.savefig(PATH + 'cons_cont_price_w_unadj.png', dpi=300)
plt.close()

pivot_unadj = ng_unadjusted_history.pivot(index=ng_unadjusted_history.index,columns='contract')
print(pivot_unadj.head())

pivot_unadj.plot()
plt.savefig(PATH + 'pivot_plot.png', dpi=300)
plt.close()

ax = pivot_unadj.plot()
ng_unadjusted_history.plot(ax=ax,ls='--',c='black')
plt.savefig(PATH + 'pivot_hist.png', dpi=300)
plt.close()

# ## Adjustment Types
# 
# There are two main adjustment types, additive or multiplicative.
# 
# * Multiplicative adjustment, mul
# 
# This essentially computes the adjustment as the ratio of new contract price /
# old contract price whenever the active contract rolls to a new contract.
# 
# * Arithmetic adjustment, 'add'
# 
# The 'add' technique computes the adjustment as the difference new contract 
# price - old contract price.
