
import datetime, re, os, sys, dateutil.parser
from functools import reduce
from pyquery import PyQuery as pq
from optparse import OptionParser

Date_Format = "%Y-%m-%d"

Stages = { 
    1: ("设计", "#deebff", "blue"),
    2: ("开发", "#e3fcef", "green"),
    3: ("联调", "#fffae5", "yellow"),
    4: ("测试", "#f4f5f7", "grey"),
    5: ("上线", "#ffebe5", "red")}

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
        return sorted(set(reduce(lambda y, x: y + list(x.all_assignees()), self.stages, [])))

def parse_stage(stage):
    for s, n in Stages.items():
        if n[0] == stage: return s
    return 0

class Stage:
    def __init__(self, stage_name):
        self.stage_name = stage_name
        self.stage = parse_stage(stage_name)
        self.tasks = []
    
    def add_task(self, task):
        self.tasks.append(task)

    def all_assignees(self):
        return sorted(set(reduce(lambda y, x: y + x.assignees, self.tasks, [])))

class Task:
    def __init__(self, task_name, begin_date, end_date):
        self.task_name = task_name
        self.begin_date = begin_date
        self.end_date = end_date
        self.assignees = []
    
    def add_assignee(self, assignee):
        self.assignees.append(assignee)

def yield_task(o):
    for p in o.projects:
        for s in p.stages:
            for t in s.tasks: yield t

def get_earliest_begin_date(o):
    date = "3000-01-01"
    for t in yield_task(o):
        if date > t.begin_date: date = t.begin_date
    return date

def get_latest_end_date(o, date):
    for t in yield_task(o):
        if date < t.end_date: date = t.end_date
    return date

def regular_date(date):
    return dateutil.parser.parse(date).strftime(Date_Format)

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
    r = re.findall(r"(#+)\s*([\s\w~\-_+\(\)!%]*)\s*(\[[\w~-]*\])?\s*(@.*)?", line)
    if not r or len(r) == 0: return None
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
            if not res: continue
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
    return None

def my_tasks(project, assignee):
    return [(s, t) for s in project.stages for t in s.tasks if assignee in t.assignees]

# TODO: Add external workingDays config
def is_working_day(date):
    if isinstance(date, str): weekday = dateutil.parser.parse(date).weekday()
    else: weekday = date.weekday()
    return weekday != 5 and weekday != 6

def dates(date_begin=None, date_count=14, only_working_dates=True):
    if not date_begin:
        date_begin = datetime.datetime.now()
    elif isinstance(date_begin, str):
        date_begin = dateutil.parser.parse(date_begin)
    f = lambda x: date_begin + datetime.timedelta(days=x)
    dates_list = [f(i) for i in range(0, date_count)]
    if only_working_dates:
        return list(filter(lambda x: is_working_day(x), dates_list))
    return dates_list

def dates_diff(begin, end, only_working_dates=True):
    b, e = dateutil.parser.parse(begin), dateutil.parser.parse(end)
    if only_working_dates:
        count = 0
        while b != e:
            if is_working_day(b): count += 1
            b += datetime.timedelta(1)
        return count
    return (e - b).days

def set_bgcolor(elem, color): elem.attr.style = f"background-color: {color}"

def prepare_bootstrap_page():
    page = pq("<html>")
    body = pq("<body>")
    body.append(pq("<link href='https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css' rel='stylesheet'>"))
    page.append(body)
    return (page, body)

def create_tab(body, date_begin, date_count, only_working_dates):
    tab = pq("<table>")
    tab.add_class("table table-bordered table-hover table-striped confluenceTable tablesorter tablesorter-default")
    thead = create_tab_header(tab, date_begin, date_count, only_working_dates)
    tbody = pq("<tbody>")
    tab.append(tbody)
    body.append(tab)
    return tab, thead, tbody

def create_tab_header(tab, date_begin, date_count, only_working_dates):
    thead, tr = pq("<thead>"), pq("<tr>")
    tr.append(pq("<td>项目</td>"))
    tr.append(pq("<td style='min-width:5em'>RD</td>"))
    today = datetime.datetime.today().strftime(Date_Format)
    for date in dates(date_begin, date_count):
        if only_working_dates and not is_working_day(date):
            continue
        format_date = date.strftime(Date_Format)
        display = format_date[5:].replace("-", "/")
        if only_working_dates and is_working_day(date):
            if date.weekday() == 0: display += " (Mon)"
        date_td = pq(f"<td><span>{display}</span></td>")
        if format_date == today: set_bgcolor(date_td, "yellow")
        tr.append(date_td)
    thead.append(tr)
    tab.append(thead)
    return thead

