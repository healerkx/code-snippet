
import datetime, re, os, sys, dateutil.parser
from functools import reduce
from pyquery import PyQuery as pq
from optparse import OptionParser


class Objective:
    def __init__(self):
        self.projects = []

    def add_project(self, project):
        self.projects.append(project)

    def get_current_project(self):
        return self.projects[-1]

class Project:
    def __init__(self, project_name):
        self.project_name = project_name
        self.stages = []

    def add_stage(self, stage):
        self.stages.append(stage)

    def get_current_stage(self):
        return self.stages[-1]

    def all_assignees(self):
        return set(reduce(lambda y, x: y + list(x.all_assignees()), self.stages, []))

Stage_Design    = 1
Stage_Develop   = 2
Stage_CoDebug   = 3
Stage_Test      = 4
Stage_Online    = 5

Stages = { 
    Stage_Design: ("设计", "#9feeee"),
    Stage_Develop: ("开发", "#7feeaa"),
    Stage_CoDebug: ("联调", "#ffee7f"),
    Stage_Test: ("测试", "#ffaa8f"),
    Stage_Online: ("上线", "#dd4444")}

def parse_stage(stage):
    for s, n in Stages.items():
        if n[0] == stage:
            return s
    return 0

class Stage:
    def __init__(self, stage_name):
        self.stage_name = stage_name
        self.stage = parse_stage(stage_name)
        self.tasks = []
    
    def add_task(self, task):
        self.tasks.append(task)

    def all_assignees(self):
        return set(reduce(lambda y, x: y + x.assignees, self.tasks, []))

class Task:
    def __init__(self, task_name, begin_date, end_date):
        self.task_name = task_name
        self.begin_date = begin_date
        self.end_date = end_date
        self.assignees = []
    
    def add_assignee(self, assignee):
        self.assignees.append(assignee)

def get_earliest_date(o):
    date = "3000-01-01"
    for p in o.projects:
        for s in p.stages:
            for t in s.tasks:
                if date > t.begin_date:
                    date = t.begin_date
    return date


def regular_date(date):
    return dateutil.parser.parse(date).strftime("%Y-%m-%d")

def parse_date(date):
    date = date.strip()
    ps = date.split("-")
    if len(ps) == 3: return date
    elif len(ps) == 2: return f"{datetime.datetime.now().year}-{date}"
    else: return f"{datetime.datetime.now().year}-{datetime.datetime.now().month}-{date}"

def parse_assignees(assignees_part):
    r = re.findall(r"(\w+)", assignees_part)
    return r

def parse_time_range(time_range_part):
    time_range_part = time_range_part.strip("[] ")
    if '~' in time_range_part: return time_range_part.split('~')
    else: return [time_range_part, time_range_part]

def parse_line(line):
    r = re.findall(r"(#+)\s*(\w*)\s*(\[[\w~-]*\])?\s*(@.*)?", line)

    if not r or len(r) == 0:
        return None
    items = r[0]
    print(items)
    level = 0
    name = None
    time_range = (None, None)
    assignees = []
    if items[0].startswith("#"):
        level = len(items[0].strip())
    if len(items) > 1: name = items[1]
    if len(items) > 2: time_range = parse_time_range(items[2])
    if len(items) > 3: assignees = parse_assignees(items[3])
    return (level, name, time_range, assignees)

#
def parse_sched_file(sched_file):
    with open(sched_file) as file:
        o = Objective()
        for line in file.readlines():
            line = line.strip()
            if not line: continue
            res = parse_line(line)
            if res[0] == 1:
                current_project = Project(res[1])
                o.add_project(current_project)
            if res[0] == 2:
                current_project = o.get_current_project()
                current_stage = Stage(res[1])
                current_project.add_stage(current_stage)
            if res[0] == 3:
                current_project = o.get_current_project()
                current_stage = current_project.get_current_stage()
                task = Task(res[1], regular_date(res[2][0]), regular_date(res[2][1]))
                for assignee in res[3]:
                    task.add_assignee(assignee)
                current_stage.add_task(task)

        return o

