# 
import datetime, re, os, sys, copy, dateutil.parser
from functools import reduce
from pyquery import PyQuery as pq
from optparse import OptionParser
import toml

Config = toml.load("conf.toml")
Date_Format = "%Y-%m-%d"

class Project:
    def __init__(self, project_info):
        project_name, project_priv, project_status, project_pm = Project.split(project_info)
        self.project_name = project_name
        self.project_priv = project_priv
        self.project_status = project_status
        self.project_pm = project_pm
        self.stages = []

    @staticmethod
    def split(project_info):
        project_info_items = []
        if "|" in project_info: project_info_items = project_info.split("|")
        if "," in project_info: project_info_items = project_info.split(",")
        if len(project_info_items) == 0: project_info_items.append(project_info)
        while len(project_info_items) < 4:
            project_info_items.append("")
        return [p.strip() for p in project_info_items]

    def add_stage(self, stage):
        self.stages.append(stage)

    def get_current_stage(self):
        return self.stages[-1]

    def all_assignees(self):
        return sorted(set(reduce(lambda y, x: y + list(x.all_assignees()), self.stages, [])))

def parse_stage(stage):
    if stage == '': return 4
    if stage in Config['stages']:
        return Config['stages'][stage]

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

    def __str__(self):
        return f"{self.task_name} {self.begin_date}-{self.end_date}"

def yield_task(projects):
    for p in projects:
        for s in p.stages:
            for t in s.tasks: yield t

def get_earliest_begin_date(projects):
    date = "3000-01-01"
    for t in yield_task(projects):
        if t.begin_date != '' and date > t.begin_date:
            date = t.begin_date
    return date

def get_latest_end_date(projects, date):
    for t in yield_task(projects):
        if date < t.end_date: date = t.end_date
    return date

def regular_date(date):
    try:
        return dateutil.parser.parse(date).strftime(Date_Format)
    except:
        return ""

def next_day(date, working_dates, days=1):
    d = dateutil.parser.parse(date) + datetime.timedelta(days=days)
    while not is_working_day(d, working_dates):
        d += datetime.timedelta(days=1)
    return d.strftime(Date_Format)

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
    r = re.findall(r"(#+)\s*([|\s\w~\-_+\(\)!%]*)\s*(\[[\w~-]*\])?\s*(@.*)?", line)
    if not r or len(r) == 0: return None
    items = r[0]
    # print(items)
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
    projects, current_project = [], None
    with open(sched_file) as file:
        for line in file.readlines():
            line = line.strip()
            if not line: continue
            res = parse_line(line)
            if not res: continue
            if res[0] == 1:
                current_project = Project(res[1])
                projects.append(current_project)
            if res[0] == 2:
                current_stage = Stage(res[1])
                current_project.add_stage(current_stage)
            if res[0] == 3:
                current_stage = current_project.get_current_stage()
                task = Task(res[1], regular_date(res[2][0]), regular_date(res[2][1]))
                for assignee in res[3]:
                    task.add_assignee(assignee)
                current_stage.add_task(task)
    return projects

def my_stages_and_tasks(project, assignee):
    return [(s, copy.copy(t)) for s in project.stages for t in s.tasks if assignee in t.assignees]

def is_working_day(date_obj, working_dates):
    date = date_obj.strftime(Date_Format)
    if f"~{date}" in working_dates: return False
    if date in working_dates: return True
    weekday = date_obj.weekday()
    if f"w{weekday}" in working_dates: return True
    return False

def dates(date_begin=None, date_count=14, working_dates=['w0', 'w1', 'w2', 'w3', 'w4']):
    if not date_begin: date_begin = datetime.datetime.now()
    f = lambda x: date_begin + datetime.timedelta(days=x)
    return [f(i) for i in range(0, date_count) if is_working_day(f(i), working_dates)]
    
def dates_diff(begin, end, working_dates):
    b, e = dateutil.parser.parse(begin), dateutil.parser.parse(end)
    count = 0
    while b != e:
        count += is_working_day(b, working_dates)
        b += datetime.timedelta(1)
    return count

def set_bgcolor(elem, color): 
    elem.attr.style = f"background-color: {Config['colors'][color]}"
    elem.attr['data-highlight-colour'] = color

def tr_append_td(tr, td_html, colspan=1, rowspan=1):
    td = pq(f"<td>{td_html}</td>")
    if colspan != 1: td.attr.colspan = str(colspan)
    if rowspan != 1: td.attr.rowspan = str(rowspan)
    tr.append(td)
    return td

def prepare_bootstrap_page():
    page = pq("<html>")
    body = pq("<body>")
    body.append(pq("<link href='https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css' rel='stylesheet'>"))
    page.append(body)
    return (page, body)

