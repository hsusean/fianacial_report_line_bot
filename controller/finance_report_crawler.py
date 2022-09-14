import requests
import pandas as pd
import dataframe_image as dfi
from datetime import datetime
import os
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from pdf2image import convert_from_path
from matplotlib.backends.backend_pdf import PdfPages
# plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
# plt.rcParams['axes.unicode_minus'] = False



def quarter_transfer(month_chinese):
    if '3月' in month_chinese or '1季' in month_chinese:
        return 'Q1'
    elif '6月' in month_chinese or '2季' in month_chinese:
        return 'Q2'
    elif '9月' in month_chinese or '3季' in month_chinese:
        return 'Q3'
    elif '12月' in month_chinese or '4季' in month_chinese:
        return 'Q4'

def get_each_stock_finance_report(stock_id, report_type, year=None, season=None, ):
    if not year:
        year = datetime.today().year - 1911
    if not season:
        season = 1
    season_seq = [4,3,2,1,4,3,2,1]
    if report_type == '資產負債表' or report_type == 'a':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t164sb03'
    elif report_type == '綜合損益表' or report_type == 'b':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t164sb04'
    elif report_type == '現金流量表' or report_type == 'c':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t164sb05'    
    elif report_type == '權益變動表' or report_type == 'e':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t164sb06'
    else:
        raise ValueError('type does not match')
    payload = {
                'encodeURIComponent': '1',
                'step': '1',
                'firstin': '1',
                'off': '1',
                'queryName': 'co_id',
                'inpuType': 'co_id',
                'TYPEK': 'all',
                'isnew': 'false',
                'co_id': str(stock_id),
                'year': str(year),
                'season': str(season),
            }
    res = requests.post(url , data = payload)
    df = pd.read_html(res.text)[1]
    df_cols = list(df.columns)
    # reset column name for 資產負債表
    if report_type == '資產負債表' or report_type == 'a':
        for idx, col in enumerate(df_cols):
            if idx == 0:
                # df_cols[idx] = col[2]
                df_cols[idx] = 'item'
            else:
                if '年' in col[2]:
                    temp = col[2].split('年')
                    df_cols[idx] = temp[0]+quarter_transfer(temp[1])+col[3]
                else:
                    df_cols[idx] = ''
    # reset column name for 綜合損益表
    elif report_type == '綜合損益表' or report_type == 'b':
        for idx, col in enumerate(df_cols):
            if idx == 0:
                # df_cols[idx] = col[2]
                df_cols[idx] = 'item'
            else:
                if season == 1:
                    temp = col[2].split('年')
                    df_cols[idx] =  temp[0] + 'Q1'+col[3]
                elif '至' in col[2]:
                    temp = col[2].split('至')[1].split('年') # ['110', '09月30日']
                    df_cols[idx] = temp[0]+'Q1-'+quarter_transfer(temp[1])+col[3]
                elif '度' in col[2]:
                    temp = col[2].split('年')
                    df_cols[idx] = temp[0] +'Q1-Q4'+col[3]
                elif '年' in col[2]:
                    temp = col[2].split('年')
                    df_cols[idx] = temp[0]+quarter_transfer(temp[1])+col[3]
                else:
                    df_cols[idx] = ''
    # reset column name for 現金流量表
    elif report_type == '現金流量表' or report_type == 'c':
        for idx, col in enumerate(df_cols):
            if idx == 0:
                # df_cols[idx] = col[2]
                df_cols[idx] = 'item'
            else:
                if season == 1:
                    temp = col[2].split('年')
                    df_cols[idx] =  temp[0] + 'Q1'+col[3]
                elif '至' in col[2]:
                    temp = col[2].split('至')[1].split('年') # ['110', '09月30日']
                    df_cols[idx] = temp[0]+'Q1-'+quarter_transfer(temp[1])+col[3]
                elif '度' in col[2]:
                    temp = col[2].split('年')
                    df_cols[idx] = temp[0] +'Q1-Q4'+col[3]
                elif '年' in col[2]:
                    temp = col[2].split('年')
                    df_cols[idx] = temp[0]+quarter_transfer(temp[1])+col[3]
                else:
                    df_cols[idx] = ''
    df.columns = df_cols
    df = df.set_index('item')
    print(11111, df)
    print(11112, os.getcwd())
    # myfontprops = FontProperties(
    #                     fname='./.fonts/TaipeiSansTCBeta-Regular.ttf')#微软雅黑
    # # TaipeiSansTCBeta-Regular
    df.to_excel('123.xlsx')

    
    # 利用 Workbook 建立一個新的工作簿
    plt.rcParams['font.sans-serif'] = ['TaipeiSansTCBeta-Regular']
    fig, ax =plt.subplots(figsize=(12,4))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
    pp = PdfPages("foo.pdf")
    pp.savefig(fig, bbox_inches='tight')
    pp.close()

    
    pages = convert_from_path('foo.pdf', 500)
    for page in pages:
        page.save('out.jpg', 'JPEG')
    # dfi.export(df, '123.png',table_conversion='matplotlib')
    
    return df

