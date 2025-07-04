#ill import some necessary libraries of python here 

import pandas as pd 
import streamlit as st
import datetime 
import plotly.express as px

st.title("AI POWERED SMART ENERGY SAVER")

myfile=st.file_uploader("Upload your weekly energy usages excel datasheet: ",type=['xlsx'])
if myfile : 
    df=pd.read_excel(myfile)

    df["Day"]=df["Day"].astype(str)#making sure that the day column elements are sring type rather than numbers/hidden excel format


    today=datetime.datetime.today().strftime("%A")# getting todays name to be used as default*


    specific_col= [col for col in df.columns if col not in ["Day","Time","Total Consumption (kWh)"] ]


## the bar chart portion 

    st.subheader("📊 Stacked Bar Chart: Appliance Usage by Hour") 
    week_day = df['Day'].unique().tolist() #it creats a list of days to be used in the dropdown 

    selected_day= st.selectbox("Select the day for bar chart",week_day,index=week_day.index(today) if today in week_day else 0 ) #basically a dropdown box user can select a specific day by default itll show today's day

    selected_day2= df[df["Day"]==selected_day]

    selected_day3= selected_day2[["Time"]+specific_col]

    selected_day3_melted = selected_day3.melt(id_vars='Time', value_vars=specific_col, var_name='Appliance', value_name='Usage')

    bar=px.bar (selected_day3_melted, 
             x="Time",
             y="Usage",
             color="Appliance",
             title=f' Hourly Appliance Usage Breakdown - {selected_day}',
             labels={"Usage":"kWh"} 

             )
    bar.update_layout(barmode="stack")# idk its not working 
    bar.update_layout(title_x=0.5, xaxis=dict(dtick=1), legend_title_text='Appliances')
    st.plotly_chart(bar, use_container_width=True)



#pie chart portion 
    st.subheader("Pie Chart: Appliance Usage by Hour") 

    selected_din=st.selectbox("Select the day for the pie chart",week_day,index=week_day.index(today) if today in week_day else 0)
    selected_din2= df[df["Day"]==selected_din]
    selected_din3= selected_din2[specific_col].sum().reset_index()
    selected_din3.columns=["Appliance","Usage"]

    pie=px.pie(
        selected_din3,
        values="Usage",
        names="Appliance",
        title=f"Appliance usage share - {selected_din}"

    )
    pie.update_layout(title_x=0.5)
    st.plotly_chart(pie,use_container_width=True)



    
