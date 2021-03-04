import seaborn as sns #visualisation
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler


sns.set(color_codes=True)

test = pd.read_csv("test.csv")
x_val = pd.read_csv("input.csv")
label = pd.read_csv("label.csv")
graph_l = list()
for x_name,val in x_val.iteritems():
    for name, values in label.iteritems():
        plot = plt.figure()
        plt.scatter(x_val[x_name],label[name])
        plt.xlabel(x_name) 
        plt.ylabel(name) 
        z = np.polyfit(x_val[x_name],label[name], 1)
        p = np.poly1d(z)
        plt.plot(x_val[x_name],p(x_val[x_name]),"r--")
        plt.title(f'{x_name} vs {name}:{x_val[x_name].corr(label[name])}') 
        if(x_val[x_name].corr(label[name]) > 0.1):
            graph_l.append((f'{x_name} vs {name}:{x_val[x_name].corr(label[name])}'))
        plot.savefig(f'Plots_xvy/{x_name} vs {name}.png')
        plt.close()
graph_l.sort()
print(graph_l)

regr = RandomForestRegressor(max_depth=5,random_state=1)
x_train, x_test, y_train, y_test = train_test_split (x_val, label, test_size = 0.2, random_state = 2)

regr.fit(x_train, y_train)
y_pred = regr.predict(x_test)
d_ypred = pd.DataFrame(y_pred)
d_ypred.columns = label.columns
y_test.columns = d_ypred.columns
for x_name,val in x_test.iteritems():
    for name, values in d_ypred.iteritems():
        plot = plt.figure()
        plt.scatter(x_test[x_name],d_ypred[name],color='red',label='Predicted')
        plt.scatter(x_test[x_name],y_test[name],color='blue',label='Actual')
        plt.xlabel(x_name) 
        plt.ylabel(name) 
        plt.legend()
        plt.title(f'{x_name} vs {name}') 
        plot.savefig(f'PredvActual/{x_name} vs {name}.png')
        plt.close()
metrics = mean_absolute_error (y_test, y_pred)
print(regr.feature_importances_)
print(metrics)