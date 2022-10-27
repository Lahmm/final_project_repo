import numpy as np;
def overSampling(x,y):
    label=np.unique(y);
    maxCount=0;#类中最多的样本数
    maxK=0;#类中最多的样本对应的类标
    for k in label:
        count=len(np.where(y==k)[0]);
        if(count>maxCount):
            maxCount=count;
            maxK=k;
    yMaxIndex=np.where(y==maxK)[0];
    x1=x[yMaxIndex,:];
    y1=y[yMaxIndex];
    for i in range(len(label)):
        if label[i]==maxK: continue;
        index=np.where(y==label[i])[0];#第i类的索引
        overIndex=np.random.choice(index,maxCount);
        x1=np.concatenate((x1,x[overIndex,:]),axis=0);
        y1=np.append(y1,y[overIndex]);
    return x1,y1;

def getClassWeight(y):
    label = np.unique(y);
    classWeight={};
    for k in label:
        count=len(np.where(y==k)[0]);
        classWeight[k]=(1/count)*(len(y)/len(label));
    return classWeight;