def get_each_stock_annual_report(stock_id, report_type, years=None):
    """
    years : list -> years = [108, 109, 110]
    """
    if not years:
        years = [datetime.today().year - 1911]
    seasons = [1,2,3,4]
    idx_yeas = 0
    result = 0
    for year in years:
        idx_season = 0
        note = ''
        try:
            for season in seasons:
                try:
                    data = get_each_stock_finance_report(stock_id ,year, season, report_type)
                    data = data.fillna(0)
                    if report_type == 'b' or report_type == 'c':
                        if season == 1:
                            data_total = data[str(year)+'Q'+str(season)+'金額']
                            # continue
                        else:
                            data_total = data[str(year)+'Q1-Q'+str(season)+'金額']
                    if report_type == 'a':
                        if idx_season == 0:
                            data_total = data[str(year)+'Q'+str(season)+'金額']
                        else:
                            data_total = data_total.add(data[str(year)+'Q'+str(season)+'金額'])
                    note = ''
                except:
                    note = ' without '+ 'Q' + str(season) + 'with report type' + report_type
                    print('no data' , year, season, report_type)
                idx_season+=1
            temp = pd.DataFrame(data_total)
            temp.columns = [str(year) + note]
            if idx_yeas==0:
                result = temp
            else:
                # remove duplicate index first, then concat
                temp = temp[~temp.index.duplicated(keep='last')]
                result = result[~result.index.duplicated(keep='last')]
                result = pd.concat([result, temp], axis = 1)
            idx_yeas +=1
        except:
            print('no', year,' year data with report type ' ,report_type)
    return result

def finance_index(stock_id, years=None):
    if not years:
        years = [datetime.today().year - 1911]
    data_a = get_each_stock_annual_report(stock_id, years, 'a')
    data_b = get_each_stock_annual_report(stock_id, years, 'b')
    data_c = get_each_stock_annual_report(stock_id, years, 'c')


    asset = (data_a.loc['流動資產合計'] + data_a.loc['非流動資產合計'])
    debt = (data_a.loc['流動負債合計'] + data_a.loc['非流動負債合計'])
    equity = asset - debt
    stock_qty = data_a.loc['股本合計'] / 10

    # 現金佔總資產比 > 25%
    cash_asset_rate = data_a.loc['現金及約當現金'] / asset
    # 平均收現日數 < 15天
    avg_receive_cash_day = 365 / (data_b.loc['營業收入合計'] / (data_a.loc['應收帳款淨額']/4) )
    # 平均銷貨日數 
    avg_sale_day = 365 / (data_b.loc['營業成本合計'] / (data_a.loc['應收帳款淨額']/4) )

    # 存活能力
    # 現金流量比 >100%
    cash_flu_rate = data_c.loc['營業活動之淨現金流入（流出）'] / data_a.loc['流動負債合計']
    # 現金流量允當比率
    # (-1*data_c.loc['取得不動產、廠房及設備'] )+data_c.loc['存貨（增加）減少'] 
    # 現金再投資比率
    # 

    # 營運能力
    # 營業費用率 < 10%
    business_fee_rate = data_b.loc['營業費用合計'] / data_b.loc['營業收入合計']
    
    # ROE > 20%
    roe = data_b.loc['本期淨利（淨損）'] / equity
    # ROA
    roa = data_b.loc['本期淨利（淨損）'] / asset
    # 淨利率 > 2% 至少
    net_rate = data_b.loc['本期淨利（淨損）'] / data_b.loc['營業收入合計']
    # 總資產周轉率 > 1
    asset_tuenover = data_b.loc['營業收入合計'] / asset
    # 權益乘數
    equity_rate = asset / equity

    # 負債比 < 80%
    debt_rate = debt / asset

    # 長期負債與廠房比  > 1
    long_term_debt_rate = (data_a.loc['非流動負債合計'] + equity) / data_a.loc['不動產、廠房及設備']  

    # 償債能力
    # 流動比率 > 300%
    flu_rate = data_a.loc['流動資產合計'] / data_a.loc['流動負債合計']
    # 速動比率 >150%
    speed_flu_rate = (data_a.loc['流動資產合計'] - data_a.loc['存貨']) / data_a.loc['流動負債合計']

    # 本益比


    index_data = {
        "現金佔總資產比" : cash_asset_rate, 
        "平均收現日數" : avg_receive_cash_day, 
        "平均銷貨日數" : avg_sale_day, 
        "現金流量比" : cash_flu_rate,  
        "營業費用率" : business_fee_rate, 
        "ROE" : roe, 
        "ROA" : roa, 
        "淨利率" : net_rate, 
        "總資產周轉率" : asset_tuenover,
        "權益乘數": equity_rate,
        "負債比" : debt_rate, 
        "長期負債與廠房比" : long_term_debt_rate, 
        "流動比率" : flu_rate, 
        "速動比率" : speed_flu_rate, 
    }
    return pd.DataFrame(index_data).T


if __name__ == '__main__':
    years = [108,109]
    stock_id = 6669
    data = get_each_stock_finance_report(6669,'a')
    # index_table = finance_index(stock_id)
    # print(data)
