import numpy as np
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .queries import *
from spmapp.models import *

# Create your views here.

# list

schoollist = School_T.objects.all()
deptlist = Department_T.objects.all()
programlist = Program_T.objects.all()
coursel = Course_T.objects.all()
sectionlist = Section_T.objects.all()
faculties = Instructor_T.objects.all()

semlist = getAllSemesters()
semesters = []
for s in semlist:
    semesters.append(s[0])

courselist = []
for c in coursel:
    courselist.append(c)


def loginview(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def logoutview(request):
    logout(request)
    return redirect('loginpage')


def userprofile(request):
    return render(request, 'page-user.html', {})


@login_required(login_url="/login/")
def homeview(request):
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name

        if group == 'Student':
            return shome(request)
        if group == 'Instructor':
            return fhome(request)
        if group == 'Higher Authority':
           return hahome(request)
        else:
            return redirect('/')

# ****************** STUDENT View ********************

@login_required(login_url="/login/")
def shome(request):
    name = request.user.get_full_name()
    usertype = request.user.groups.all()[0].name

    studentid = 1823001

    row = getStudentWisePLO_program(studentid)
    chart1 = 'PLO Achievement'
    plolabel1 = []
    plodata1 = []

    for i in row:
        plolabel1.append(i[0])
        plodata1.append(i[1])

    return render(request, 'student/studenthome.html', {
        'name': name,
        'usertype': usertype,

        'chart1': chart1,
        'plolabel1': plolabel1,
        'plodata1': plodata1,

    })


# *************  1(a), 1(b) *************
def studentplo(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    student = 1416455
    row = getCourseListOfAStudent(student)
    courses = ["Select Course"]
    for i in row:
        courses.append(i[0])

    if request.method == 'POST':
        # student = int(request.POST['student'])
        course = request.POST['course']
        st = Student_T.objects.get(pk=student)
        prog = st.program
        dept = prog.department
        school = dept.school
        uni = school.university

        row = getStudentWiseePLO_course(student, course)
        plo1 = []
        table1 = []

        for i in row:
            plo1.append(i[0])
            table1.append(i[1])

        row = getCourseWisePLO(course, uni.universityID)
        table2 = []
        plo2 = []
        for i in row:
            plo2.append(i[0])
            table2.append(i[1])

        row = getStudentWisePLO_program(student)
        plo3 = []
        table3 = []

        for i in row:
            plo3.append(i[0])
            table3.append(i[1])

        pplo = []
        row = getProgramWisePLOpp(prog.programID)
        for r in row:
            pplo.append(r[1])
        

        response = {
            'name': name,
            'usertype': type,

            'plo1': plo1,
            'table1': table1,

            'plo2': plo2,
            'table2': table2,

            'courses': courses,
            'selectCourse': course,
             'plo3': plo3,
            'table3': table3,
            'pplo': pplo,

            'search': 0,
            'segment': 'PLO Analysis'
        }

        return render(request, 'ploanalysis/studentplo.html', response)
    else:
        return render(request, 'ploanalysis/studentplo.html', {
            'name': name,
            'usertype': type,
            'courses': courses,
            'selectedCourse': None,
            'search': 1,
            'segment': 'PLO Analysis'

        })

#  ***************  1(c)  ****************


def studentplotable_st(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    studentid = 1416455
    (plo, courses, table) = getCourseWiseStudentPLO(studentid, 'report')
    range = len(courses)
    return render(request, 'studentplotable_st.html', {
        'name': name,
        'usertype': type,
        'plo': plo,
        'courses': courses,
        'table': table,
        'range': range,
        'sid': studentid,
        'search': 0,

        })


# ********************* FACULTY VIEW **************************
@login_required(login_url="/login/")
def fhome(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    deptT = Instructor_T.objects.get(pk=int(request.user.username))

    dept = deptT.department_id

    row = getDeptWisePLO(dept)
    plolabel = []
    plodata = []

    for i in row:
        plolabel.append(i[0])
        plodata.append(i[1])

    return render(request, 'facultyhome.html', {
        'name': name,
        'usertype': type,

        'plolabel': plolabel,
        'plodata': plodata,

    })


# data entry
def dataentry(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    courselist = Course_T.objects.all()

    courses = []
    for c in courselist:
        courses.append(c.courseID)

    semesters = ["Spring", "Summer", "Autumn"]

    sections = [1, 2, 3]
    year = [2019, 2020]

    return render(request, 'dataentry.html', {
        'name': name,
        'usertype': type,
        'courses': courses,
        'semesters': semesters,
        'sections': sections,
        'year': year,
    })


def courseinfoentry(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    courselist = Course_T.objects.all()
    courses = []
    for c in courselist:
        courses.append(c.courseID)

    semesters = ["Spring", "Summer", "Autumn"]

    sections = [1, 2, 3]
    year = [2019, 2020]

    return render(request, 'courseinfoentry.html', {
        'name': name,
        'usertype': type,
        'courses': courses,
        'semesters': semesters,
        'sections': sections,
        'year': year,
    })


def plocomapping(request):
    usertype = request.user.groups.all()[0].name
    if request.method == 'POST':
        courseID = request.POST.get('course')
        coMaps = request.POST.getlist('coMaps')

        course = Course_T.objects.get(pk=50)

        plist = PLO_T.objects.all()

        plolist = []

        for p in plist:
            if p.program_id == course.program_id:
                plolist.append(p)

        for i in range(len(coMaps)):
            k = -1

            for p in range(len(plolist)):
                if plolist[p].ploNum == coMaps[i]:
                    k = p
            co = CO_T(coNum="CO" + str(i + 1), course=course, plo=plolist[k])
            co.save()

        return redirect('plocomapping')
    else:
        return render(request, 'plocomapping.html', {
            'usertype': usertype,
            'clist': courselist,

        })


def assessmentdataentry(request):
    usertype = request.user.groups.all()[0].name

    sections = [1, 2, 3]

    if request.method == 'POST':
        faculty_id = request.user.username
        course_id = request.POST.get('course')
        sectionNo = request.POST.get('section')
        semester = request.POST.get('semester')
        totalMarks = request.POST.getlist('totalMarks')
        weightage = request.POST.getlist('weightAge')
        assessmentName = request.POST.getlist('assessmentName')
        questions = request.POST.getlist('questions')
        cos = request.POST.getlist('co')

        section_id = None
        try:
            sections = Section_T.objects.raw('''
                SELECT *
                FROM spmapp_section_t s,
                    spmapp_course_t c
                WHERE s.course_id = c.courseID
                    AND c.courseID = '{}'
                    AND sectionNum = '{}'
                    AND sec_semester = '{}'

            '''.format(course_id, sectionNo, semester))
            section_id = sections[0].sectionID
        except:
            section_id = None

        if section_id is None:
            section = Section_T(sectionNum=sectionNo, course_id=12,
                                instructor_id=faculty_id, sec_semester=semester, year=2021)
            section.save()
            section_id = section.sectionID

        for j in range(1, len(totalMarks) + 1):
            conum = cos[j-1]
            co_id = CO_T.objects.raw('''
                SELECT *
                FROM spmapp_co_t co,
                spmapp_course_t c
                WHERE co.course_id = c.courseNum
                    AND c.courseID = '{}'
                    AND co.coNum = '{}'
            '''.format(course_id, conum))

            assessment = Assessment_T(sectionID_id=section_id, coID_id=co_id[0].coID, totalMarks=totalMarks[j - 1],
                                      assessmentName=assessmentName[j-1], questionNum=questions[j-1], instructorID_id=4102,weight=weightage[j-1])
            assessment.save()

        return redirect('assessmentdataentry')

    else:
        return render(request, 'assessmentdataentry.html', {
            'usertype': usertype,
            'clist': courselist,
            'semesters': semesters,
            'sections': sections,

        })


def evaluationdataentry(request):
    usertype = request.user.groups.all()[0].name
    section = [1, 2, 3]

    if request.method == 'POST':
        course_id = request.POST.get('course')
        section = request.POST.get('section')
        semester = request.POST.get('semester')

        print(course_id)
        print(section)
        print(semester)

        student_id = request.POST.getlist('student')
        obtainedMarks = []
        questions = []
        for i in range(len(student_id)):
            obtainedMarks.append(request.POST.getlist(f'obtainedMarks{i}'))
            questions.append(request.POST.getlist(f'questions'))

        section_id = None
        try:
            section_id = Section_T.objects.raw('''
                 SELECT *
                FROM spmapp_section_t s,
                    spmapp_course_t c
                WHERE s.course_id = c.courseNum
                    AND c.courseID = '{}'
                    AND sectionNum = '{}'
                    AND sec_semester = '{}'
            '''.format(course_id, section, semester))
            section_id = section_id[0].sectionID
            print(section_id)
        except:
            section_id = None
        assessment_list = []
        coLength = 0
        try:
            col = CO_T.objects.raw('''
                SELECT count(*)
                FROM spmapp_co_t co,
                    spmapp_course_t c
                    WHERE co.course_id = c.courseNum
                        AND c.courseID = '{}'
                '''.format(course_id))
            coLength = col[0][0]+1
        except:
            coLength = 0
        for j in range(1, len(questions[0])+1):
            assessment_id = None
            try:
                assessment_id = Assessment_T.objects.raw('''
                    SELECT *
                    FROM spmapp_assessment_t
                    WHERE sectionID_id = '{}'
                        AND coID_id IN (
                        SELECT coID
                        FROM spmapp_co_t co,
                            spmapp_course_t c
                        WHERE co.course_id = c.courseNum
                            AND c.courseID = '{}'
                            AND questionNum = '{}'
                    )
                '''.format(section_id, course_id, j))
                assessment_list.append(assessment_id[0].assessmentID)
            except:
                assessment_id = None
                assessment_list.append(assessment_id)

        for i in range(len(student_id)):

            registration_id = None
            try:
                registration_id = Registration_T.objects.raw('''
                    SELECT *
                    FROM spmapp_registration_t
                    WHERE student_id = '{}'
                        AND section_id = '{}'
                '''.format(student_id[i], section_id))
                registration_id = registration_id[0].registrationID
            except:
                registration_id = None

            if registration_id is None:
                print(section_id)
                print(student_id[i])
                registration = Registration_T(
                    student_id=student_id[i], section_id=2, reg_semester=semester)
                registration.save()
                registration_id = registration.regID

            for j in range(len(assessment_list)):
                evaluation = Evaluation_T(reg_id=registration_id, assessment_id= 3,
                                          obtainedMarks=obtainedMarks[i][j], instructor_id = 4102)
                evaluation.save()
        return redirect('evaluationdataentry')
    else:
        return render(request, 'evaluationdataentry.html', {
            'usertype': usertype,
            'clist': courselist,
            'semesters': semesters,
            'sections': section,

        })


def studentplotable(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        studentid = request.POST.get('student')
        (plo, courses, table) = getCourseWiseStudentPLO(studentid, 'report')
        range = len(courses)
        return render(request, 'studentplotable.html', {
            'name': name,
            'usertype': type,
            'plo': plo,
            'courses': courses,
            'table': table,
            'range': range,
            'sid': studentid,
            'search': 0,

        })
    else:
        return render(request, 'studentplotable.html', {
            'name': name,
            'usertype': type,
            'sid': None,
            'search': 1,
        })


# ****************** Higher Authority View *******************
@login_required(login_url="/login/")
def hahome(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    totalStudents = len(studentlist)

    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    row = getDeptWisePLO(3)
    plolabel = []
    plodata = []

    for i in row:
        plolabel.append(i[0])
        plodata.append(i[1])

    return render(request, 'hahome.html', {
        'name': name,
        'usertype': type,
        'plolabel': plolabel,
        'plodata': plodata,
        'segment': 'fadash'

    })



# ********************* 3(a) ************************

def programplocomp(request):
    usertype = request.user.groups.all()[0].name

    if request.method == 'POST':
        program = request.POST.get('program')
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])
        sem = ["Spring", "Summer", "Autumn"]
        labels = []
        for i in range(b, e + 1):
            labels.append(sem[i])

        expected = []
        actual = []
        plo = []

        for l in labels:
            (plo, etemp, atemp) = getProgramWisePLOComp(program, l)
            expected.append(etemp)
            actual.append(atemp)

        actual = np.transpose(actual)
        actual = actual.tolist()

        expected = np.transpose(expected)
        expected = expected.tolist()

        return render(request, 'plocomp/programplocomp.html', {
            'usertype': usertype,

            'labels': labels,
            'expected': expected,
            'actual': actual,
            'plo': plo,

            'sem1': b,
            'sem2': e,
            'semesters': semesters,

            'selectedProgram': program,
            'plist': programlist,
            'search': 0,

            'segment': 'PLO Comp2'

        })
    else:
        return render(request, 'plocomp/programplocomp.html', {
            'usertype': usertype,

            'semesters': semesters,
            'search': 1,
            'plist': programlist,
            'segment': 'PLO Comp'

        })


# ************** 4(c) ***************
pp = ["PLO1", "PLO2", "PLO3", "PLO4", "PLO5", "PLO6",
    "PLO7", "PLO8", "PLO9", "PLO10", "PLO11", "PLO12"]
uu = University_T.objects.all()


def universityplowiseper(request):
    name = request.user.get_full_name()
    usertype = request.user.groups.all()[0].name

    if request.method == 'POST':
        suni = request.POST.get('uni')
        splos = request.POST.getlist('plos')

        expected = []
        actual = []
        plop = []
        for p in splos:
            (plo, etemp, atemp) = getUniversityWisePloPerformance(p, suni)
            expected.append(etemp)
            actual.append(atemp)
            plop.append(plo)

        return render(request, 'universitywiseplo.html', {
            'usertype': usertype,

            'plop': plop,
            'expected': expected,
            'actual': actual,

            'selectedUni': suni,
            'ulist': uu,
            'selectedPlo': splos,
            'plist': pp,
            'search': 0,

            'segment': 'PLO Comp1'

        })
    else:
        return render(request, 'universitywiseplo.html', {
            'usertype': usertype,
            'ulist': uu,
            'plist': pp,
            'search': 1,
            'segment': 'PLO Comp'
        })


# ************ 2(a) **************
def instructorwiseploforcourse(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    courses = []

    for c in courselist:
        courses.append(c.courseID)

    if request.method == 'POST':
        selectedCourse = request.POST['course']
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        sem = ["Spring", "Summer", "Autumn"]
        labels = []
        uni = "IUB"
        plo = []
        insnames = []
        l = "Summer"
        (plo, insnames , t)= getInstructorWisePLOForCourse(selectedCourse, l, uni)
        labels = plo
        f1 = t[0]
        f2 = t[1]
        f3 = t[2]
        
        return render(request, 'gpa/instructorwisegpaforcourse.html', {
            'name': name,
            'usertype': type,

            'courses': courses,
            'semesters': semesters,

            'selected1': b,
            'selected2': e,
            'selectedCourse': selectedCourse,

            'plo': plo,
            'labels': labels,
            'insnames': insnames,

            'table': t,
            'f1': f1,
            'f2': f2,
            'f3': f3,

            'search': 0,
            'segment': 'PLO Comp'

        })

    else:
        return render(request, 'gpa/instructorwisegpaforcourse.html', {
            'name': name,
            'usertype': type,
            'courses': courses,
            'semesters': semesters,
            'selected1': None,
            'selected2': None,
            'search': 1,
            'segment': 'PLO Comp'
        })


# *************** 2(c) ****************
def courseplocomp(request):
    usertype = request.user.groups.all()[0].name

    if request.method == 'POST':
        course = request.POST.get('course')
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])
        sem = ["Spring", "Summer", "Autumn"]
        labels = []
        for i in range(b, e + 1):
            labels.append(sem[i])

        expected = []
        actual = []
        plo = []

        for l in labels:
            (plo, etemp, atemp) = getCourseWisePLOComp(course, l)
            expected.append(etemp)
            actual.append(atemp)

        actual = np.transpose(actual)
        actual = actual.tolist()

        expected = np.transpose(expected)
        expected = expected.tolist()

        return render(request, 'courseplocomp.html', {
            'usertype': usertype,

            'labels': labels,
            'expected': expected,
            'actual': actual,
            'plo': plo,

            'sem1': b,
            'sem2': e,
            'semesters': semesters,

            'selectedCourse': course,
            'clist': courselist,
            'search': 0,

            'segment': 'PLO Comp'

        })
    else:
        return render(request, 'courseplocomp.html', {
            'usertype': usertype,

            'semesters': semesters,
            'search': 1,
            'clist': courselist,
            'segment': 'PLO Comp'

        })


# *************** 2(b) ******************
def courseploper(request):
    usertype = request.user.groups.all()[0].name

    if request.method == 'POST':
        icourse = request.POST.getlist('course')
        iplo = request.POST.getlist('plos')
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        sem = ["Spring", "Summer", "Autumn"]
        labels = []
        for i in range(b, e + 1):
            labels.append(sem[i])

        table = []
        cr = []
        pl = []

            # for l in labels:
        
        c1 =[]
            # p1 = []   
        for c in icourse:
            cp = getPLO(c)
            for p in iplo:
                if(p in cp):
                    (t1,t2) = getCourseWisePLOC(c, "Spring", p)
                    table.append((t1[0]/t2[0])*100)
                    c1.append(p+" "+c)
                    
        # cr.append(c1)
        # pl.append(p1)
        print(table)
        print(c1)
            
        return render(request, 'plocourseper.html', {
            'usertype': usertype,

            'labels': c1,
            'table': table,
            'course': cr,
            'plo': pl,
            'sem1': b,
            'sem2': e,
            'semesters': semesters,
            'courses': courselist,
            'selectedCourse': icourse,
            'plist': pp,
            'selectedPlo': iplo,
            'search': 0,
            'segment': 'PLO Comp'

        })
    else:
        return render(request, 'plocourseper.html', {
            'usertype': usertype,
            'semesters': semesters,
            'courses': courselist,
            'plist': pp,
            'search': 1,
            'segment': 'PLO Comp'

        })


# *************** 3(b) ******************
def programplotable(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    if request.method == 'POST':
        program = request.POST.get('program')
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        print("******** 1 *******")        
        (plo3, co, table3) = getProgramWisePLO(program,"chart")
        (plo4, courses, table4) = getCOWiseProgramPLO(program, 'chart')

        print("plo3:***************",plo3)
        print("table3:***************",table3)
        return render(request, 'programplocwise.html',{
            'name': name,
            'usertype': type,
            'co': co,
            'plo3': plo3,
            'table3': table3,

            'courses': courses,
            'plo4': plo4,
            'table4': table4,
            'pname': program,

            'sem1': b,
            'sem2': e,
            'semesters': semesters,
            'selectedProgram': program,
            'plist': programlist,

            'search': 0,
            'segment': 'plotables'
        })

    else:
        return render(request, 'programplocwise.html', {
            'name': name,
            'usertype': type,
            'semesters': semesters,
            'plist': programlist,
            'search': 1,
            'segment': 'plotables'
        })

u = ["IUB", "BRAC"]
# ********************* 4(a) ************************
def programploradar(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name
    
    if request.method == 'POST':
        uni = request.POST.get('uni')
        program = request.POST.get('program')
        b = int(request.POST['sem1'])
        e = int(request.POST['sem2'])

        sem = ["Spring", "Summer", "Autumn"]
        labels = []
        for i in range(b, e + 1):
            labels.append(sem[i])
        
        plo = []
        data = []
        for i in labels:
            d = []
            (plo, d) = getUniversityWiseCountStudent_program(i, program, uni)
            data.append(d)
        
        return render(request, 'radar1.html', {
            'usertype': type,

            'labels': labels,
            'data': data,
            'plo': plo,

            'sem1': b,
            'sem2': e,
            'semesters': semesters,
            'uni': u,
            'selectedUni': uni,
            'selectedProgram': program,
            'plist': programlist,
            'search': 0,
            'segment': 'radar'

        })
    else:
        return render(request, 'radar1.html', {
            'usertype': type,
            'uni': u,
            'semesters': semesters,
            'search': 1,
            'plist': programlist,
            'segment': 'radar'

        })


# *************  1(a), 1(b) *************
def hastudentplo(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name

    student = 1416455
    row = getCourseListOfAStudent(student)
    courses = ["Select Course"]
    for i in row:
        courses.append(i[0])

    if request.method == 'POST':
        student = int(request.POST['student'])
        course = request.POST['course']
        st = Student_T.objects.get(pk=student)
        prog = st.program
        dept = prog.department
        school = dept.school
        uni = school.university

        row = getStudentWiseePLO_course(student, course)
        plo1 = []
        table1 = []

        for i in row:
            plo1.append(i[0])
            table1.append(i[1])

        row = getCourseWisePLO(course, uni.universityID)
        table2 = []
        plo2 = []
        for i in row:
            plo2.append(i[0])
            table2.append(i[1])

        row = getStudentWisePLO_program(student)
        plo3 = []
        table3 = []

        for i in row:
            plo3.append(i[0])
            table3.append(i[1])

        pplo = []
        row = getProgramWisePLOpp(prog.programID)
        for r in row:
            pplo.append(r[1])
        

        response = {
            'name': name,
            'usertype': type,

            'sid': student,

            'plo1': plo1,
            'table1': table1,

            'plo2': plo2,
            'table2': table2,

            'courses': courses,
            'selectCourse': course,
             'plo3': plo3,
            'table3': table3,
            'pplo': pplo,

            'search': 0,
            'segment': 'PLO State'
        }

        return render(request, 'ha_cp_stud.html', response)
    else:
        return render(request, 'ha_cp_stud.html', {
            'name': name,
            'usertype': type,
            'courses': courses,
            'selectedCourse': None,
            'sid': None,
            'search': 1,
            'segment': 'PLO State'

        })



        # ********************* 4(b) ************************
def radar2(request):
    name = request.user.get_full_name()
    type = request.user.groups.all()[0].name
    
    if request.method == 'POST':
        uni = request.POST.get('uni')
        program = request.POST.getlist('program')

        
        plo = []
        data = []
        for i in program:
            d = []
            (plo, d) = getUniversityWiseGraduateStudent(i, uni)
            data.append(d)
        labels =[]
        for i in program:
            labels.append((Program_T.objects.get(pk=i)).programName)
        
        return render(request, 'radar2.html', {
            'usertype': type,
            'labels': labels,
            'data': data,
            'plo': plo,
            'uni': u,
            'selecteduni': uni,
            'selectedProgram': program,
            'plist': programlist,
            'search': 0,
            'segment': 'radar2'

        })
    else:
        return render(request, 'radar2.html', {
            'usertype': type,
            'uni': u,
            'search': 1,
            'plist': programlist,
            'segment': 'radar2'

        })
