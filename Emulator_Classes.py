from abc import ABCMeta, abstractmethod
import numpy as np
import random
import math


class Algorithm:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.curr_schedule = None

    def input(self, schedule):  # Pass in the empty schedule overall
        self.curr_schedule = schedule

    def schedule(self, patient):  # pass in a patient
        p, w, d, s, noshow = self.schedule_patient(patient)  # get the best p/w/d/s
        if noshow == 1e99:  # No more slots
            print 'No More available slots'
            return
        else:
            patient.set_noshow(noshow)
            self.curr_schedule.assign_patient(patient, p, w, d, s)  # Assign to the best
        return

    def schedule_patient(self, patient):
        # Magic happens here on our end
        # For an invalid slot, return noshow = 1e99
        p = 0
        w = 0
        d = 0
        s = 0
        noshow = 0
        return p, w, d, s, noshow

    def output(self):  # output the current schedule
        return self.curr_schedule


class TestAlgorithm(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)

    def schedule_patient(self, patient):
        probabilities = patient.get_probabilities()
        probabilities[np.equal(self.curr_schedule.schedule, None)] = 1e99  # Never schedule with unavailable slots
        value_range = self.curr_schedule.get_range()

        scheduled = False
        while scheduled == False:
            assigned = np.argmin(probabilities)  # Take smallest probability
            p, w, d, s = np.unravel_index(assigned, value_range)
            noshow = probabilities[p, w, d, s]

            if noshow == 1e99:
                p, w, d, s = 1e99, 1e99, 1e99, 1e99
                return p, w, d, s, noshow

            if self.curr_schedule.schedule[p, w, d, s].can_assign():
                scheduled = True
                return p, w, d, s, noshow
            else:
                probabilities[p, w, d, s] = 1e99

    def schedule(self, patient):  # pass in a patient
        p, w, d, s, noshow = self.schedule_patient(patient)  # get the best p/w/d/s
        if noshow == 1e99:  # No more slots
            print 'No More available slots'
            return
        else:
            patient.set_noshow(noshow)
            self.curr_schedule.assign_patient(patient, p, w, d, s)  # Assign to the best
        return


class Schedule:
    def __init__(self):
        self.schedule = None

    def initialize(self, providers, weeks, days, slots):
        self.schedule = np.empty(shape=(providers, weeks, days, slots), dtype=object)  # Dtype is whatever object our 'patients' are

    def assign_patient(self, patient, p, w, d, s):
        try:
            slot = self.schedule[p, w, d, s]
            if slot == None:
                print 'That slot is not available!'
                return
            else:
                if slot.assign_patient(patient):
                    print 'Assigned: ', patient.demo[
                        'FName'], 'Physician:', p + 1, ' Week:', w + 1, 'Day:', d + 1, 'Slot:', s + 1
                else:
                    print 'No more patients can go in this slot! Desired patient not assigned'
                return
        except IndexError:
            print 'One of physician, week, day, slot is out of range.'
            print 'The appropriate range is: '
            print self.schedule.shape


    def set_open_slots(self, tup, start=1, max_p=1):
        # This is disgusting

        p = tup[0]
        w = tup[1]
        d = tup[2]
        s = tup[3]

        if type(p) == int:
            p = [p]
        if type(w) == int:
            w = [w]
        if type(d) == int:
            d = [d]
        if type(s) == int:
            s = [s]

        for i in p:
            for j in w:
                for k in d:
                    for l in s:
                        slot = Slot(start, max_p)
                        self.schedule[i, j, k, l] = slot
        return

    def get_range(self):
        return self.schedule.shape

    def day_summary(self, p, w, d, one_index=1):
        if ~one_index:
            p -= 1
            w -= 1
            d -= 1
        try:
            slots = self.schedule[p, w, d, :]
            print 'Physician: {0}, Week: {1}, Day: {2}'.format(p, w, d) + '\n'
            for i in range(len(slots)):
                print 'Slot: {0}'.format(i+1) + '\t' + slots[i].summary()
        except IndexError:
            print 'Not in date range'


class Slot:
    def __init__(self, start=1, max_p=1):
        self.max_patients = max_p
        self.can_start = start
        self.patients = []
        self.duration = 60  # Slot duration

    def __str__(self):
        final_str = 'Scheduled Patients: '
        for i in self.patients:
            final_str += i.demo['FName']
        return final_str

    def can_start(self):
        return self.can_start

    def max_patients(self):
        return self.max_patients

    def assign_patient(self, patient):
        if len(self.patients) < self.max_patients:
            self.patients.append(patient)
            return True
        else:
            return False

    def can_assign(self):
        if len(self.patients) < self.max_patients:
            return True
        else:
            return False

    def get_req_time(self, predict_noshow=0, overflow=0):

        if predict_noshow:  # If we want to predict who's showing up as well
            overflow -= self.duration

            for patient in self.patients:
                r = random.random()

                if r > patient.get_noshow():  # Patient showed up
                    overflow += patient.appt_length

            overflow = max(overflow, 0)

            return overflow

        else:
            overflow -= self.duration
            for patient in self.patients:
                overflow += patient.appt_length
            overflow = max(overflow, 0)

            return overflow

    def summary(self):
        if len(self.patients) == 0:
            return 'No Patient Assigned'
        else:
            return_str = ''
            for p in self.patients:
                return_str += p.demo['FName'] + "\t" + 'Appt length: ' + str(p.appt_length) + ', \t'
            return return_str


class Patient:
    def __init__(self, demographics, appt):
        self.demo = {}
        self.probs = None
        self.noshow = None
        self.appt_length = appt
        for key in demographics:
            self.demo[key] = demographics[key]

    def no_show(self, temp_range):
        p = temp_range[0]
        w = temp_range[1]
        d = temp_range[2]
        s = temp_range[3]

        self.probs = np.random.rand(p, w, d, s)*(.3)
        return

    def get_probabilities(self):
        return self.probs

    def set_noshow(self, noshow):
        self.noshow = noshow
        return

    def get_noshow(self):
        return self.noshow


class PostProcessor:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.schedule = algorithm.curr_schedule
        self.slots = algorithm.curr_schedule.schedule
        self.date_range = self.schedule.get_range()

    def overtime(self, availabilities):  # Get overtime per day
        overtime = None

        for avail in availabilities:

            overtime = np.empty(self.date_range[:3])

            p = avail[0]
            w = avail[1]
            d = avail[2]

            if type(p) == int:
                p = [p]
            if type(w) == int:
                w = [w]
            if type(d) == int:
                d = [d]

            for p_ in p:  # through all providers
                # print 'Provider'
                for w_ in w:
                    for d_ in d:
                        day = self.slots[p_, w_, d_, :]

                        over = 0
                        for slot in day:
                            # print slot
                            over = slot.get_req_time(predict_noshow=0, overflow=over)
                            # print over

                        overtime[p_, w_, d_] = over

        if overtime is None:
            print 'No Availabilties inputted!'
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
        print demographics, appt_length
        patient = Patient(demographics, appt_length)
        patient.no_show(date_range)

        patients.append(patient)

    return patients




