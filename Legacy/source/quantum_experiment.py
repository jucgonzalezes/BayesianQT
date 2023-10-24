# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 10:23:02 2022

@author: ale
"""
from qiskit import *
from qiskit.tools.monitor import job_monitor
from numpy import pi


# class experiments contains the real and simulated experiments of a real quantum computer
# the constructor takes in input the number of shots ie of experiments and whether you
# want the simulated data or the real ones
class experiments:
    # default simulated is 1, real 0 meaning we only want simulated values
    def __init__(self, n_of_shots, simulated=1, real=0):
        self.shots = n_of_shots
        self.Xsimulated = 0
        self.Ysimulated = 0
        self.Zsimulated = 0
        self.Xreal = 0
        self.Yreal = 0
        self.Zreal = 0
        if simulated == 1:
            self.simulated_X()
            self.simulated_Y()
            self.simulated_Z()
        if real == 1:
            self.real_X()
            self.real_Y()
            self.real_Z()

    def simulated_X(self):
        qr = QuantumRegister(1)
        cr = ClassicalRegister(1)
        circuit = QuantumCircuit(qr, cr)
        circuit.h(qr[0])
        circuit.barrier(qr[0])
        circuit.measure(qr, cr)
        simulator = Aer.get_backend("qasm_simulator")
        result = execute(circuit, backend=simulator, shots=self.shots).result()
        self.Xsimulated = result.get_counts(circuit)

    def simulated_Y(self):
        qr = QuantumRegister(1)
        cr = ClassicalRegister(1)
        circuit = QuantumCircuit(qr, cr)
        circuit.h(qr[0])
        circuit.barrier(qr[0])
        circuit.h(qr[0])
        circuit.measure(qr, cr)
        simulator = Aer.get_backend("qasm_simulator")
        result = execute(circuit, backend=simulator, shots=self.shots).result()
        self.Ysimulated = result.get_counts(circuit)

    def simulated_Z(self):
        qr = QuantumRegister(1)
        cr = ClassicalRegister(1)
        circuit = QuantumCircuit(qr, cr)
        circuit.h(qr[0])
        circuit.barrier(qr[0])
        circuit.u(pi / 2, 0, pi / 2, qr[0])
        circuit.measure(qr, cr)
        simulator = Aer.get_backend("qasm_simulator")
        result = execute(circuit, backend=simulator, shots=self.shots).result()
        self.Zsimulated = result.get_counts(circuit)

    def real_X(self):
        qr = QuantumRegister(1)
        cr = ClassicalRegister(1)
        circuit = QuantumCircuit(qr, cr)
        circuit.h(qr[0])
        circuit.barrier(qr[0])
        circuit.measure(qr, cr)

        IBMQ.load_account()
        provider = IBMQ.get_provider("ibm-q")
        qcomp = provider.get_backend("ibmq_belem")
        job = execute(circuit, backend=qcomp, shots=self.shots)
        job_monitor(job)
        result = job.result()
        self.Xreal = result.get_counts(circuit)

    def real_Y(self):
        qr = QuantumRegister(1)
        cr = ClassicalRegister(1)
        circuit = QuantumCircuit(qr, cr)
        circuit.h(qr[0])
        circuit.barrier(qr[0])
        circuit.h(qr[0])
        circuit.measure(qr, cr)

        IBMQ.load_account()
        provider = IBMQ.get_provider("ibm-q")
        qcomp = provider.get_backend("ibmq_belem")
        job = execute(circuit, backend=qcomp, shots=self.shots)
        job_monitor(job)
        result = job.result()
        self.Yreal = result.get_counts(circuit)

    def real_Z(self):
        qr = QuantumRegister(1)
        cr = ClassicalRegister(1)
        circuit = QuantumCircuit(qr, cr)
        circuit.h(qr[0])
        circuit.barrier(qr[0])
        circuit.u(pi / 2, 0, pi / 2, qr[0])
        circuit.measure(qr, cr)

        IBMQ.load_account()
        provider = IBMQ.get_provider("ibm-q")
        qcomp = provider.get_backend("ibmq_belem")
        job = execute(circuit, backend=qcomp, shots=self.shots)
        job_monitor(job)
        result = job.result()
        self.Zreal = result.get_counts(circuit)


# NB class mumbers are dictionaries so you must input "0" and "1" to get the associated count
ex1 = experiments(50, 1, 0)
print(ex1.Xsimulated)
print(ex1.Ysimulated)
print(ex1.Zsimulated)
"""
print(ex1.Xreal)
print(ex1.Yreal)
print(ex1.Zreal)
"""
