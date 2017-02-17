from abc import ABCMeta, abstractmethod
import numpy as np
import random
import math
from Emulator_Classes import *

class PostProcessor:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.schedule = algorithm.curr_schedule
        self.slots = algorithm.curr_schedule.schedule
        self.date_range = self.schedule.get_range()

    def overtime(self):  # Get overtime per day
        overtime = np.empty(self.date_range[:3])

        p = self.date_range[0]
        w = self.date_range[1]
        d = self.date_range[2]

        for p_ in range(p):  # through all providers
            for w_ in range(w):
                for d_ in range(d):
                    day = self.slots[p_, w_, d_, :]

                    over = 0
                    for slot in day:
                        # print slot
                        over = slot.get_req_time(predict_noshow=0, overflow=over)
                        # print over

                    overtime[p_, w_, d_] = over

        if overtime is None:
            return None
        else:
            return overtime


def generate_patients(k, mean_appt_len, total_appt_spread, date_range):
    names = {
        'Adam': 0,
        'Barry': 0,
        'Clark': 0,
        'Dwayne': 0,
        'Elon': 0,
        'Fred': 0,
        'George': 0,
        'Harrison': 0,
        'Ingrid': 0,
        'Kurt': 0,
        'Larry': 0}

    patients = []

    for i in range(k):
        name = random.choice(names.keys())
        names[name] += 1
        demographics = {'FName': name + ' ' + str(names[name])}
        appt_length = (random.random() * total_appt_spread) + mean_appt_len - (0.5*total_appt_spread)
        patient = Patient(demographics, appt_length)
        patient.no_show(date_range)

        patients.append(patient)

    return patients




