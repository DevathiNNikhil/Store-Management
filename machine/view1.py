from django.db import connection
from .models import data
from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from xgboost.sklearn import XGBRegressor
def scale_data1(train_set):
    #apply Min Max Scaler
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaler = scaler.fit(train_set)
    
    # reshape training set
    train_set = train_set.reshape(train_set.shape[0], train_set.shape[1])
    train_set_scaled = scaler.transform(train_set)
        
    X_train, y_train = train_set_scaled[:, 1:], train_set_scaled[:, 0:1].ravel()
    
    return X_train, y_train, scaler

def scale_data2(scaler,test_set):
    
    test_set = test_set.reshape(test_set.shape[0], test_set.shape[1])
    test_set_scaled = scaler.transform(test_set)
    return test_set_scaled

def undo_scaling(y_pred, x_test, scaler_obj, lstm=False):  
    #reshape y_pred
    y_pred = y_pred.reshape(y_pred.shape[0], 1, 1)
    
    if not lstm:
        x_test = x_test.reshape(x_test.shape[0], 1, x_test.shape[1])
    
    #rebuild test set for inverse transform
    pred_test_set = []
    for index in range(0,len(y_pred)):
        pred_test_set.append(np.concatenate([y_pred[index],x_test[index]],axis=1))
        
    #reshape pred_test_set
    pred_test_set = np.array(pred_test_set)
    pred_test_set = pred_test_set.reshape(pred_test_set.shape[0], pred_test_set.shape[2])
    
    #inverse transform
    pred_test_set_inverted = scaler_obj.inverse_transform(pred_test_set)
    
    return pred_test_set_inverted

def load_data():  
    return pd.read_csv('E:\downloads\demand-forecasting-kernels-only\\train.csv')  

def get_diff(data):
    data['sales_diff'] = data.sales.diff()
    data = data.dropna()
    return data

def generate_supervised(data):
    supervised_df = data.copy()
    
    #create column for each lag
    for i in range(1,13):
        col_name = 'lag_' + str(i)
        supervised_df[col_name] = supervised_df['sales_diff'].shift(i)
    
    #drop null values
    supervised_df = supervised_df.dropna().reset_index(drop=True)
    
#     supervised_df.to_csv('../data/model_df.csv', index=False)
    
    return supervised_df

query=str(data.objects.all().query)
df=pd.read_sql_query(query,connection)
df.drop('id',axis=1,inplace=True)
sales_data = df
monthly_data = sales_data.copy()
monthly_data.date = monthly_data.date.apply(lambda x: str(x)[3:])


# monthly_data=monthly_data[monthly_data['product']<=3]

group_data=monthly_data.groupby(['product','date'])['sales'].sum().reset_index()
group_data.date = pd.to_datetime(group_data.date)

group1_data=group_data.groupby('product')


l=[]

for key,item in group1_data:
    a_group=group1_data.get_group(key)
    stationary_df =get_diff(a_group)
    model_df = generate_supervised(stationary_df)
    l.append(model_df)
df=pd.concat(l).reset_index()


df.drop('index',axis=1)

store_dummies=pd.get_dummies(df['product'])

merged_df=pd.concat([df,store_dummies],axis='columns')

final=merged_df.drop(['index','product',3],axis=1)


train1=final.drop(['date','sales'],axis=1)
train=train1.values

X_train,y_train,scale=scale_data1(train)
mod = XGBRegressor( n_estimators=100,learning_rate=0.2,objective='reg:squarederror')
mod.fit(X_train, y_train)
test=train1[-1:]
print(train1)
# # test.drop('sales_diff',axis=1,inplace=True)
# test=test.values
# print(test)
# X_test=scale_data2(scale,test)

# predictions = mod.predict(X_test)
# original_df = group_data
# unscaled = undo_scaling(predictions, X_test, scale)
# unscaled_df = unscaled[0][0]+1315
# print(unscaled_df)
def forecast():
    pass


