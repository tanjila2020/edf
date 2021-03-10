# Require Python 3
import json
from functools import reduce
import matplotlib.pyplot as plt
from collections import Counter
import math


def generate_gnatt_chart(graph, time_span, name='figure'):
    if time_span > 60:
        time_span = 60

    fig, gnt = plt.subplots()
    task_names = [task[0] for task in graph]

    fig.suptitle(name)
    gnt.set_ylim(0, 5 * (len(task_names)))
    gnt.set_xlim(0, time_span)
    gnt.set_xlabel('Time')
    gnt.set_xticks([i for i in range(time_span + 1)])
    gnt.set_ylabel('Tasks')
    # gnt.set_yticks([i + 2.5 for i in range(0, 5 * len(task_names), 5)])
    gnt.set_yticks([i for i in range(0, 5 * len(task_names), 5)])
    gnt.set_yticklabels(task_names)
    gnt.grid(True)

    for i, task in enumerate(graph):
        gnt.broken_barh(task[1], (5 * (i), 5), facecolors='tab:blue')

    plt.savefig(name + '.png')
    plt.show()

    print(name + ".png is generated based on the input tasks")


def get_gcd(first_number, second_number):
    if second_number == 0:
        return first_number

    return get_gcd(second_number, first_number % second_number)


def get_lcm(first_number, second_number):
    return first_number * second_number // get_gcd(first_number, second_number)


def get_graph(jobs):
    graph = {}

    if len(jobs) > 60:
        jobs = jobs[:60]

    for job in jobs:
        task_name, execution_time, task_start_time, task_end_time, _, _ = job
        node = (task_start_time, execution_time)

        if task_name not in graph:
            graph[task_name] = [node]
        else:
            graph[task_name].append(node)

    graph = sorted(graph.items())

    return graph


def get_deadline_table(jobs):
    table = {}
    for job in jobs:
        task_name = job[0]
        deadline_missed = job[-1]
        table[task_name] = table.get(task_name, 0) + int(deadline_missed)
    return table


def task_no_of_ins(tasks):
    tasks_period_map = {}

    for task in tasks:
        tasks_period_map[task[0]] = task[1]

    return tasks_period_map


def task_period(tasks):
    tasks_period_map = {}

    for task in tasks:
        tasks_period_map[task[0]] = task[3]

    return tasks_period_map


def task_data_size(tasks):
    task_data_size_map = {}

    for task in tasks:
        task_data_size_map[task[0]] = task[4]

    return task_data_size_map


def create_queue(tasks, time_span):
    queue = []

    for task in tasks:
        task_name, execution_time, deadline, period, data_size = task

        for i in range(0, time_span + 1 - period, period):
            task_deadline = i + deadline
            queue.append((task_name, execution_time, i, task_deadline))

    queue = sorted(queue, key=lambda x: (x[3], x[2]))

    task_counter = []
    modified_queue = []

    # adding job number
    for q in queue:
        task_counter.append(q[0])
        task_count = task_counter.count(q[0])
        q = list(q)
        q.append(task_count)
        q = tuple(q)
        modified_queue.append(q)

    print('Sorted queue', modified_queue)

    return modified_queue


def preemptive(queue, tasks_period_map):
    output = []
    leftover = []
    job_response_time = {}
    cpu_current_time = 0

    for task in queue:
        task_name, execution_time, task_start_time, task_deadline, job_no = task
        task_start_time = max(task_start_time, cpu_current_time)
        task_end_time = task_start_time + execution_time
        deadline_missed = task_end_time > task_deadline

        job = (task_name,
               execution_time,
               task_start_time,
               task_end_time,
               deadline_missed,
               job_no)

        print('task_name, execution_time, task_start_time, task_end_time, deadline_missed, job_no', job)

        if not deadline_missed:
            if task_name not in job_response_time:
                job_response_time[task_name] = {}

            job_response_time[task_name][job_no] = task_start_time - (job_no - 1) * tasks_period_map[task_name]
            cpu_current_time = task_end_time
            output.append(job)
        else:
            leftover.append(job)

    print('leftover', leftover)

    return output, leftover, job_response_time


