import pandas as pd
import requests
import datetime

dt_now = datetime.datetime.today().strftime('%Y%m%d')


def cpi_meta(req='urls'):
    """
    req == 'urls' -> Add url_prefix to the values in the cpi dictionary
    req == 'file_names' -> 'cpi_' + key + '.txt'
    """
    url_prefix = 'https://download.bls.gov/pub/time.series/cu/cu.'
    cpi = {
        'area': 'area',
        'base': 'base',
        'data': 'data.1.AllItems',
        'population': 'data.19.PopulationSize',
        'foot': 'footnote',
        'item': 'item',
        'period': 'period',
        'periodicity': 'periodicity',
        'seasonal': 'seasonal',
        'series': 'series'
    }
    if req == 'urls':
        for key in cpi.keys():
            cpi[key] = url_prefix + cpi[key]
    elif req == 'file_names':
        for key in cpi.keys():
            cpi[key] = 'cpi_' + key + '.txt'
    return cpi


def remove_newlines(x):
    if isinstance(x, str):
        x = x.replace('\n', '').strip()
    return x


def create_dataframe(req):
    file_names = cpi_meta(req='file_names')
    output_file = file_names[req]

    # Read data from txt
    vars()['df_' + req] = pd.read_csv(output_file, sep='\t', lineterminator='\r')

    # Clean column names
    dict_rename = {}
    for col in vars()['df_' + req].columns.to_list():
        dict_rename.update({col: col.strip()})
        vars()['df_' + req][col] = vars()['df_' + req][col].apply(lambda x: remove_newlines(x))

    # Clean data
    vars()['df_' + req] = vars()['df_' + req].rename(columns=dict_rename)
    col_to_check = vars()['df_' + req].columns.to_list()[0]
    vars()['df_' + req] = vars()['df_' + req].dropna(subset=[col_to_check])
    vars()['df_' + req] = vars()['df_' + req][vars()['df_' + req][col_to_check] != '']
    return vars()['df_' + req]


def main():
    # Prep data and metadata dictionaries
    urls = cpi_meta(req='urls')
    file_names = cpi_meta(req='file_names')

    for req in urls.keys():
        # Gather metadata
        url = urls[req]
        output_file = file_names[req]
        print(f'{req}: {url} -> {output_file}')

        # Download data from url (requests.get), save as txt
        with open(output_file, "wb") as f:
            f.write(requests.get(url).content)

    df_area = create_dataframe('area')
    df_base = create_dataframe('base')
    df_data = create_dataframe('data')
    df_foot = create_dataframe('foot')
    df_item = create_dataframe('item')
    df_period = create_dataframe('period')
    df_periodicity = create_dataframe('periodicity')
    df_population = create_dataframe('population')
    df_seasonal = create_dataframe('seasonal')
    df_series = create_dataframe('series')

    # Combine data
    df_data['series_title'] = df_data.merge(df_series, how='left',
                                            left_on='series_id', right_on='series_id')['series_title']
    df_data['seasonal_code'] = df_data['series_id'].apply(lambda x: x[2:3])
    df_data['seasonal'] = df_data.merge(df_seasonal, how='left',
                                        left_on='seasonal_code', right_on='seasonal_code')['seasonal_text']
    df_data['periodicity_code'] = df_data['series_id'].apply(lambda x: x[3:4])
    df_data['periodicity'] = df_data.merge(df_periodicity, how='left',
                                           left_on='periodicity_code', right_on='periodicity_code')['periodicity_name']
    df_data['area_code'] = df_data['series_id'].apply(lambda x: x[4:8])
    df_data['area'] = df_data.merge(df_area, how='left',
                                    left_on='area_code', right_on='area_code')['area_name']
    df_data['item_code'] = df_data['series_id'].apply(lambda x: x[8:11])
    df_data['item'] = df_data.merge(df_item, how='left',
                                    left_on='item_code', right_on='item_code')['item_name']

    df_data.to_csv(f'cpi_{dt_now}.csv', index=False)
    print('Pause here.')
    print('')


if __name__ == '__main__':
    main()

