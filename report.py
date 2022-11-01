import streamlit as st

st.title('Online Education Data Analysis and Forecast')

st.header('1. Abstract')
st.markdown('Due to the advent of the epidemic, online education has developed rapidly and gradually become one of the main teaching methods. kddcup2015 competition data set is from Tsinghua Xuetang online course platform, which records the learning data of about 120,000 students and about 8 million learning logs in detail. This paper uses **data visualization** to observe user characteristics and analyze the main characteristics of students skipping classes; The **decision tree** and **Adaboost promotion method** were used to predict whether students skipped class or not, and the contribution of each attribute was observed. Finally, according to the qualitative and quantitative analysis to determine the characteristics of skipping class group.')
st.markdown('**Keywords: data visualization, decision tree, Adaboost lifting method, skipping class**')


st.header('2. Introduction to the Dataset')
st.subheader('2.1. Overview of the dataset')
st.write('This dataset was obtained from the 2015 kddcup Data Mining competition. The experimental dataset size is a total of 10 files, respectively user_info.csv, log_train.csv, log_test.csv, course_info.csv, data.csv, object.csv, enrollment_test.csv, enrollment_train.csv, truth_test.csv, truth_train.csv. ')
st.subheader('2.2. Relationship of the dataset')
st.image('图片1.png')

st.header('3. Experience Target')
st.markdown('**1**. Make statistics on the distribution of overall user characteristics, such as age and education background distribution, to obtain the overall user characteristics of the platform.')
st.markdown('**2**. By processing the original data, the difference between skipping class and not skipping class is obtained, and it is visualized. To show the relationship between skipping class and learning behavior in an intuitive way. So that we can conveniently observe the characteristics of students skipping class from the data statistics chart.')
st.markdown('**3**. A classifier can be trained to predict whether students skip class or not, and observe whether the contribution of each feature in the classifier is related to the statistical graph.')

st.header('4. Distribution of User Features')
st.markdown('This task is mainly done using **MySQL database**. After importing user_info.csv into the database, write query statements to obtain statistics and visualize them in python.')
st.subheader('4.1. Age')
st.markdown('Query **sql** code: Because there are outliers and unreasonable values in the data (for example, some people were born after 2015, but the data was collected in 2015), records with age less than 0 and data larger than 3 times the standard deviation of the mean will be filtered out in the statistics.')
code = '''
select 2015-BIRTH age,count(BIRTH) count  
from USER_INFO
where 2015-BIRTH>0 and 2015-BIRTH<(select avg(2015-BIRTH)+3*stddev(2015-BIRTH) from USER_INFO where 2015-BIRTH>0)
group by (BIRTH)
order by age
'''
st.code(code, language='sql')
st.image('age2.png')
st.markdown('**Analysis**: According to Figure 4.1, it can be found that the user age is concentrated between 18 and 25 years old. It can be guessed that the main users of online education are undergraduate students and postgraduate students, mainly to complete the teaching tasks assigned by teachers.')
st.subheader('4.2. Gender and Skipping Labels')
code = '''
select GENDER,count(GENDER) from USER_INFO group by GENDER;
select LABEL,count(LABEL) count from TRUTH_TRAIN group by LABEL;
'''
st.code(code,language='sql')
st.image('gender.png', caption='png-4.2：Pie-Char of urser gender')
st.markdown('**Analysis**: The male student is slightly more than the female student, guess the reason that the male student is more than the female student overall. However, the proportion of skipping classes is far greater than that of sticking to study, which indicates that college students are more playful, and also represents that the data set is a seriously unbalanced data set.')
st.subheader('4.3. Education Background')
code = '''
select EDUCATION,count(EDUCATION) count from USER_INFO where EDUCATION is not null group by EDUCATION
'''
st.code(code, language='sql')
st.image('degree.png')
st.markdown('**Analysis**: Undergraduates account for the vast majority, which is also in line with the characteristics of more courses and heavy teaching tasks for undergraduates')
st.subheader('4.4. Learning Style')
code = '''
select EVENT,count(EVENT) count from LOG_TRAIN group by EVENT
'''
st.code(code, language='sql')
st.image('action.png')
st.markdown('**Analysis**: access events account for the largest proportion, while students mainly watch videos and do homework on online platforms, which reflects that students\' learning attitude is not too serious, and they do not fully and effectively use online classes. At the same time, the number of people who browse chapters and do homework is almost the same. This article speculates that homework can only be entered by browsing chapters.')
st.subheader('4.5. Learning Time')
st.image('time.png')
st.markdown('**Analysis**: It can be seen from the chart that students\' study time is mainly concentrated in June to July and December to January, while a relatively small number of students study from August to October, and it also shows that students\' study time is usually the final examination period. It can be seen that most students study less in ordinary times, but study more seriously in the final.')


