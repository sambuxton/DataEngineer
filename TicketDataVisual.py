import chart_studio
chart_studio.tools.set_credentials_file(username='samuelbuxton', api_key='-------')
storage_account_name = "------"
storage_account_access_key = "-------"

file_type = "csv"

spark.conf.set(
  "fs.azure.account.key."+storage_account_name+".blob.core.windows.net",
  storage_account_access_key)

file_location = "wasbs://sm-ticketdata@datastoreinvestigation.blob.core.windows.net/SM Jan2018-Jun19.csv"
file_location2 = "wasbs://sm-ticketdata@datastoreinvestigation.blob.core.windows.net/SupplyChain_CLEAN.csv"
file_location3 = "wasbs://sm-ticketdata@datastoreinvestigation.blob.core.windows.net/Last 6 months alerts-SCOM.csv"


#Operating on the tables to pick columns
import pyspark
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark import sql
import pyspark.sql.functions as sf
from pyspark.sql.functions import to_date
import datetime
from pyspark.sql.functions import year, month, dayofmonth
from pyspark.sql.functions import *


SCOM = spark.read.option("inferSchema", "true").option("datetimeFormat", "MM/dd/yy h:mm a").csv(file_location3, header='true')
SC = spark.read.option("inferSchema", "true").csv(file_location2, header='true')
SMData = spark.read.option("inferSchema", "true").option("timestampFormat", "MMM-yy").csv(file_location, header='true')


#Formatting column values
split_col = pyspark.sql.functions.split(SMData['Severity'], '-')
SM = SMData.withColumn('SevNum', split_col.getItem(0))
SM = SM.withColumn('SevString', split_col.getItem(1))

split_col = pyspark.sql.functions.split(SMData['OpenedYM'], ',')
SM = SM.withColumn('MonthOpened', split_col.getItem(0))
SM = SM.withColumn('YearOpened', split_col.getItem(1))

SM = SM.withColumn("SevNum", trim(SM.SevNum))

#heatmap for total hours to resolution per category and Severity
HeatMap = SM.select("HoursToResolutionExclusion", "category", "SevNum").groupBy(SM.category, SM.SevNum).agg(sf.sum('HoursToResolutionExclusion').alias('TotalHours')).withColumnRenamed("category", "Categories")

TopCat = SM.select("category", "HoursToResolutionExclusion").groupBy(SM.category).agg(sf.sum('HoursToResolutionExclusion').alias('Hours'))
TopCat = TopCat.orderBy(TopCat.Hours.desc()).limit(10)

HeatMap = TopCat.join(HeatMap, HeatMap.Categories == TopCat.category, "left_outer")
HeatMap = HeatMap.select("Categories", "SevNum", "TotalHours").orderBy("Categories")

#used to flatten list of lists
def flattenList(column, ftn):
  list = []
  for sublist in column:
    for item in sublist:
      if (ftn == 'log'):
        list.append(log(item+1))
      else:
        list.append(item)
  return list

# We wanted to show the stakeholder exactly where effort was being spent on tickets so that they could target their time saving efforts in those specific areas
# This graph answers the question: What severity level and category takes the majority of the effort?
# Use case: I can see using this graph that a great ammount of effort is going towards Email Error tickets with severity level 3. I will implement a protocol
# to streamline the process and conserve hours of work.
# HeatMapRef

# Only discrete values on the y-axis

import chart_studio
import chart_studio.plotly as py 
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px

from math import log


y0 = HeatMap.limit(2000).select('TotalHours').collect()
y = flattenList(y0, 'log')

x0 =  HeatMap.limit(2000).select('SevNum').collect()
x = flattenList(x0, 0)
        
z0 =  HeatMap.limit(2000).select('Categories').collect()
z = flattenList(z0, 0)

data = {'TotalTickets':y , 'SevNum': x, 'category': z}
dataPD = pd.DataFrame(data)

fig = go.Figure(data=go.Heatmap(
                   z=y,
                   y=x,
                   x=z)
               
               
    )

