import Emulator_Classes as ec
reload(ec)
import random
import numpy as np

date_range = (2, 10, 5, 8)  # providers, weeks, days, slots

demographics = {'FName': 'Barry', 'LName': 'Allen', 'Age': 25, 'Location': 'Central City'}  # Type of physician, LOS
appt_length = (random.random() * 20) + 50  # Appt length centered on 60 minutes, uniform distribution 10 mins
p1 = ec.Patient(demographics, appt_length)
p1.no_show(date_range)  # Rudimentary assignment of no-show probabilities between .6 and .9

demographics = {'FName': 'Clark', 'LName': 'Kent', 'Age': 30, 'Location': 'Smallville'}
appt_length = (random.random() * 20) + 50  # Appt length centered on 60 minutes, uniform distribution 10 mins
p2 = ec.Patient(demographics, appt_length)
p2.no_show(date_range)

demographics = {'FName': 'Dwayne', 'LName': 'Allen', 'Age': 30, 'Location': 'Lions'}
appt_length = (random.random() * 20) + 50  # Appt length centered on 60 minutes, uniform distribution 10 mins
p3 = ec.Patient(demographics, appt_length)
p3.no_show(date_range)

demographics = {'FName': 'Elon', 'LName': 'Musk', 'Age': 27, 'Location': 'The Future'}
appt_length = (random.random() * 20) + 50  # Appt length centered on 60 minutes, uniform distribution 10 mins
p4 = ec.Patient(demographics, appt_length)
p4.no_show(date_range)

patients = [p1, p2, p3, p4]


s = ec.Schedule()
s.initialize(date_range[0], date_range[1], date_range[2], date_range[3])
availabilities = [(0, 0, 0, list(range(8))), (1, 0, 0, list(range(8)))]  # Both providers, week 1, day 1, all slots

for availability in availabilities:
    s.set_open_slots(availability, start=1, max_p=1)  # Start = Can we start an app? max_p = max p per physician


t = ec.TestAlgorithm()
t.input(s)

for patient in patients:
    t.schedule(patient)

for avail in availabilities:

    overtime = np.zeros(date_range[:3])

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
        print 'Provider'
        for w_ in w:
            for d_ in d:
                day = s.schedule[p_, w_, d_, :]

                over = 0
                for slot in day:
                    print slot
                    over = slot.get_req_time(predict_noshow=0, overflow=over)
                    print over

                overtime[p_, w_, d_] = over