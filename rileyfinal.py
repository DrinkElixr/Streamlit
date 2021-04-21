import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
import matplotlib.pyplot as plt
def load_data(loadna):
    df=pd.read_csv("rileydata.csv")
    if loadna==False:
        df=df.dropna()
    return df
def chart_options(index):
    st.header("Chart Options")
    c1,c2,c3,c4,c5=st.beta_columns(5)
    alpha=c2.slider("Select Transparency",0.0,1.0,.5,key=index)
    ascending=c3.selectbox("Ascending or Descending?",["Ascending","Descending"],key=index)
    color=c1.selectbox("Select Color for Charts",["purple","red","blue","green","yellow","orange","black","grey"],key=index)
    filter_by=c4.selectbox("Filter by Largest or Smallest",["Largest # of schools","Smallest # of schools"],key=index)
    keep=int(c5.number_input("How many records would you like to see?",key=index))



    return color,alpha,ascending,filter_by,keep
def filter_by_state(use,index):
    try:
        dfn=pd.read_csv("FilterbyState.csv")
    except:
        df=load_data(True)
        states=pd.unique(df["STATE"])
        d1=[]
        for state in states:
            d2=[]
            count=len(df[df["STATE"]==state])

            d2.append(state)
            d2.append(count)
            d2.append(df[df["STATE"]==state]["LON"].mean())
            d2.append(df[df["STATE"]==state]["LAT"].mean())
            d1.append(d2)
        dfn=pd.DataFrame(d1)
        dfn.columns=["state","number_of_schools","lon","lat"]
        dfn.to_csv("FilterbyState.csv")
    if use=="Maps":
        st.header("Map of Schools by State")
        view=pdk.ViewState(latitude=dfn["lat"].mean(),longitude=dfn["lon"].mean(),pitch=20,zoom=5)
        map = pdk.Layer("ColumnLayer",data=dfn,get_position=["lon", "lat"],get_elevation="number_of_schools",elevation_scale=1000,radius=10000,pickable=True,auto_highlight=True,get_fill_color=[225,225,225,225])
        tooltip = {"html": "<b>{state}</b>: {number_of_schools} schools","style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"}}
        map=pdk.Deck(map_provider='carto',layers=[map],initial_view_state=view,api_keys=None,tooltip=tooltip)
        st.pydeck_chart(map)
    if use=="Charts":
        color,alpha,ascending,filter_by,num_to_keep=chart_options(index)
        if filter_by=="Largest # of schools":
            dfn=dfn.nlargest(num_to_keep,columns=["number_of_schools"])
        else:
            dfn=dfn.nsmallest(num_to_keep,columns=["number_of_schools"])
        if ascending=="Ascending":
            dfn=dfn.sort_values(by="number_of_schools",ascending=True)
        else:
            dfn=dfn.sort_values(by="number_of_schools",ascending=False)
        objects = dfn["state"]
        y_pos = np.arange(len(objects))
        performance = dfn["number_of_schools"]
        plt.barh(y_pos, performance, align='center', alpha=alpha,color=color)
        plt.yticks(y_pos, objects)
        plt.xlabel('Number of Schools')
        plt.ylabel("States")
        plt.title('Number of Schools by State')
        st.pyplot(plt)
        plt.clf()
def filter_by_town(use,index):
    try:
        dfn=pd.read_csv("FilterbyTown.csv")
    except:
        df=load_data(True)
        df["st"]=df["STATE"]+","+df["CITY"]

        states=pd.unique(df["st"])
        d1=[]
        for state in states:
            d2=[]
            count=len(df[df["st"]==state])

            d2.append(state)
            d2.append(count)
            d2.append(df[df["st"]==state]["LON"].mean())
            d2.append(df[df["st"]==state]["LAT"].mean())
            d1.append(d2)
        dfn=pd.DataFrame(d1)
        dfn.columns=["town","number_of_schools","lon","lat"]
        dfn.to_csv("FilterbyTown.csv")

    if use=="Maps":
        st.header("Map of Schools by Town")
        view=pdk.ViewState(latitude=dfn["lat"].mean(),longitude=dfn["lon"].mean(),pitch=20,zoom=5)
        map = pdk.Layer("ColumnLayer",data=dfn,get_position=["lon", "lat"],get_elevation="number_of_schools",elevation_scale=1000,radius=1000,pickable=True,auto_highlight=True,get_fill_color=[225,225,225,225])
        tooltip = {"html": "<b>{town}</b>: {number_of_schools} schools","style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"}}
        map=pdk.Deck(map_provider='carto',layers=[map],initial_view_state=view,api_keys=None,tooltip=tooltip)
        st.pydeck_chart(map)
    if use=="Charts":
        color,alpha,ascending,filter_by,num_to_keep=chart_options(index)
        if filter_by=="Largest # of schools":
            dfn=dfn.nlargest(num_to_keep,columns=["number_of_schools"])
        else:
            dfn=dfn.nsmallest(num_to_keep,columns=["number_of_schools"])
        if ascending=="Ascending":
            dfn=dfn.sort_values(by="number_of_schools",ascending=True)
        else:
            dfn=dfn.sort_values(by="number_of_schools",ascending=False)
        objects = dfn["town"]
        y_pos = np.arange(len(objects))
        performance = dfn["number_of_schools"]
        plt.barh(y_pos, performance, align='center', alpha=alpha,color=color)
        plt.yticks(y_pos, objects)
        plt.xlabel('Number of Schools')
        plt.ylabel("Towns")
        plt.title('Number of Town')
        st.pyplot(plt)
        plt.clf()
def all_colleges(use,index):

    df=load_data(True)
    if use=="Maps":
        st.header("Map of all Schools")
        view=pdk.ViewState(latitude=df["LAT"].mean(),longitude=df["LON"].mean(),pitch=20,zoom=5)
        map = pdk.Layer("ColumnLayer",data=df,get_position=["LON", "LAT"],get_elevation=100,elevation_scale=1000,radius=500,pickable=True,auto_highlight=True,get_fill_color=[225,225,225,225])
        tooltip = {"html": "<b>{NAME}</b>: {STREET}, {CITY} {STATE}","style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"}}
        map=pdk.Deck(map_provider='carto',layers=[map],initial_view_state=view,api_keys=None,tooltip=tooltip)
        st.pydeck_chart(map)


def main():
    st.title("College Explorer")
    mm=st.sidebar.radio("What do you want to see?",["Maps","Charts"])
    if mm=="Maps":
        sm=st.multiselect("Which maps would you like to see? (can select more than 1)",["Colleges by State","All Colleges","Colleges by Town"])
        for i,x in enumerate(sm):
            if x=="Colleges by State":
                filter_by_state(mm,i)
            if x=="All Colleges":
                all_colleges(mm,i)
            if x=="Colleges by Town":
                filter_by_town(mm,i)
    if mm=="Charts":
        sm=st.multiselect("Which Chart would you like to see? (can select more than 1)",["Colleges by State","Colleges by Town"])
        for i,x in enumerate(sm):
            if x=="Colleges by State":
                filter_by_state(mm,i)
        for i,x in enumerate(sm):
            if x=="Colleges by Town":
                filter_by_town(mm,i)


main()

