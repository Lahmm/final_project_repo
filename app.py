import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split;
from sklearn import metrics;
from sklearn.tree import DecisionTreeClassifier;
from sklearn.preprocessing import StandardScaler;

df = pd.read_csv('STATISTICAL_INFORMATION.csv')
plt.style.use('seaborn-bright')

st.title('Online education data analysis and forecast')
st.subheader('By Haobo Yang and Nian Liu')

#filters 
#filter 1 by description
problem_filter = st.sidebar.slider('Problems',0,500,0)
video_filter = st.sidebar.slider('Video',0,500,0)
access_filter = st.sidebar.slider('Access',0,500,0)
wiki_filter = st.sidebar.slider('Wiki',0,500,0)
page_close_filter = st.sidebar.slider('Page close',0,500,0)
discuss_filter = st.sidebar.slider('Discussion',0,500,0)
navigate_filter = st.sidebar.slider('Navigate',0,500,0)

# Pie chart
df_1 = df[df['PROBLEM'] >= problem_filter]
df_2= df_1[df_1['VIDEO'] >= video_filter]
df_3 = df_2[df_2['ACCESS1'] >= access_filter]
df_4 = df_3[df_3['WIKI'] >= wiki_filter]
df_5 = df_4[df_4['PAGE_CLOSE'] >= page_close_filter]
df_6 = df_5[df_5['DISCUSSION'] >= discuss_filter]
df_7 = df_6[df_6['NAVIGATE'] >= navigate_filter]
fig, ax = plt.subplots(figsize=(5,5))
cnt = [df_7['LABLE'].value_counts()[0], df_7['LABLE'].value_counts()[1]]
ax.pie(cnt, labels=['Continue', 'Drop'])
st.pyplot(fig)

#input box
pro = st.sidebar.number_input('pro')
acc = st.sidebar.number_input('acc')
vie = st.sidebar.number_input('vie')
dis = st.sidebar.number_input('dis')
wik = st.sidebar.number_input('wik')
page = st.sidebar.number_input('page')
nav = st.sidebar.number_input('nav')

# Model test
df = pd.read_csv('STATISTICAL_INFORMATION.csv')
df["LABLE"]=df["LABLE"].astype("int")
cols=df.columns.tolist()
del cols[0];
del cols[-1];
for col in cols:
    df.loc[df[col]>df[col].mean()+3*df[col].std(),col] = df[col].mean();
martix=np.array(df.values);
scaler=StandardScaler(); #去均值和方差归一化
X=scaler.fit_transform(martix[:,1:-1]);
Y=martix[:,-1];
Y=Y.astype(int)

mean = np.mean(martix, axis=0)
std = np.std(martix, axis=0)
mean = np.delete(mean, 0)
mean = np.delete(mean, -1)
std = np.delete(std,0)
std = np.delete(std,-1)


x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.3);  #样本占比0.3
model = DecisionTreeClassifier(criterion="entropy") #熵
model.fit(x_train,y_train); #训练


y_pre=model.predict(x_test);    #测试 返回正确分类的比例
precision=metrics.precision_score(y_pred=y_pre,y_true=y_test,average="binary");
recal=metrics.recall_score(y_pred=y_pre,y_true=y_test,average="binary");


if st.button('Submit'):
    test = np.array([pro,acc,vie,dis,wik,page,nav])
    test = (test - mean)/ std
    test = test.reshape(1, -1)
    result = int(model.predict(test)[0])

    if result == 0:
        st.write('You will continue')
        st.balloons()
    else:
        st.write('You will drop')
        st.snow()



