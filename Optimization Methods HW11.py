
# coding: utf-8

# In[22]:


# Import


# In[23]:


from gurobi import *


# In[24]:


import pandas as pd
from pandas import ExcelFile
fc = pd.read_excel('/Users/Max/Downloads/data.xlsx', sheet_name='FCs')
dp = pd.read_excel('/Users/Max/Downloads/data.xlsx', sheet_name='DPs')


# In[25]:


#fc


# In[26]:


#dp


# In[27]:


model = Model("Homework 11")


# In[28]:


#cost matrix


# In[29]:


costDF = pd.read_excel('/Users/Max/Downloads/data.xlsx', sheet_name='Sheet2')
#costDF


# In[30]:


import math

for i in range(20):
    for j in range(10):
            costDF.iloc[i,j]=math.sqrt((fc.iloc[j,0]-dp.iloc[i,0])**2+(fc.iloc[j,1]-dp.iloc[i,1])**2)
            
#costDF


# In[31]:


# decision variables 


# In[32]:


x = [[0 for i in range(3)]for j in range(10)]
for i in range(3):
    for j in range(10):
        x[j][i]=model.addVar( vtype = GRB.BINARY, name = "x" + str(j+1)+ "_" + str(i+1))
model.update()        


# In[33]:


#x


# In[34]:


y = [[[0 for k in range(3)]for i in range(20)]for j in range(10)]
for k in range(3):
    for i in range(10):
        for j in range(20):
            y[i][j][k]=model.addVar( vtype = GRB.BINARY, name = "y" + str(j+1)+ "_" + str(i+1)+"_"+str(k+1))
model.update()            
#y


# In[35]:


objective_function = LinExpr()

for j in range(20):
    for i in range(10):
        objective_function+=6.0*(y[i][j][0]*costDF.iloc[j,i])
        
for j in range(20):
    for i in range(10):
        objective_function+=5.0*(y[i][j][1]*costDF.iloc[j,i])
        
for j in range(20):
    for i in range(10):
        objective_function+=9.0*(y[i][j][2]*costDF.iloc[j,i])

model.setObjective(objective_function,GRB.MINIMIZE)
model.update()


# In[36]:


#constraints


# In[37]:


for k in range(3):
    for j in range(10):
        for i in range(20):
            constraint_expression = LinExpr()
            constraint_expression+=y[j][i][k]
            model.addConstr( lhs = constraint_expression, sense = GRB.LESS_EQUAL, rhs = x[j][k] )
            
for k in range(3):
    constraint_expression = LinExpr()
    for j in range(10):
        constraint_expression+=x[j][k]
    model.addConstr( lhs = constraint_expression, sense = GRB.EQUAL, rhs = k+1 )

for k in range(3):
    for j in range(20):
        constraint_expression = LinExpr()
        for i in range(10):
            constraint_expression+=y[i][j][k]
        model.addConstr( lhs = constraint_expression, sense = GRB.EQUAL, rhs = 1 )

for k in range(1,3):
    for j in range(10):
        constraint_expression = LinExpr()
        constraint_expression+=x[j][k]
        model.addConstr( lhs = constraint_expression, sense = GRB.GREATER_EQUAL, rhs = x[j][k-1] )


model.update()  

#for k in range(3):
#    constraint_expression = LinExpr()
#    for j in range(10):
#        for i in range(20):
#            constraint_expression+=y[i][j][k]
#        model.addConstr( lhs = constraint_expression, sense = GRB.EQUAL, rhs = 20 )
#for i in range(3):
#    constraint_expression=LinExpr()
#    for j in range(10):
#        constraint_expression+=1.0*x[j][i]
#    model.addConstr( lhs = constraint_expression, sense = GRB.EQUAL, rhs = 1 )    
#model.update()
#for i in range(10):
#    constraint_expression=LinExpr()
#    for j in range(3):
#        constraint_expression+=x[i][j]
#    model.addConstr(lhs=constraint_expression, sense=GRB.EQUAL, rhs=1)    
#model.update()


# In[38]:


model.write("gurobi_output_hw11.lp")


# In[39]:


model.optimize()
print("\nOptimal Objective: " + str(model.ObjVal)) 

#extract decision variables
print("\nOptimal Solution:") 
allVars = model.getVars()

for var in allVars:
    print(var.varName + " " + str(var.x))
    