def gen_project_view_task_line(tr, tasks, dates_list, only_working_dates):
    i = 0
    while i < len(dates_list):
        hit_some_task_begin_date = False
        diff = 1
        for (stage, task) in tasks:
            # TODO: 如果date_begin大于某个task的begin, 那么整个task就不会显示了
            # TODO: 一个人的两个Task是不能有交集的, 
            if task.begin_date == dates_list[i]:
                hit_some_task_begin_date = True
                date_td = pq(f"<td>")

                diff = dates_diff(task.begin_date, task.end_date, only_working_dates) + 1
                date_td.append(pq(f"<span>{task.task_name}</span>"))
                date_td.attr.colspan = str(diff)

                date_td.attr.style = f"background-color:{Stages[stage.stage][1]}"
                date_td.attr['data-highlight-colour'] = Stages[stage.stage][2]
                date_td.add_class(f"confluenceTd")
                tr.append(date_td)
                break
        if not hit_some_task_begin_date:
            date_td = pq(f"<td>")
            tr.append(date_td)

        i += diff

def gen_project_view(o, date_begin, date_count, only_working_dates):
    page, body = prepare_bootstrap_page()
    if date_count <= 0:
        date_count = dates_diff(date_begin, get_latest_end_date(o, date_begin), False) + 1

    _tab, _thead, tbody = create_tab(body, date_begin, date_count, only_working_dates)
    
    dates_list = dates(date_begin, date_count, only_working_dates)
    dates_list = list(map(lambda x: x.strftime(Date_Format), dates_list))
    for p in o.projects:
        if p.project_name.startswith('!'): continue
        has_project_name = False
        for assignee in p.all_assignees():
            tr = pq(f"<tr>")
            tbody.append(tr)
            if not has_project_name:
                proj_td = pq(f"<td>{p.project_name}</td>")
                proj_td.attr.rowspan = str(len(p.all_assignees()))
                tr.append(proj_td)
                has_project_name = True

            assignee_td = pq(f"<td><span>{assignee}</span></td>")
            tr.append(assignee_td)

            tasks = my_tasks(p, assignee)
            if tasks: gen_project_view_task_line(tr, tasks, dates_list, only_working_dates)
    return page

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file", action="store", dest="file", help="Provide schedule filename")
    parser.add_option("-b", "--date-begin", action="store", dest="date_begin", help="Provide view begin date")
    parser.add_option("-c", "--date-count", action="store", dest="date_count", help="Provide view date count", default=30)
    parser.add_option("-w", "--only-working-dates", action="store", dest="only_working_dates", help="Provide working dates setting", default=True)
    parser.add_option("-o", "--output-file", action="store", dest="output", help="Provide output file name")
    
    options, args = parser.parse_args()
    filename = options.file

    o = parse_sched_file(filename) if filename else exit()
    date_begin = options.date_begin if options.date_begin else get_earliest_begin_date(o)
    output_filename = options.output if options.output else f"{filename}.html"

    page = gen_project_view(o, date_begin, int(options.date_count), options.only_working_dates)

    with open(os.path.join(os.path.dirname(filename), output_filename), "w") as file:
        file.write(str(page))

##################
# 在项目前面加! 就可以隐藏整个项目
# 例子:
# ------------------------------------------
# 多服务商
## 设计
### 整体设计 [2019-11-1~2019-11-5] @雪芹
## 开发
### JOB开发 [7~11] @冯征
### API开发 [7~11] @泽乾
### 分单策略后端java [6~11] @雪芹
### 前端开发 [8~11] @彤硕
## 联调
### 各端联调 [12~13] @冯征 @泽乾 @雪芹 @彤硕
## 测试
### QA测试 [14~19] @冯征 @泽乾 @雪芹 @彤硕
## 上线 
### 上线 [20] @冯征 @泽乾 @雪芹 @彤硕
# ------------------------------------------