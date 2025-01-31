import streamlit as st
import pandas as pd
import numpy as np





def cleaup_data(df):
        data         = []
        previous_row = []
        id           = ''
        name         = ''

        for index, row in df.iterrows():
            if len(previous_row) == 0:
                previous_row = row
                continue

            if not pd.isna(previous_row['Pay Type']):
                if 'ID' in previous_row['Pay Type']:
                    id   = previous_row['Pay Type'].split(' ')[1]
                    name = previous_row['Reg']
                
                if not pd.isna(row['Pay Type']):
                    if not pd.isna(row['Department']):
                        if row['Department'] != 'Department':
                            data.append([id, name, row['Pay Type'], float(row['Reg']), float(row['OT1']) + float(row['OT2']), row['Department']])

            previous_row = row
        
        df = pd.DataFrame(data, columns=['ID','Employee','Pay Type','Reg','OT','Department'])
        df = df[['ID','Employee','Reg','OT','Department']]
        df = df.groupby(['ID','Employee','Department']).agg('sum').reset_index()
        df = df.sort_values('Department')
        df = df[['ID','Employee','Reg','OT','Department']]
        
        return df





st.set_page_config(page_title='Labor Distribution', page_icon='📄', layout='wide', initial_sidebar_state='auto', menu_items=None)

st.caption('VACAYZEN')
st.title('Labor Distribution')
st.info('Convert the Paylocity Master Timecard Summary into labor distribution files.')

file = st.file_uploader('Master Timecard Summary','xls')

if file:
    
    df1         = pd.read_excel(file, sheet_name='Sheet2', header=None).dropna(how='all')
    df2         = pd.read_excel(file, sheet_name='Sheet4', header=None).dropna(how='all')
    df1.columns = ['Pay Type','Reg','OT1','OT2','Ttl Paid','Ttl Unpd','Department']
    df2.columns = ['Pay Type','Reg','OT1','OT2','Ttl Paid','Ttl Unpd','Department']
    df1         = cleaup_data(df1)
    df2         = cleaup_data(df2)
    df          = pd.concat([df1, df2]).sort_values('Department')
    
    l, r = st.columns(2)
    l.subheader('30A BEACH HOSPITALITY HOLDINGS, LLC')
    l.dataframe(df1, use_container_width=True, hide_index=True)

    r.subheader('RGH LSV, LLC')
    r.dataframe(df2, use_container_width=True, hide_index=True)

    l, r = st.columns(2)
    ll, lr = l.columns(2)
    ll.metric('Reg', np.sum(df1.Reg))
    lr.metric('OT', np.sum(df1.OT))
    rl, rr = r.columns(2)
    rl.metric('Reg', np.sum(df2.Reg))
    rr.metric('OT', np.sum(df2.OT))

    st.divider()

    st.subheader('COMBINED')
    st.dataframe(df, use_container_width=True, hide_index=True)
    l, r = st.columns(2)
    l.metric('Reg', np.sum(df.Reg))
    r.metric('OT', np.sum(df.OT))