import pandas as pd

pd.options.display.float_format = '{:,.2f}'.format

df_data = pd.read_csv('data_df.csv')
df_contr = pd.read_csv('contract_df.csv')

# Поиищем информацию по контрагенту KONTROLYUM OTOMASYON SISTEMLERI ООО
# изобщего пула информацмм выбираем только отвечающего условию
df_owner = df_contr.loc[(df_contr['contract_owner']=='KONTROLYUM OTOMASYON SISTEMLERI ООО'), \
                        ['lot_number', 'lot_end_date', 'contract_number', 'contract_date',
       'contract_actor', 'contract_owner', 'goods_name', 'vendor_unit',
       'goods_qty', 'unit', 'unit_price', 'amount_of_goods',
       'additional_expenses', 'total_price', 'currency']]

df_own_tmp = df_owner.groupby(['lot_number', 'lot_end_date', 'contract_number', 'contract_date',
       'contract_actor', 'contract_owner', 'goods_name', 'vendor_unit',
       'goods_qty', 'unit', 'unit_price', 'amount_of_goods',
       'additional_expenses', 'total_price', 'currency']).sum()

# df_own_tmp.to_excel(r'C:\Users\dzhamshed.amonov\Kontrolium.xlsx', index=False)

writer = pd.ExcelWriter('example.xlsx', engine='xlsxwriter')

df_own_tmp.to_excel(writer, 'Sheet1')

writer._save()
