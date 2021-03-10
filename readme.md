## Earliest Deadline First Algorithm
A task set will be given input by a user. 
Each task has (execution time, deadline, period). 
Using earliest deadline first algorithm, `code.py` will 
output the sequence of the schedule of tasks.

### Requirements
- Python 3
- Package listed in `requirements.txt`

### How to run?
- Create a virtual environment using Python 3:
    ```
    python3 -m venv venv
    ```
- Activate the virtual environment:
    ```
    source venv/bin/activate
    ```
- Install the required packages listed in `requirements.txt`:
    ```
    pip install -r requirements.txt
    ```
- Run the program `code.py` in the virtual environment:
    ```
    python code.py
    ```
- Example input:
    ```
    How many tasks to schedule: 3
    Enter the execution time, deadline and period of task 1: 1 4 4
    Enter the execution time, deadline and period of task 2: 2 6 6
    Enter the execution time, deadline and period of task 3: 3 8 8
    gantt_edf.png is generated based on the input tasks
    Deadline missed for each task: {'T1': 0, 'T2': 0, 'T3': 0}
    ```


## Git workflow

### Download project
```git
git clone https://github.com/tanjila2020/edf.git
```

### Download latest code
```bash
git pull origin main
```

### Upload your code
```bash
git add .
git commit -m "your message"
git push origin main
```
