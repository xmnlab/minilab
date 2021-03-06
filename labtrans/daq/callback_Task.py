# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 17:04:42 2013

@author: ivan
"""

from PyDAQmx import *
from PyDAQmx.DAQmxCallBack import *
from numpy import zeros

"""This example is a PyDAQmx version of the ContAcq_IntClk.c example
It illustrates the use of callback function

This example demonstrates how to acquire a continuous amount of
data using the DAQ device's internal clock. It incrementally store the data
in a Python list.

This example is also an example for the object oriented uses of PyDAQmx
"""
import time

class CallbackTask(Task):
    def __init__(self):
        Task.__init__(self)
        self.data = zeros(1000)
        self.a = []
        self.CreateAIVoltageChan("Dev1/ai0","",DAQmx_Val_RSE,-10.0,10.0,DAQmx_Val_Volts,None)
        self.CfgSampClkTiming("",10000.0,DAQmx_Val_Rising,DAQmx_Val_ContSamps,1000)
        self.AutoRegisterEveryNSamplesEvent(DAQmx_Val_Acquired_Into_Buffer,1000,0)
        self.AutoRegisterDoneEvent(0)
    def EveryNCallback(self):
        read = int32()
        self.ReadAnalogF64(1000,10.0,DAQmx_Val_GroupByScanNumber,self.data,1000,byref(read),None)
        self.a.extend(self.data.tolist())
        print time.time(), self.data
    def DoneCallback(self, status):
        print "Status",status.value
        return 0 # The function should return an integer


task=CallbackTask()
task.StartTask()

raw_input('Acquiring samples continuously. Press Enter to interrupt\n')

task.StopTask()
task.ClearTask()