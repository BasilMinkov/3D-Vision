import pandas as pd


# The following functions are used form making excel tables. They are basically used only ones :(


def real_mult_log(data='apex_by_ten.csv', name='Bar Plots Info.xlsx'):
    """ Creates a data frame and excel book with all the essential data about
    simulation. Default input data – .csv file, got after implementing the apex_by_ten function.
    Default output book's name is Bar Plots Info.xlsx. """

    writer = pd.ExcelWriter(name, engine='xlsxwriter')
    df = pd.read_csv(data, header=None)
    df.to_excel(writer, 'Data')
    invalid = df.loc[:, [10]].sum(axis=1)
    zero = df.loc[:, [11, 20, 21]].sum(axis=1)
    df1 = pd.concat([invalid, zero], axis=1).rename(columns={0: 'Invalid', 1: 'Number of interpretations is 0'})
    df2 = pd.concat([df1, df.loc[:, 1:4]], axis=1)
    counter = 20
    li = []
    by_ten_li = []
    for i in range(df2.shape[0]):
        real = df2.iloc[i, :]
        real.name = 'Real'
        by_ten = df2.iloc[i, :].apply(lambda x: x * 10 if x != 0 else 1)
        by_ten.name = 'Mult By 10'
        by_ten_li.append(list(by_ten)[1:])
        log_ten = by_ten.apply(np.log10)
        log_ten.name = 'Log10'
        df3 = pd.concat([real, by_ten, log_ten], axis=1).transpose()
        counter += 2
        li.append(counter)
        df3.to_excel(writer, 'Data', startrow=counter)
        counter += 5
    worksheet = writer.sheets['Data']
    worksheet.set_column('C:C', 26)
    for i in range(18):
        worksheet.write('A{}'.format(li[i]), '{lo}-{hi}'.format(lo=i * 10, hi=(i + 1) * 10))
    writer.save()
    return df3, by_ten_li