fig.update_yaxes(nticks=5, title = "Severity")



py.plot(fig, output_type = "div")

#heatmap for total number of tickets per category and Severity
MapCount = SM.select("number", "cmdb_ci", "SevNum").groupBy(SM.cmdb_ci, SM.SevNum).agg(sf.count('number').alias('TotalTickets')).withColumnRenamed("cmdb_ci", "Categories")
MapCount = MapCount.orderBy(MapCount.TotalTickets.desc())

TopCat2 = SM.select("cmdb_ci", "number").groupBy(SM.cmdb_ci).agg(sf.count('number').alias('Tot'))
TopCat2 = TopCat2.orderBy(TopCat2.Tot.desc()).limit(10)

MapCount = TopCat2.join(MapCount, MapCount.Categories == TopCat.cmdb_ci, "left_outer")
MapCount = MapCount.select("Categories", "SevNum", "TotalTickets").orderBy("Categories")

#Graphing a heatmap for total hours per category with severity
y0 = MapCount.limit(2000).select('TotalTickets').collect()
y = flattenList(y0, 'log')

x0 =  MapCount.limit(2000).select('SevNum').collect()
x = flattenList(x0, 0)
        
z0 =  MapCount.limit(2000).select('Categories').collect()
z = flattenList(z0, 0)

data = {'TotalTickets':y , 'SevNum': x, 'cmdb_ci': z}
dataPD = pd.DataFrame(data)

fig = go.Figure(data=go.Heatmap(
                   z=y,
                   y=x,
                   x=z))

fig.update_yaxes(nticks=5, title = "Severity")
fig.update_layout(title = "Hours of Effort vs. Severity")

#3D table showing Severity vs Quantity vs Total Hours
tbl_3D = SM.select("number", "cmdb_ci", "HoursToResolutionRaw", "SevNum").groupBy(SM.cmdb_ci, SM.SevNum).agg(sf.sum('HoursToResolutionRaw').alias('TotalHours')).withColumnRenamed("cmdb_ci", "Categories").withColumnRenamed("SevNum", "Severity")

TotTick = SM.select("number", "cmdb_ci", "SevNum").groupBy(SM.cmdb_ci, SM.SevNum).agg(sf.count('number').alias('TotalTickets'))
TotTick.createOrReplaceTempView("tblTOTAL")

tbl_3D = tbl_3D.join(TotTick, (tbl_3D.Categories == TotTick.cmdb_ci) & (tbl_3D.Severity == TotTick.SevNum), "inner")
tbl_3D = tbl_3D.select("Categories", "Severity", "TotalHours", "TotalTickets")


# In this graph we wanted to create a centralized tool to draw correlations among three key areas: Severity, Total Hours, and 
# Total tickets submitted. 
# Use Case: I want to see which category has a greater average resolution time so I map total hours vs. total tickets against each
# other to see that a particular category is not on the regression line
# 3DGraphRef

chart_studio.tools.set_credentials_file(username='samuelbuxton', api_key='--------')

y0 = tbl_3D.limit(1000).select('TotalTickets').collect()
y = flattenList(y0, 'log')

x0 =  tbl_3D.limit(1000).select('Severity').collect()
x = flattenList(x0, 0)
        
z0 =  tbl_3D.limit(1000).select('Categories').collect()
z = flattenList(z0, 0)    

w0 =  tbl_3D.limit(1000).select('TotalHours').collect()
w = flattenList(w0, 'log')

data = {'TotalTickets':y , 'SevNum': x, 'TotalHours': w, 'Categories': z}
dataPD = pd.DataFrame(data)

fig = px.scatter_3d(dataPD, x='TotalTickets', y='TotalHours', z = 'SevNum', color = 'Categories')
fig.update_yaxes(nticks=5, title = "Severity")
fig.update_layout(title = "Hours of Effort vs. Severity")

py.plot(fig, output_type = "div")




py.plot(fig, output_type = "div")



