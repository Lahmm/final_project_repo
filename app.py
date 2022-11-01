import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import AdaBoostClassifier
plt.style.use('seaborn')

st.title('Online Education Data Analyses and Forecase')
st.markdown('_by YHB & LN_')
df = pd.read_csv('STATISTICAL_INFORMATION.csv')

st.header('1.Data Display:')
st.subheader('1.1.User Information:')

option = st.selectbox(
    'Which information you want to check?',
    ('age', 'gender', 'education degree'))

if option == 'age':
    age_img = Image.open('age.png')
    st.image(age_img, caption='Stackplot of user\'s age')
elif option == 'gender':
    gender_img = Image.open('gender.png')
    st.image(gender_img, caption='Pie-Char of urser\'s gender')
else:
    edu_img = Image.open('education.png')
    st.image(edu_img, caption='Histogram of ueser\'s education degree')

st.subheader('1.2.Learning Style (Event):')
events_img = Image.open('events.png')
st.image(events_img, caption='Distribution Pie Char of Events')
st.markdown('**Event**: Indicates the type of events performed by users.')
st.markdown('**problem**: do homework')
st.markdown('**video**: watch a video')
st.markdown('**access**: read objects other than the video and assignment in the course')
st.markdown('**wiki**: read the Wikipedia of the course')
st.markdown('**discussion**: discussion')
st.markdown('**navigate**: browse the rest of the course')
st.markdown('**page close**: shut down web pages of MOOC')
 
    
st.subheader('1.3.Study Time:')
time_img = Image.open('learn_count.png')
st.image(time_img)
st.markdown(' Students\' study time is mainly concentrated in **June** to **July** and **December** to **January**, while a relatively small number of students study from **August** to **October**.')

st.header('2.Event Data Analyses:')
option = st.selectbox(
    'Which event do you want to view information about?',
    ('Problem', 'Video', 'Access', 'Wiki', 'Discussion', 'Navigate', 'Page_Close'))

st.write('The following is detail about event ', option)

option = option.upper()
if option == 'ACCESS':
    option = 'ACCESS1'

fig, ax = plt.subplots(figsize=(20, 5))
df[option].plot()
st.pyplot(fig)

# Model test
df = pd.read_csv('STATISTICAL_INFORMATION.csv')
df["LABLE"]=df["LABLE"].astype("int")
cols=df.columns.tolist()
del cols[0]
del cols[-1]
for col in cols:
    df.loc[df[col]>df[col].mean()+3*df[col].std(),col] = df[col].mean()
martix=np.array(df.values)
scaler=StandardScaler(); #去均值和方差归一化
X=scaler.fit_transform(martix[:,1:-1])
Y=martix[:,-1]
Y=Y.astype(int)

# 计算均值方差
mean = np.mean(martix, axis=0)
std = np.std(martix, axis=0)
mean = np.delete(mean, 0)
mean = np.delete(mean, -1)
std = np.delete(std,0)
std = np.delete(std,-1)

x_train,x_test,y_train,y_test=train_test_split(X,Y);  #样本占比0.3 ,test_size=0.3
model = DecisionTreeClassifier(criterion="entropy") #熵
model.fit(x_train,y_train); #训练


# y_pre=model.predict(x_test);    #测试 返回正确分类的比例
# precision=metrics.precision_score(y_pred=y_pre,y_true=y_test,average="binary");
# recal=metrics.recall_score(y_pred=y_pre,y_true=y_test,average="binary");

base_model = DecisionTreeClassifier(criterion="entropy",max_depth=10)
model=AdaBoostClassifier(base_estimator=base_model,n_estimators=50,learning_rate=0.5)
model.fit(x_train,y_train)


st.header('3.Forecast:')

col1, col2, col3 = st.columns(3)
with col1:
    problem = st.slider('Input the number of the problem you worked:', 0.0, 113.0, 0.0)
    #st.write('Your problem number is :'+ round(int(problem)))
    video = st.slider('Input the number of the video you watched:', 0.0, 50.0, 0.0)
    #st.write('Your video number is :'+ round(video))
    access = st.slider('Input the number of time you access in MOOC:', 0.0, 189.0, 0.0)
    #st.write('Your access number is :'+ round(access))
with col2:
    wiki = st.slider('Input the number of times you\'ve looked up Wikipedia:', 0.0, 12.0, 0.0)
    #st.write('Your wiki number is :'+ round(wiki))
    discussion = st.slider('Input the number of time you discussed:', 0.0, 119.0, 0.0)
    #st.write('Your discussion number is :'+ round(discussion))
with col3:
    navigate = st.slider('Input the number of time you browse the rest of the course:', 0.0, 47.0, 0.0)
    #st.write('Your navigate number is :'+ round(navigate))
    page_close = st.slider('Input the number of time you shut down web pages of MOOC:', 0.0, 72.0, 0.0)
    #st.write('Your page-close number is :'+ round(page_close))


test = np.array([round(problem), round(video), round(access), round(wiki), round(discussion), round(navigate), round(page_close)])




if st.button('Submit'):
    test = (test - mean)/ std
    test = test.reshape(1, -1)
    result = int(model.predict(test)[0])

    if result == 0:
        st.write('You will continue')
        st.balloons()
    else:
        st.write('You will drop')
        st.snow()
