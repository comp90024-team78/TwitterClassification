import pandas as pd

# Input format: YYYYmmDD
def get_date_range(start_date, end_date):
    '''
    This method is used to get the date range list between two dates

    Args:
        start_date:         Date of starting harvesting
        end_date:           Date of ending harvesting

    Returns:
        List of date range where zero at start of month and day will be erased
        e.g. return 2015,1,1 instead of 2015,01,01
    '''
    date_str_range = []
    date_range = pd.date_range(start=start_date ,end=end_date)
    for date_stamp in date_range:
        year = str(int(date_stamp.strftime('%Y')))
        month = str(int(date_stamp.strftime('%m')))
        day = str(int(date_stamp.strftime('%d')))   
        date_str_range.append(year+','+month+','+day)
    return date_str_range

# Test method
def test(start_date, end_date):
    print(get_date_range(start_date, end_date))

if __name__ == '__main__':
    test('20140101', '20140301')