def my_tasks(project, assignee):
    tasks = []
    for s in project.stages:
        for t in s.tasks:
            if assignee in t.assignees:
                tasks.append((s, t))
    return tasks

def visit_objective(o, func=None):
    for p in o.projects:
        print(p.project_name)
        for s in p.stages:
            print("  " + s.stage_name)
            for t in s.tasks:
                print(f"{t.task_name}: {t.begin_date}~{t.end_date}, {t.assignees}")

def dates(date_begin=None, date_count=14):
    if not date_begin:
        date_begin = datetime.datetime.now()
    elif isinstance(date_begin, str):
        date_begin = dateutil.parser.parse(date_begin)
    f = lambda x: (date_begin+datetime.timedelta(days=x)).strftime("%Y-%m-%d")
    return [f(i) for i in range(0, date_count)]

def dates_diff(begin, end):
    a = dateutil.parser.parse(begin)
    b = dateutil.parser.parse(end)
    return (b - a).days


def prepare_bootstrap_page():
    page = pq("<html></html")
    body = pq("<body>")
    body.append(pq("<link href='https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css' rel='stylesheet'>"))
    page.append(body)
    return (page, body)

def create_tab(body, date_begin, date_count):
    tab = pq("<table>")
    tab.add_class("table table-bordered table-hover table-striped")
    thead = create_tab_header(tab, date_begin, date_count)
    tbody = pq("<tbody>")
    tab.append(tbody)
    body.append(tab)
    return tab, thead, tbody

def create_tab_header(tab, date_begin, date_count):
    thead, tr = pq("<thead>"), pq("<tr>")
    tr.append(pq("<td>项目</td>"))
    tr.append(pq("<td style='min-width:5em'>RD</td>"))
    for date in dates(date_begin, date_count):
        tr.append(pq(f"<td>{date}</td>"))
    thead.append(tr)
    tab.append(thead)
    return thead

def stage_color(stage):
    return Stages[stage][1]

def gen_project_view(o, date_begin, date_count):
    page, body = prepare_bootstrap_page()
    _tab, _thead, tbody = create_tab(body, date_begin, date_count)
    
    dates_list = dates(date_begin, date_count)
    for p in o.projects:
        has_project_name = False
        for assignee in p.all_assignees():
            tr = pq(f"<tr>")
            if not has_project_name:
                proj_td = pq(f"<td>{p.project_name}</td>")
                proj_td.attr.rowspan = str(len(p.all_assignees()))
                tr.append(proj_td)
                has_project_name = True

            assignee_td = pq(f"<td><span>{assignee}</span></td>")
            tr.append(assignee_td)

            tasks = my_tasks(p, assignee)
            if not tasks: continue

            i = 0
            while i < len(dates_list):
                hit_some_task_begin_date = False
                diff = 1
                for (stage, task) in tasks:
                    if task.begin_date == dates_list[i]:
                        hit_some_task_begin_date = True
                        date_td = pq(f"<td>")

                        diff = dates_diff(task.begin_date, task.end_date) + 1
                        date_td.append(pq(f"<span>{task.task_name}</span>"))
                        date_td.attr.colspan = str(diff)
                        color = stage_color(stage.stage)
                        date_td.attr.style = f"background-color:{color}"
                        tr.append(date_td)
                        break
                if not hit_some_task_begin_date:
                    date_td = pq(f"<td>")
                    tr.append(date_td)
                    i += 1
                else:
                    i += diff

            tbody.append(tr)
    return page

if __name__ == '__main__':

    parser = OptionParser()

    parser.add_option("-f", "--file", action="store", dest="file", help="Provide schedule filename")
    parser.add_option("-b", "--date-begin", action="store", dest="date_begin", help="Provide view begin date")
    parser.add_option("-c", "--date-count", action="store", dest="date_count", help="Provide view date count", default=30)

    options, args = parser.parse_args()
    filename = options.file
    if not filename:
        exit()
    o = parse_sched_file(filename)

    date_begin = options.date_begin
    if not date_begin:
        date_begin = get_earliest_date(o)
        
    page = gen_project_view(o, date_begin, options.date_count)

    with open(os.path.join(os.path.dirname(filename), "schedule.html"), "w") as file:
        file.write(str(page))