st.header('5. Statistical Modeling of Skipping Classes')
st.write('In the data set, there are only 120,542 students with labeled individuals. Therefore, true_test.csv will be used for feature extraction in the following modeling. The only file that can extract features for students is log_train.csv. This file records every learning event of all students. It is a log file. This file will be modeled in subsequent modeling efforts. The main tool used is the **MySQL database**. ')
st.markdown('At present, the action data of each student can be extracted from **log_train.csv** as follows: **problem**: doing homework, **video**: watching video, **access**: reading other objects except video and homework of the course, **wiki**: reading Wikipedia of the course, **discussion**: Forum discussions, **navigate**: navigate the rest of the course, **page_close**: close the page. Therefore, it is necessary to **sort out** the learning situation of each student from the log file.')

st.header('5.1 Preprocessing')
st.subheader('5.1.1. Grouping Statistics')
st.markdown('Separate statistics were made for each action to sort out The Times of each student\'s corresponding actions and separate tables were built. For the 7 events contained in the log file, there were 7 tables for **one-to-one correspondence**. The specific statistical method takes statistical problem as an example, where the sql code is as follows:')
code = '''
create table problems(enrollment_id,problem) as select enrollment_id,count(event) problem from log_train
where event='problem' group by(enrollment_id)
'''
st.code(code, language='sql')
st.markdown('The table has two fields: **enrollment_id** corresponds to the student registration number, and **problem** the number of enrollments that the event triggered')
col1, col2, col3 = st.columns(3)
with col2:
    st.image('preview.jpg')
st.write('Others are the same.')
st.subheader('5.1.2. Data Integration')
st.write('Using true_train.csv as the standard, left-join with other 7 tables and create a new table, sql code:')
code = '''
create table statistical_information as
select TRUTH_TRAIN.ENROLLMENT_ID ENROLLMENT_ID,PROBLEM,VIDEO,ACCESS1,WIKI,DISCUSSION,PAGE_CLOSE,NAVIGATE,LABLE
from ((((((TRUTH_TRAIN left join PROBLEMS on TRUTH_TRAIN.ENROLLMENT_ID=PROBLEMS.ENROLLMENT_ID) 
left join VIDEOS on TRUTH_TRAIN.ENROLLMENT_ID=VIDEOS.ENROLLMENT_ID) 
left join ACCESSS on TRUTH_TRAIN.ENROLLMENT_ID=ACCESSS.ENROLLMENT_ID) 
left join WIKIS on TRUTH_TRAIN.ENROLLMENT_ID=WIKIS.ENROLLMENT_ID) 
left join DISCUSSIONS on TRUTH_TRAIN.ENROLLMENT_ID=DISCUSSIONS.ENROLLMENT_ID) 
left join NAVIGATES on TRUTH_TRAIN.ENROLLMENT_ID=NAVIGATES.ENROLLMENT_ID) 
left join PAGE_CLOSES on TRUTH_TRAIN.ENROLLMENT_ID=PAGE_CLOSES.ENROLLMENT_ID;
'''
st.code(code, language='sql')
st.header('5.2. Data cleaning')
st.markdown('After the integration was complete, a lot of missing data was found. This paper speculated that some students may have never triggered an event from the beginning to the end, resulting in no learning record of this item in the log. So fill it with 0. Some abnormal data were also found in the preliminary statistics (for example, the number of times some accounts completed homework was as high as 800 times, while the course lasted only one year). Therefore, in this paper, according to the principle of **3sigma;**, data less than (mean -3* standard deviation) or more than (mean +3* standard deviation) were regarded as abnormal data and modified to mean value.')
code = '''
con = create_engine('mysql+pymysql://root:@127.0.0.1:3306/LiuNian');
sql="select * from STATISTICAL_INFORMATION";
df=pd.read_sql(sql,con);
df["lable"]=df["lable"].astype("int")
cols=df.columns.tolist()
del cols[0];
del cols[-1];
for col in cols:
    df.loc[df[col]>df[col].mean()+3*df[col].std(),col]=df[col].mean();
'''
st.code(code, language='sql')
st.image('preview_2.jpg')
st.header('5.3. Visual Analysis of Skipping Class or Not')
st.markdown('In order to better compare the difference of student groups between skipping class and not skipping class, this paper makes a **comparative analysis** of the data visualization. Because of the huge difference between skipping class and not skipping class, **the dimensional effect should be eliminated**. In this paper, the number of people corresponding to The Times of each time is divided by the total number of people corresponding to the missing class label, which is converted into the frequency of events, and the probability distribution diagram of seven events in the case of skipping class and not skipping class is drawn. The sql code takes problem as an example:')
code = '''
select PROBLEM,count(PROBLEM) count from statistical_information group by PROBLEM
'''
st.code(code, language='sql')
col1, col2 = st.columns(2)
with col1:
    st.image('5.1.png')
    st.image('5.3.png')
    st.image('5.5.png')
    st.image('5.7.png')
