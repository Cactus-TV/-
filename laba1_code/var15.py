#!/usr/bin/env python
# coding: utf-8

# # Лабораторная работа №1
# ## Вариант 15 (15, а, г, е)
# ### Мотякин Артем Андреевич СКБ211

# __15: Массив данных ЗАГСа:__ ФИО жениха, дата рождения жениха,  ФИО невесты, дата рождения невесты, дата бракосочетания,  номер ЗАГСа (сравнение по полям – номер ЗАГСа, дата  бракосочетания, ФИО жениха)<br>
# 
# __а) Сортировка выбором<br>
# г) Шейкер-сортировка<br>
# е) Быстрая сортировка__


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
from datetime import datetime, timedelta
import time



arr_sizes = np.array([100, 500, 1000, 2000, 5000, 10000, 20000])
table = pd.read_csv('Names.csv', sep=';', index_col=False, header=None)#csv где по 100 женских и мужских ФИО
arr_names_man = np.array(table[0])
arr_names_woman = np.array(table[1])


# In[3]:


#Сгенерируем 7 наборов данных следующих размерностей: 100, 500, 1000, 2000, 5000, 10000, 20000
print("Generating data...\n")
for i in np.nditer(arr_sizes):
    name_groom = np.random.choice(arr_names_man, size=i)
    name_bride = np.random.choice(arr_names_woman, size=i)
    num_registry = np.random.randint(1, high=i+1, size=i)
    date_groom = []
    date_bride = [] 
    date_wedding = []
    
    for _ in range(i):
        start_date_birthday = datetime.strptime("01-01-1980", "%d-%m-%Y")
        end_date_birthday = datetime.strptime("01-01-2000", "%d-%m-%Y")

        start_date_wedding = datetime.strptime("01-01-2018", "%d-%m-%Y")
        end_date_wedding = datetime.strptime("01-01-2024", "%d-%m-%Y")

        days_birthday = (end_date_birthday - start_date_birthday).days
        days_wedding = (end_date_wedding - start_date_wedding).days

        date_groom.append((start_date_birthday + timedelta(days=np.random.randint(0, high=days_birthday))).strftime("%d-%m-%Y"))
        date_bride.append((start_date_birthday + timedelta(days=np.random.randint(0, high=days_birthday))).strftime("%d-%m-%Y"))
        date_wedding.append((start_date_wedding + timedelta(days=np.random.randint(0, high=days_wedding))).strftime("%d-%m-%Y"))
        
    print('Generating ', len(date_wedding), "done!")
    
    d = {"Groom fullname": name_groom,
           "Groom birth date": np.array(date_groom),
           "Bride fullname": name_bride,
           "Bride birth date": np.array(date_bride),
           "Wedding date": np.array(date_wedding),
           "Registry office number": num_registry}
    df = pd.DataFrame(data=d)
    df.to_csv(f"Data_{i}.csv")
    print('Saved ', len(date_wedding), "to csv!")


class Obj:
    def __init__(self, arr):
        self.num_reg = int(arr[6])
        self.gr_fname = arr[1]
        self.date_w = datetime.strptime(arr[5], "%d-%m-%Y")
        
    def __le__(self, other): # <=
        return (self.num_reg, self.gr_fname, self.date_w) <= (other.num_reg, other.gr_fname, other.date_w)
        
    def __ge__(self, other): # >=
        return (self.num_reg, self.gr_fname, self.date_w) >= (other.num_reg, other.gr_fname, other.date_w)
        
    def __lt__(self, other): # <
        return (self.num_reg, self.gr_fname, self.date_w) < (other.num_reg, other.gr_fname, other.date_w)
    
    def __gt__(self, other): # >
        return (self.num_reg, self.gr_fname, self.date_w) > (other.num_reg, other.gr_fname, other.date_w)
    
    
