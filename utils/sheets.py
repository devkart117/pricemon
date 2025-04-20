import os

import pandas as pd


def get_google_sheet_as_dataframe(url):
    df = pd.read_csv(url)
    return df

def get_blinkit_data():
    return get_google_sheet_as_dataframe('https://docs.google.com/spreadsheets/d/1dBgCwQshJ-cZV7jPRiKSxuZEOQIHAV8wKO8widdRknk/export?gid=0&format=csv').to_dict(orient='records')


def get_zepto_data():
    return get_google_sheet_as_dataframe('https://docs.google.com/spreadsheets/d/1z-srXgF9O5EIG-UuXNqRwG4IoAfxKMeG6qGOZSA3-V0/export?gid=2073622558&format=csv').to_dict(orient='records')


def get_amazon_data():
    return get_google_sheet_as_dataframe('https://docs.google.com/spreadsheets/d/1kgqFc2pYijdyYhcDB0JJ3dwnY5ONj5zMlb576hdaZj0/export?gid=0&format=csv').to_dict(orient='records')


def get_flipcart_data():
    return get_google_sheet_as_dataframe('https://docs.google.com/spreadsheets/d/1kgqFc2pYijdyYhcDB0JJ3dwnY5ONj5zMlb576hdaZj0/export?gid=31823053&format=csv').to_dict(orient='records')


def get_1mg_data():
    return get_google_sheet_as_dataframe('https://docs.google.com/spreadsheets/d/1kgqFc2pYijdyYhcDB0JJ3dwnY5ONj5zMlb576hdaZj0/export?gid=1811929831&format=csv').to_dict(orient='records')


def get_nykaa_data():
    return get_google_sheet_as_dataframe('https://docs.google.com/spreadsheets/d/1kgqFc2pYijdyYhcDB0JJ3dwnY5ONj5zMlb576hdaZj0/export?gid=1704332346&format=csv').to_dict(orient='records')


def get_hyugalife_data():
    return get_google_sheet_as_dataframe('https://docs.google.com/spreadsheets/d/1kgqFc2pYijdyYhcDB0JJ3dwnY5ONj5zMlb576hdaZj0/export?gid=1022515349&format=csv').to_dict(orient='records')


def color_cells(df):
    def color_cell(s):
        if s.name.startswith('scraped_'):
            source_col = 'source_' + s.name[8:]
            style_list = []
            for scraped, source in zip(s, df[source_col]):
                try:
                    if scraped > source:
                        style_list.append('background-color: green')
                    elif scraped < source:
                        style_list.append('background-color: red')
                    else:
                        style_list.append('background-color: gray')
                except:
                    style_list.append('')
            return style_list
        else:
            return [''] * len(s)

    return df.style.apply(color_cell)


def compile_data(amazon_data, flipcart_data, one_mg_data, nykaa_data, hugalife_data, blinkit_data, zepto_data):
    if not os.path.exists('data'):
        os.makedirs('data')
    
    excel_writer = pd.ExcelWriter('data/output.xlsx', engine='xlsxwriter')
    
    color_cells(pd.DataFrame(data=amazon_data)).to_excel(excel_writer, sheet_name='Amazon', index=False)
    color_cells(pd.DataFrame(data=flipcart_data)).to_excel(excel_writer, sheet_name='Flipcart', index=False)
    color_cells(pd.DataFrame(data=one_mg_data)).to_excel(excel_writer, sheet_name='1mg', index=False)
    color_cells(pd.DataFrame(data=nykaa_data)).to_excel(excel_writer, sheet_name='Nykaa', index=False)
    color_cells(pd.DataFrame(data=hugalife_data)).to_excel(excel_writer, sheet_name='HyugaLife', index=False)
    color_cells(pd.DataFrame(data=blinkit_data)).to_excel(excel_writer, sheet_name='Blinkit', index=False)
    color_cells(pd.DataFrame(data=zepto_data)).to_excel(excel_writer, sheet_name='Zepto', index=False)

    excel_writer._save()
