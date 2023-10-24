from qiskit import *
from qiskit.tools.monitor import job_monitor
from numpy import pi
from qiskit import Aer
from qiskit.circuit.random import random_circuit
import qiskit.quantum_info as qi
import numpy as np


class experiments:
    def __init__(self, n_of_shots, n_of_qubits, real=0, random=0,vec=[]):
        self.n_of_shots = n_of_shots
        self.n_of_qubits = n_of_qubits
        self.random = random
        self.operators = []
        self.real_state = 0
        self.vec = vec

        self.shots = n_of_shots
        if real == 0:
            self.simulated = [0] * (2 ** n_of_qubits + 1)
            for i in range(2 ** n_of_qubits + 1):
                self.simulate(i)
        if real == 1:
            self.res = [0] * (2 ** n_of_qubits + 1)
            for i in range(2 ** n_of_qubits + 1):
                self.rl(i)

    def simulate(self, op_number):
        qr = QuantumRegister(self.n_of_qubits)
        cr = ClassicalRegister(self.n_of_qubits)
        circuit = QuantumCircuit(qr, cr)

        self.real_state = np.matrix(
            [
                [1 if i == j == 0 else 0 for i in range(2 ** self.n_of_qubits)]
                for j in range(2 ** self.n_of_qubits)
            ]
        )
        for i in range(self.n_of_qubits):
            circuit.h(qr[i])
            circuit.barrier(qr[i])

        self.real_state = np.matmul(
            np.matrix(qi.Operator(circuit)),
            np.matmul(self.real_state, np.matrix(qi.Operator(circuit)).H),
        )
        if self.random == 0:
            qr1 = QuantumRegister(self.n_of_qubits)
            cr1 = ClassicalRegister(self.n_of_qubits)
            circuit1 = QuantumCircuit(qr1, cr1)

            if op_number < 2 ** self.n_of_qubits:
                for i in range(self.n_of_qubits):
                    if self.vec[op_number][i] == "0":
                        circuit.h(qr[i])
                        circuit1.h(qr1[i])
                    else:
                        circuit1.u(pi / 2, 0, pi / 2, qr1[i])
                        circuit.u(pi / 2, 0, pi / 2, qr[i])
                self.operators.append(qi.Operator(circuit1))

            else:
                self.operators.append(qi.Operator(circuit1))

        else:
            circuit1 = random_circuit(self.n_of_qubits, 3, 3)
            self.operators.append(qi.Operator(circuit1))
            circuit.compose(circuit1, inplace=True)

        circuit.measure(qr, cr)

        simulator = Aer.get_backend("qasm_simulator")
        result = execute(circuit, backend=simulator, shots=self.shots).result()
        self.simulated[op_number] = result.get_counts(circuit)

    def rl(self, op_number):
        qr = QuantumRegister(self.n_of_qubits)
        cr = ClassicalRegister(self.n_of_qubits)
        circuit = QuantumCircuit(qr, cr)

        for i in range(self.n_of_qubits):
            circuit.h(qr[i])
            circuit.barrier(qr[i])

        if self.random == 0:
            qr1 = QuantumRegister(self.n_of_qubits)
            cr1 = ClassicalRegister(self.n_of_qubits)
            circuit1 = QuantumCircuit(qr1, cr1)

            if op_number < 2 ** self.n_of_qubits:
                for i in range(self.n_of_qubits):
                    if self.vec[op_number][i] == "0":
                        circuit.h(qr[i])
                        circuit1.h(qr1[i])
                    else:
                        circuit1.u(pi / 2, 0, pi / 2, qr1[i])
                        circuit.u(pi / 2, 0, pi / 2, qr[i])
                self.operators.append(qi.Operator(circuit1))

            else:
                self.operators.append(qi.Operator(circuit1))

        else:
            circuit1 = random_circuit(self.n_of_qubits, 3, 3)
            self.operators.append(qi.Operator(circuit1))
            circuit.compose(circuit1, inplace=True)

        circuit.measure(qr, cr)

        IBMQ.load_account()
        provider = IBMQ.get_provider("ibm-q")
        qcomp = provider.get_backend("ibmq_belem")
        job = execute(circuit, backend=qcomp, shots=self.shots)
        job_monitor(job)
        result = job.result()
        self.res[op_number] = result.get_counts(circuit)
