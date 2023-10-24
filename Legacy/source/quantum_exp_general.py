# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 20:30:21 2022

@author: ale
"""

from qiskit import *
from qiskit.tools.monitor import job_monitor
from numpy import pi
from qiskit import Aer
from qiskit.circuit.random import random_circuit
import qiskit.quantum_info as qi


class experiments:
    def __init__(self, n_of_shots, n_of_qubits, real=0, random=0):
        self.n_of_shots = n_of_shots
        self.n_of_qubits = n_of_qubits
        self.random = random
        self.random_operator = []

        self.shots = n_of_shots
        if real == 0:
            self.Xsimulated = 0
            self.Ysimulated = 0
            self.Zsimulated = 0
            for i in range(3):
                self.simulated(i)
        if real == 1:
            self.Xreal = 0
            self.Yreal = 0
            self.Zreal = 0
            for i in range(3):
                self.rl(i)

    def simulated(self, op_number):
        qr = QuantumRegister(self.n_of_qubits)
        cr = ClassicalRegister(self.n_of_qubits)
        circuit = QuantumCircuit(qr, cr)

        for i in range(self.n_of_qubits):
            circuit.h(qr[i])
            circuit.barrier(qr[i])

        if self.random == 0:
            if op_number == 1:
                for i in range(self.n_of_qubits):
                    circuit.h(qr[i])
            if op_number == 2:
                for i in range(self.n_of_qubits):
                    circuit.u(pi / 2, 0, pi / 2, qr[i])

        else:
            circuit1 = random_circuit(self.n_of_qubits, 3, 3)
            self.random_operator.append(qi.Operator(circuit1))
            circuit.compose(circuit1, inplace=True)

        circuit.measure(qr, cr)

        simulator = Aer.get_backend("qasm_simulator")
        result = execute(circuit, backend=simulator, shots=self.shots).result()
        if op_number == 0:
            self.Xsimulated = result.get_counts(circuit)
        if op_number == 1:
            self.Ysimulated = result.get_counts(circuit)
        if op_number == 2:
            self.Zsimulated = result.get_counts(circuit)

    def rl(self, op_number):
        qr = QuantumRegister(self.n_of_qubits)
        cr = ClassicalRegister(self.n_of_qubits)
        circuit = QuantumCircuit(qr, cr)

        for i in range(self.n_of_qubits):
            circuit.h(qr[i])
            circuit.barrier(qr[i])

        if self.random == 0:
            if op_number == 1:
                for i in range(self.n_of_qubits):
                    circuit.h(qr[i])
            if op_number == 2:
                for i in range(self._of_qubits):
                    circuit.u(pi / 2, 0, pi / 2, qr[i])

        else:
            circuit1 = random_circuit(self.n_of_qubits, 3, 3)
            self.random_operator.append(qi.Operator(circuit1))
            circuit.compose(circuit1, inplace=True)

        circuit.measure(qr, cr)

        IBMQ.load_account()
        provider = IBMQ.get_provider("ibm-q")
        qcomp = provider.get_backend("ibmq_belem")
        job = execute(circuit, backend=qcomp, shots=self.shots)
        job_monitor(job)
        result = job.result()
        if op_number == 0:
            self.Xsimulated = result.get_counts(circuit)
        if op_number == 1:
            self.Ysimulated = result.get_counts(circuit)
        if op_number == 2:
            self.Zsimulated = result.get_counts(circuit)


ex1 = experiments(50, 2, 0, 1)
print(ex1.Xsimulated)
print(ex1.Ysimulated)
print(ex1.Zsimulated)
print(ex1.random_operator[0])
print(ex1.random_operator[1])
print(ex1.random_operator[2])
