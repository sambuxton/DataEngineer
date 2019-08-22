import pandas as pd
from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot as plt
from pandas.plotting import autocorrelation_plot
import pandas as pd
from pandas import DataFrame
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import math


#Change this part if the document has a different date format 
def parser(x):
    return datetime.strptime(x, '%b-%Y')


from pyspark.sql.functions import to_date
test = spark.read.option("inferSchema", "true").csv(file_location, header='true')
test = test.select('OpenedYM2', "TicketCount")
pd_test = test.toPandas()


index = pd.to_datetime(pd_test['OpenedYM2'])

pd_test.drop(['OpenedYM2'], axis=1, inplace=True)
dataframe = pd.DataFrame(index = index, data = pd_test.squeeze().values)



X = dataframe.values


size = int(len(X) * 0.25)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]
predictions = list()
print(len(test))
print(history)

#Compares and saves the predicted point and actual point
for t in range(len(test)):
    model = ARIMA(history, order=(1,1,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat)
    obs = test[t]
    history.append(obs)
    print('predicted=%f, expected=%f' % (yhat, obs))
error = math.sqrt(mean_squared_error(test, predictions))
print('Test MSE: %.3f' % error)


#Formats the display
plt.title('ARIMA Prediction vs. Actual')
plt.xlabel('Months')
plt.ylabel('Total Hours')

plt.gca().legend(('Actual','Predicted'))


plt.plot(test, color = 'blue')
plt.plot(predictions, color='red')
display()



