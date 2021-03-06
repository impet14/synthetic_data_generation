# Autogenerated with SMOP 
from smop.core import *
# 
import sys
import os
import numpy as np
import scipy.io as sio
import pandas as pd
import pdb
from oct2py import octave
from oct2py import Oct2Py
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
oc = Oct2Py() 

@function
def Read_Traj(dir=None,*args,**kwargs):
    varargin = Read_Traj.varargin
    nargin = Read_Traj.nargin

    #Read Trajectory from path
#In case the input is from raw input, feature selection might be required
#feature_selection need to be clear!!!!
# feature_selection = [1:19 ];
    data=pd.read_csv(dir, sep=',',header=None) #csvread(dir)

# Read_Traj.m:6
    num_frame=size(data,1)
# Read_Traj.m:7
    t=arange(1,num_frame,1)
# Read_Traj.m:8
    data=matlabarray(cat(t.T,data))
# Read_Traj.m:9.
    # traj = data(:,feature_selection);
    traj=copy(data)
# Read_Traj.m:11
    sio.savemat('trajpy.mat', {'traj':traj})
    return traj

@function
def random_traj(traj_dir=None,K=None,dis_threshold=None,*args,**kwargs):
    
    varargin = random_traj.varargin
    nargin = random_traj.nargin

    #Implemented by Ruikun Luo
#Basic idea is from STOMP paper, only generate multiple random traj
#traj = N * D, where N is the traj length, D is the traj dimension
    
    #traj=Read_Traj(traj_dir)
    data=sio.loadmat('traj.mat')
    traj = data['traj']

# random_traj.m:6
    ## Precompute part
#### A, R_1, M
#### N: traj length, M: traj dimension
    N=size(traj,1)
# random_traj.m:10
    D=size(traj,2)
# random_traj.m:11 x=zeros(N-2,2)
    #save('original.mat','traj')
    A=np.eye(N)
# random_traj.m:15
    x=dot(np.eye(N - 1),- 2)
# random_traj.m:16 x = [zeros(1,N);x zeros(N-1,1)];
    #x=matlabarray(cat([oc.zeros(1,N)],[x,oc.zeros(N - 1,1)])).reshape
    temp = np.hstack([x, zeros(N-1,1)])
    x=np.vstack([zeros(1,N),temp])
# random_traj.m:17
    A=A + x
# random_traj.m:18
    x=np.eye(N - 2)
# random_traj.m:19 x = [zeros(2,N);x zeros(N-2,2)];
    temp =np.hstack([x,zeros(N - 2,2)])
    x=np.vstack([zeros(2,N),temp])

# random_traj.m:20
    A=A + x
# random_traj.m:21 A = [A; zeros(1,N-2) 1 -2;zeros(1,N-1) 1 ];
    A=np.vstack([A, np.hstack([ zeros(1,N - 2),np.mat([1]),np.mat([-2]) ]),np.hstack([ zeros(1,N - 1),np.mat([1]) ]) ])
# random_traj.m:22
    R_1=inv(dot(A.T,A))
# random_traj.m:23
    R=dot(A.T,A)
# random_traj.m:24 y = max(R_1,[],1);
    y=np.max(R_1, axis=0) #y = np.amax(R_1, axis=0)
# random_traj.m:25
    y=np.tile(y,(N,1))
# random_traj.m:26 M = R_1 ./ y *(1/N);
    M=np.dot(np.divide(R_1, y) , (1.0/N))
# random_traj.m:27
    ## generate traj
#### loop for each dimension, ignore the first dimension because it is the
#### time index
    for ind_D in arange(0,K,1): 
        theta=traj[:,1:]
# random_traj.m:33 np.random.multivariate_normal (np.zeros(N), R_1, D-1).T
        theta_k=np.random.multivariate_normal (np.zeros(N),R_1,D - 1).T
        
# random_traj.m:34
        test_traj=theta + theta_k
# random_traj.m:35
        while fastdtw(test_traj,theta,dist=lambda x, y: np.linalg.norm(x - y, ord=1)) > dis_threshold:
            print fastdtw(test_traj,theta,dist=lambda x, y: np.linalg.norm(x - y, ord=1)),
            theta_k=np.dot(M,theta_k)
# random_traj.m:37
            test_traj=theta + theta_k

# random_traj.m:38
        traj_opt[ind_D]=traj + np.hstack([zeros(N,1),theta_k])
        pdb.set_trace();
# random_traj.m:40
        pdb.set_trace();
        print('.')
    save('random_traj.mat','traj_opt')
    pdb.set_trace();
    return traj_opt
    

def main():
  print "testing synthetic generation"
  random_traj('/home/john/unsupervised_online_reaching_prediction/scripts/csvFiles/obsTraj.csv',5,0.04)
  
if __name__== "__main__":
  main()

print "End synthetic generation"