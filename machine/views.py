from django.db import connection
from .models import data
from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from xgboost.sklearn import XGBRegressor
from pract.models import products

def forecast1():
    def scale_data1(train_set):
        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaler = scaler.fit(train_set)
        train_set = train_set.reshape(train_set.shape[0], train_set.shape[1])
        train_set_scaled = scaler.transform(train_set)
        return train_set_scaled, scaler

    def scale_data2(scaler,test_set):
        test_set = test_set.reshape(test_set.shape[0], test_set.shape[1])
        test_set_scaled = scaler.transform(test_set)
        return test_set_scaled


    def get_diff(data):
        data['sales_diff'] = data.sales.diff()
        data = data.dropna()
        return data

    def generate_supervised(data):
        supervised_df = data.copy()
        for i in range(1,13):
            col_name = 'lag_' + str(i)
            supervised_df[col_name] = supervised_df['sales_diff'].shift(i)
        supervised_df = supervised_df.dropna().reset_index(drop=True)
        return supervised_df

    def prediction(mod,df20):
        df20=df20.drop("index",axis=1)
        y=df20["sales"].values
        df3=df20.drop("sales",axis=1)
        store_dummies=pd.get_dummies(df3["product"])
        merge_df=pd.concat([df3,store_dummies],axis="columns")
        merge_df=merge_df.drop(["product",3],axis=1)
        merge_df=merge_df.values
        X_test=scale_data2(scale,merge_df)
        z=mod.predict(X_test)
        z+=y
        return z




    query=str(data.objects.all().query)
    df=pd.read_sql_query(query,connection)
    df.drop('id',axis=1,inplace=True)
    sales_data = df
    monthly_data = sales_data.copy()
    monthly_data.date = monthly_data.date.apply(lambda x: str(x)[3:])
    group_data=monthly_data.groupby(['product','date'])['sales'].sum().reset_index()
    group_data.date = pd.to_datetime(group_data.date)
    group1_data=group_data.groupby('product')
    l=[]
    l1=[]
    for key,item in group1_data:
        a_group=group1_data.get_group(key)
        a_group = a_group.sort_values(by="date")
        stationary_df =get_diff(a_group)
        model_df = generate_supervised(stationary_df)
        df1=model_df[-2:-1]
        model_df=model_df[:-2]
        x=df1.drop(["date","lag_12"],axis=1)
        l1.append(x)
        l.append(model_df)
    df=pd.concat(l).reset_index()
    df20=pd.concat(l1).reset_index()
    df.drop('index',axis=1)
    store_dummies=pd.get_dummies(df['product'])
    merged_df=pd.concat([df,store_dummies],axis='columns')
    final=merged_df.drop(['index','product',3],axis=1)
    train1=final.drop(['date','sales'],axis=1)
    train=train1.values
    X_train, y_train = train[:, 1:], train[:, 0:1].ravel()
    X_train,scale=scale_data1(X_train)
    mod = XGBRegressor( n_estimators=100,learning_rate=0.2,objective='reg:squarederror')
    mod.fit(X_train, y_train)
    s1=prediction(mod,df20)
    query1=str(products.objects.all().order_by('unique').query)
    daf=pd.read_sql_query(query1,connection)
    daf1=daf.drop(["qty","buy_price","sell_price"],axis=1)
    daf1=daf1.values
    x=dict()
    for i in range(len(daf1)):
        s=daf1[i][1]
        x[daf1[i][0]]=int(s1[s-1])
    return x





def forecast(request):
    x=forecast1()
    context={
        'forecast1':x
    }
    return render(request,'forecast.html',context)
