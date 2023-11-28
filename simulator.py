import concurrent.futures
import math
import copy
import time 
import numpy as np

from tqdm import tqdm
from collections import deque
from typing import Optional
from mcTasks import MCTask, MCTaskSet

class ModeSchedule:

    def __init__(self, time, mode):
        self.time = time
        self.mode = mode

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.__dict__)

class MCTaskSimulator:

    def __init__(self):
        self.current_mode = "LO"
        self.current_time = 0
        self.current_task = None
        self.job_queue = []
        self.mode_change_time = 0
        self.mode_schedule = deque()

    def reset(self):
        self.current_mode = "LO"
        self.current_time = 0
        self.current_task = None
        self.job_queue = []
        self.mode_schedule = deque()

    def tasks_lcm(self, tasks):
        # calculate T_LOs LCM
        task: MCTask
        lcm = 1
        for task in tasks:
            lcm = lcm * task.T_LO // math.gcd(lcm, task.T_LO)
        return lcm

    def release_task(self, task: list) -> Optional[list]:
        t: MCTask = task[1]
    
        task[1].released_mode = self.current_mode
        if self.current_mode == "HI":
            task[1].deadline = (self.current_time + task[1].T_HI)
            if self.current_time == 0:
                return task
            elif (self.current_time - task[1].HI_start) % task[1].T_HI == 0:
                return task

        elif self.current_mode == "LO":
            task[1].deadline = self.current_time + task[1].T_LO
            if self.current_time == 0:
                return task
            elif self.current_time % task[1].T_LO == 0:
                return task

        return None

    def set_mode_change(self, schedule: ModeSchedule):
        self.mode_schedule.append(schedule)

    def mode_change(self):
        if len(self.mode_schedule) == 0:
            return

        if self.mode_schedule[0].time <= self.current_time:
            mc = self.mode_schedule[0]
            self.current_mode = mc.mode

        return

    def simulate_edf(self, tasks):
        lcm = self.tasks_lcm(tasks)
        n = len(tasks)
        u = MCTaskSet().calc_utilization(tasks)
        tasks = [[i + 1, task] for i, task in enumerate(tasks)]

        while self.current_time < lcm:
            # task release
            for task in tasks:
                t = copy.deepcopy(task)
                released_task = self.release_task(t)

                if released_task is not None:
                    self.job_queue.append(t)
                    # sort by tasks deadline
                    self.job_queue = sorted(self.job_queue, key=lambda x: x[1].deadline)
                    
            # check scheduled mode change
            self.mode_change()
            # 1sec spend
            self.current_time += 1
            
            # early deadline first
            for i in range(len(self.job_queue)):
                task = self.job_queue[i]

                # deadline missed
                if task[1].deadline < self.current_time:
                    # print()
                    # print(f"\t\tTask {task[0]} missed {task[1]}")
                    # print("Mode changed when: ", self.mode_schedule[0])
                    # print("Scheduling tasks: \n\t" + "\n\t".join([f"{pt}" for pt in tasks]))
                    # print("Jobs: \n\t" + "\n\t".join([f"{pj}" for pj in self.job_queue]))
                    # print("LCM: " + str(lcm))
                    # print("Utilization: " + str(u))
                    # print("Current time: " + str(self.current_time) + " Mode: " + self.current_mode)

                    raise Exception(f"Task missed deadline when time {self.current_time}")
                # task 1sec spend
                task[1].C -= 1
                if task[1].C == 0:
                    if task[1].HI_start == 0 and task[1].released_mode == "HI":
                        for j in range(len(tasks)):
                            if tasks[j][0] == task[0]:
                                tasks[j][1].HI_start = task[1].deadline
                    self.job_queue.remove(task)
                break
    
    def simulate_rm(self, tasks):
        lcm = self.tasks_lcm(tasks)
        u = MCTaskSet(scheduler="rm").calc_utilization(tasks)
        tasks = [[i, task] for i, task in enumerate(tasks)] # tasks[0] is priority

        while self.current_time < lcm:
            for task in tasks:
                t = copy.deepcopy(task)
                released_task = self.release_task(t)

                if released_task is not None:
                    self.job_queue.append(t)
                    # sort by tasks priority 
                    self.job_queue = sorted(self.job_queue, key=lambda x: x[0])

            # check scheduled mode change
            self.mode_change()
            # 1sec spend
            self.current_time += 1
            
            for i in range(len(self.job_queue)):
                task = self.job_queue[i]
                # deadline missed
                if task[1].deadline < self.current_time:
                    raise Exception(f"Task missed deadline when time {self.current_time}")
                # task 1sec spend
                task[1].C -= 1
                if task[1].C == 0:
                    self.job_queue.remove(task)
                break



def main():
    app = MCTaskSimulator()
    taskset = MCTaskSet(
        max_T_HI=15,
        min_T_HI=10,
        max_T_LO=30,
        min_T_LO=15,
        max_u=1.2,
        c=0.1
    )
    # tasks = taskset.create_taskset(n=100, hi=3, lo=5)
    # taskset.export_taskset(tasks)
    tasks = taskset.import_taskset("taskset_u_1.3.pkl")

    fail_count = 0
    pass_count = 0
    for task in tqdm(tasks):
        try:
            lcm = app.tasks_lcm(task)
            for i in np.linspace(int(lcm / 100), lcm, 99):
                app.set_mode_change(ModeSchedule(int(i), "HI"))
                app.simulate(task)
                app.reset()


        except Exception as e:
            print(e)
            fail_count += 1
            app.reset()

    print()
    print("Total:", pass_count + fail_count, "Fail:", fail_count, "Success:", pass_count, "Ratio:",
          pass_count / (pass_count + fail_count))

def ensure_future(task, scheduler="edf"):
    app = MCTaskSimulator()
    try:
        for t in task:
            if t.X == "HI":
                for k in range(1, 33+1):
                    app.set_mode_change(ModeSchedule(t.T_LO * k, "HI"))
                    if scheduler == "edf":
                        app.simulate_edf(task)
                    elif scheduler == "rm":
                        app.simulate_rm(task)
                    app.reset()

        return True

    except Exception as e:
        return False


def multi_main(file=None, obj=None, scheduler="edf"):
    if file is not None:
        taskset = MCTaskSet().import_taskset(file)
        print(file)
    else:
        taskset = obj

    passed = 0
    failed = 0
    try:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            with tqdm(total=len(taskset)) as progress:
                futures = []
                for i, task in enumerate(taskset):
                    future = executor.submit(ensure_future, task, scheduler)
                    future.add_done_callback(lambda p: progress.update())
                    futures.append(future)

                for future in futures:
                    result = future.result()
                    if result:
                        passed += 1
                    else:
                        failed += 1

    except KeyboardInterrupt:
        for future in futures:
            future.cancel()

    return passed, failed

if __name__ == "__main__":
    import sys 
    path = sys.argv[1]

    multi_main(path)