def non_preemptive(queue, tasks_period_map):
    job_response_time = []
    leftover = []
    output = []
    cpu_current_time = 0
    job_response_time = {}

    for task in queue:
        task_name, execution_time, task_start_time, task_deadline, job_no = task
        task_start_time = max(task_start_time, cpu_current_time)
        task_end_time = task_start_time + execution_time
        deadline_missed = task_end_time > task_deadline

        job = (task_name,
               execution_time,
               task_start_time,
               task_end_time,
               deadline_missed,
               job_no)

        print('task_name, execution_time, task_start_time, task_end_time, deadline_missed, job_no', job)

        if task_name not in job_response_time:
            job_response_time[task_name] = {}

        job_response_time[task_name][job_no] = task_start_time - (job_no - 1) * tasks_period_map[task_name]

        cpu_current_time = task_end_time

        output.append(job)

    print('Leftover', leftover)

    return output, job_response_time


def get_execution_time(no_of_instructions, cpu_capacity):
    return math.ceil(no_of_instructions / cpu_capacity)


def transfer_time(datasize, network_bw):
    return math.ceil(datasize / network_bw)


def print_response_time(response_time):
    for task in sorted(response_time.items()):
        print(task[0])
        for key, value in task[1].items():
            print('Job', key, ', Response time', value)


if __name__ == "__main__":
    given_tasks = []
    # total_number_of_tasks = int(input("How many tasks to schedule: "))

    # for i in range(1, total_number_of_tasks + 1):
    #     task_name = f"T{i}"

    #     no_of_instructions, deadline, period, data_size = map(
    #         int,
    #         input(f"Enter the No of Instructions, Deadline, Period and Data sizeof task {i}: ").split()
    #     )

    #     given_tasks.append([task_name, no_of_instructions, deadline, period, data_size])

    # example task
    given_tasks = [
        # task name, millions of instructions, dealine, period, data size
        ["T1", 48, 7, 10, 32],
        ["T2", 28, 4, 8, 24],
        ["T3", 98, 9, 12, 32],
    ]

    # v = float((input('Enter the value of v: ')))
    # o = float((input('Enter the value of o: ')))
    # freq = float((input('Enter the value of frequency: ')))
    # no_of_cores = float((input('Enter the value of number of core: ')))
    # network_bandwidth = float((input('Enter the value of network bandwidth: ')))
    # scheduling_period = float((input('Enter the value of scheduling period: ')))

    v = 7.683
    o = -4558.52
    freq = 2.5  # cpu frequency in GHz
    no_of_cores = 1
    network_bandwidth = 16  # network BW in Mbps
    # scheduling_period = 10

    cpu_capacity = ((v * (freq*1000) + o) * no_of_cores) * 0.001  # millons of instructions per milisecond
    cpu_capacity = math.floor(cpu_capacity)
    network_cpu_capacity = math.floor(cpu_capacity * 5)
    print('CPU Capacity: ', cpu_capacity)
    print('Network CPU Capacity: ', network_cpu_capacity)
    task_no_of_ins_map = task_no_of_ins(given_tasks)

    calculated_tasks = []

    for task in given_tasks:
        task_name, no_of_instructions, deadline, period, data_size = task
        execution_time = get_execution_time(no_of_instructions, cpu_capacity)
        calculated_tasks.append([task_name, execution_time, deadline, period, data_size])

    print('User input ', calculated_tasks)

    span = reduce(get_lcm, [task[2] for task in calculated_tasks])
    queue = create_queue(calculated_tasks, span)
    tasks_period_map = task_period(calculated_tasks)
    task_data_size_map = task_data_size(calculated_tasks)

    primary_cpu_jobs, offloadable, primary_job_response_time = preemptive(queue, tasks_period_map)
    primary_graph_data = get_graph(primary_cpu_jobs)

    # print("Deadline missed for each task: ")
    # print(get_deadline_table(queue))

    calc_offloadable = []

    for task in offloadable:
        task_name, execution_time, task_start_time, task_deadline, deadline_missed, job_no = task
        task_start_time += transfer_time(task_data_size_map[task_name], network_bandwidth)
        execution_time = get_execution_time(task_no_of_ins_map[task_name], network_cpu_capacity)
        calc_offloadable.append([task_name, execution_time, task_start_time, task_deadline, job_no])

    print('New start time after network transfer', calc_offloadable)

    network_cpu_jobs, network_job_response_time = non_preemptive(calc_offloadable, tasks_period_map)
    network_graph_data = get_graph(network_cpu_jobs)

    print('Primary CPU Job response time')
    print_response_time(primary_job_response_time)

    if len(calc_offloadable):
        print('Network CPU Job response time')
        print_response_time(network_job_response_time)

        print('Missed job count for each task')
        for key, value in Counter([job[0] for job in calc_offloadable]).items():
            print(key, value)

    generate_gnatt_chart(primary_graph_data, span, 'Primary CPU EDF')
    generate_gnatt_chart(network_graph_data, span, 'Network CPU EDF')