def SelectSort(arr):
    l = len(arr)
    for i in range(l): # i - current step
        k = i
        x = arr[i]
        for j in range(i+1, l): # loop for searching minimal element
            if Obj(arr[j]) < Obj(x):
                k = j
                x = arr[j]
        # swap minimal element and a[i]
        arr[k], arr[i] = arr[i], x


def ShakerSort(arr):
    k = len(arr) - 1
    ub = len(arr) - 1
    lb = 1
    while True:
        # from bottom to top passage 
        for j in reversed(range(1, ub+1)):
            if Obj(arr[j-1]) > Obj(arr[j]):
                arr[j-1], arr[j] = arr[j], arr[j-1]
                k = j
        lb = k+1
        
        # passage from top to bottom
        for j in range(lb, ub+1):
            if Obj(arr[j-1]) > Obj(arr[j]):
                arr[j-1], arr[j] = arr[j], arr[j-1]
                k = j
        ub = k-1
        if lb >= ub:
            break

            
def partition(arr, left, right):
    pivot = Obj(arr[right])
    sorted_idx = left - 1
    for j in range(left, right):
        if Obj(arr[j]) < pivot:
            sorted_idx += 1
            arr[sorted_idx], arr[j] = arr[j], arr[sorted_idx]
    arr[sorted_idx+1], arr[right] = arr[right], arr[sorted_idx+1]
    return sorted_idx + 1

def QuickSort(arr, left, right):
    if left < right:
        pivot = partition(arr, left, right)
        QuickSort(arr, left, pivot-1)
        QuickSort(arr, pivot+1, right)


print("Getting data...\n")
arr_select = []
arr_shaker = []
arr_quick = []
for i in np.nditer(arr_sizes):
    print(f"Computing {i}")
    df = pd.read_csv(f'Data_{i}.csv', index_col=False, header=None)
    arr1 = df.to_numpy().tolist()[1:]
    arr2 = df.to_numpy().tolist()[1:]
    arr3 = df.to_numpy().tolist()[1:]
    
    print(f"SelectSort {i}")
    start_time = time.time_ns() // 1000000 # time in milliseconds
    SelectSort(arr1)
    arr_select.append(time.time_ns() // 1000000 - start_time)
    df1 = pd.DataFrame(data=arr1)
    df1.to_csv(f"Data_SelectSort_{i}.csv")
    
    print(f"ShakerSort {i}")
    start_time = time.time_ns() // 1000000 # time in milliseconds
    ShakerSort(arr2)
    arr_shaker.append(time.time_ns() // 1000000 - start_time)
    df2 = pd.DataFrame(data=arr2)
    df2.to_csv(f"Data_ShakerSort_{i}.csv")
    
    print(f"QuickSort {i}")
    start_time = time.time_ns() // 1000000 # time in milliseconds
    QuickSort(arr3, 0, len(arr3)-1)
    arr_quick.append(time.time_ns() // 1000000 - start_time)
    df3 = pd.DataFrame(data=arr3)
    df3.to_csv(f"Data_QuickSort_{i}.csv")
    
    assert arr1==arr2
    assert arr1==arr3
    
print("Done!")


plt.plot(arr_sizes, arr_select, label='SelectSort')
plt.plot(arr_sizes, arr_shaker, label='ShakerSort')
plt.plot(arr_sizes, arr_quick, label='QuickSort')
plt.xlabel('Size of Input Data')
plt.ylabel('Time (milliseconds)')
plt.legend()
plt.show()

from math import log

plt.plot(arr_sizes, [log(i) for i in arr_select], label='SelectSort')
plt.plot(arr_sizes, [log(i) for i in arr_shaker], label='ShakerSort')
plt.plot(arr_sizes, [log(i) for i in arr_quick], label='QuickSort')
plt.xlabel('Size of Input Data')
plt.ylabel('Ln() from Time (milliseconds)')
plt.xticks(arr_sizes, rotation=-65)
plt.xlim(arr_sizes[0], arr_sizes[-1])
plt.legend()
plt.show()