def create_tab(body, date_begin, date_count, working_dates):
    tab = pq("<table>")
    tab.add_class("table table-bordered table-hover table-striped confluenceTable tablesorter tablesorter-default")
    thead = create_tab_header(tab, date_begin, date_count, working_dates)
    tbody = pq("<tbody>")
    tab.append(tbody)
    body.append(tab)
    return tab, thead, tbody

def create_tab_header(tab, date_begin, date_count, working_dates):
    thead, tr = pq("<thead>"), pq("<tr>")
    tr.append(pq("<td>项目</td>"))
    tr.append(pq("<td>优先级</td>"))
    tr.append(pq("<td>状态</td>"))
    tr.append(pq("<td style='min-width:5em'>DEV&QA</td>"))
    today_str = datetime.datetime.today().strftime(Date_Format)
    for date in dates(date_begin, date_count, working_dates):
        if not is_working_day(date, working_dates):
            continue
        format_date = date.strftime(Date_Format)
        display = format_date[5:].replace("-", "/")
        if is_working_day(date, working_dates) and date.weekday() == 0:
            display += " (Mon)"
        date_td = tr_append_td(tr, display, 1, 1)
        if format_date == today_str:
            set_bgcolor(date_td, "yellow")

    thead.append(tr)
    tab.append(thead)
    return thead

def gen_project_view_task_line(tr, stages_and_tasks, dates_list, working_dates):
    i = 0
    while i < len(dates_list):
        hit_some_task_begin_date = False
        diff = 1
        for (stage, task) in stages_and_tasks:
            # TODO: 如果date_begin大于某个task的begin, 那么整个task就不会显示了
            # TODO: 一个人的两个Task是不能有交集的, 
            if task.begin_date == dates_list[i]:
                hit_some_task_begin_date = True
 
                diff = dates_diff(task.begin_date, task.end_date, working_dates) + 1
                date_td = tr_append_td(tr, task.task_name, diff, 1)
                set_bgcolor(date_td, stage.stage)
                date_td.add_class(f"confluenceTd")
                break

        if not hit_some_task_begin_date:
            tr.append(pq(f"<td>"))
        i += diff

def gen_project_view(projects, date_begin, date_count, working_dates):
    page, body = prepare_bootstrap_page()
    if date_count <= 0:
        date_count = dates_diff(date_begin, get_latest_end_date(projects, date_begin), working_dates) + 1

    _tab, _thead, tbody = create_tab(body, date_begin, date_count, working_dates)
    
    dates_list = [d.strftime(Date_Format) for d in dates(date_begin, date_count, working_dates)]
    for p in projects:
        if p.project_name.startswith('!'): continue
        has_project_name = False
        for assignee in p.all_assignees():
            tr = pq(f"<tr>")
            tbody.append(tr)
            if not has_project_name:
                has_project_name = True
                row_span = str(len(p.all_assignees()))
                pm_name_part = f"<br>({p.project_pm})" if len(p.project_pm) > 0 else ""

                tr_append_td(tr, p.project_name + pm_name_part, 1, row_span)
                tr_append_td(tr, p.project_priv, 1, row_span)
                tr_append_td(tr, p.project_status, 1, row_span)

            tr_append_td(tr, assignee, 1, 1)

            stages_and_tasks = my_stages_and_tasks(p, assignee)
            if not stages_and_tasks:
                continue
            last_task_end_date = datetime.datetime.today().strftime(Date_Format)
            for (_, task) in stages_and_tasks:            
                if task.begin_date == "": task.begin_date = next_day(last_task_end_date, working_dates)
                if task.end_date == "": task.end_date = task.begin_date
                last_task_end_date = task.end_date

            gen_project_view_task_line(tr, stages_and_tasks, dates_list, working_dates)
    return page

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file", action="store", dest="file", help="Provide schedule filename")
    parser.add_option("-b", "--date-begin", action="store", dest="date_begin", help="Provide view begin date")
    parser.add_option("-c", "--date-count", action="store", dest="date_count", help="Provide view date count", default=30)
    parser.add_option("-w", "--working-dates", action="store", dest="working_dates", help="Provide working dates setting", default="w0,w1,w2,w3,w4")
    parser.add_option("-o", "--output-file", action="store", dest="output", help="Provide output file name")
    parser.add_option("-p", "--project-name", action="store", dest="project_name", help="Provide project name", default=None)
    options, args = parser.parse_args()

    filename = options.file
    projects = parse_sched_file(filename) if filename else exit()
    if options.project_name:
        projects_given = list(map(lambda x: x.strip(), options.project_name.split(',')))
        projects = list(filter(lambda x: x.project_name in projects_given, projects))
    date_begin = options.date_begin if options.date_begin else get_earliest_begin_date(projects)
    page = gen_project_view(projects, dateutil.parser.parse(date_begin), int(options.date_count), options.working_dates.split(","))

    output_filename = options.output if options.output else f"{filename}.html"
    with open(os.path.join(os.path.dirname(filename), output_filename), "w") as file:
        file.write(str(page))