with col2:
    st.image('5.2.png')
    st.image('5.4.png')
    st.image('5.6.png')
st.markdown('**Analysis**: From the above figure, it can be seen that there is a big difference between Figures 5.1, 5.2, 5.3 and 5.6. The two curves in Figure 5.4 and 5.5 are similar. **But all of the graphs had one common feature: the distribution of frequency of skipping classes was more clustered in places with lower study times than the distribution of persistence, meaning that students who skipped classes learned less about events**. This provides a strong support for our subsequent classifier modeling.')
st.header('5.4. Constructing a Classifier')
st.markdown('The data mining part of this paper is completed based on **sklearn**.')
st.subheader('5.4.1. The Base Classifier')
st.markdown('Taking these 7 fields as the characteristics of students, this paper chooses **decision tree** as the basic classifier. Due to the sufficient data volume, there are about 120,000 samples. However, it can be seen from Figure 4.2 that there is a serious class **imbalance** problem in the data set, that is, the sample that skips class is about three times that of the sample that insists on learning. Therefore, the training set should be **resampled** to ensure class balance. This experiment adopts the **set-aside method**, and the test set is 30 percent of the overall data set. Due to the serious imbalance of the class, the evaluation indexes of the experimental results include **accuracy**, **F1 score** and **G-mean** for comprehensive evaluation. The experimental results are as follows:')
code = '''
DecisionTree:  
accuracy: 0.8043303929430633 
F1 score: 0.8778820930553637 
G-Mean score: 0.8258453296011508
'''
st.code(code, language='sql')
st.markdown('**Contribution**:')
st.image('contribution.jpg')
st.markdown('**Corresponding fields**:')
st.image('field.jpg')
st.markdown('Therefore, the contribution of access, page_close and navigate is high, while the contribution of wiki and discussion is low. From the visual images in 5.3, attributes with high contribution degree of access, page_close and navigate have greater curve differences, while those with low contribution degree of wiki and discussion have higher curve coincidence degree. **The more differentiated the curve, the more information it provides to the decision tree**.')
st.subheader('5.4.2. Promotion')
st.markdown('In order to further improve the performance of the classifier, this paper will use the **lifting method** to obtain better training results. Historically Kearns and Valiant were the first to propose the concepts of "strongly learnable" and "weakly learnable". And in Schapire\'s later proof it turns out that these two things are equivalent. **Therefore, we can use a linear combination of multiple basic classifiers to obtain a strong classifier**. Finding a basic classifier is not difficult. In this paper, the basic classifier is **decision tree**, and the lifting algorithm is the relatively common **Adaboost algorithm**. The evaluation indexes are still **accuracy**, **F1 score** and **G-mean**.')
code = '''
AdaboostDecisionTree: 
accuracy: 0.8424356386361751 
F1 score: 0.9037174721189591 
G-Mean score: 0.8735636035471351
'''
st.code(code, language='sql')
st.header('6. Summary')
st.markdown('**According to the visual analysis of the data and the contribution of each attribute of the machine learning model**, the students who skipped class completed the events less than those who insisted on learning, and many students who skipped class only triggered one or two events. From this point of view, there is still much room for improvement in online teaching.')

