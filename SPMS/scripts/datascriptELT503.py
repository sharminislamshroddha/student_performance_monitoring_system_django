from spmapp.models import *
import django
import pandas as pd
import os
import random
import datetime

course = Course_T(courseID='ELT503', courseName="ELT cde", numOfCredits=3, program_id=5,
                  courseType="Core")
course.save()

# CO
plolist = list(PLO_T.objects.filter(program_id=5))

colist = []

colist.append(CO_T(coNum="CO1", course=course, plo=plolist[8]))
colist.append(CO_T(coNum="CO2", course=course, plo=plolist[9]))
colist.append(CO_T(coNum="CO3", course=course, plo=plolist[10]))
colist.append(CO_T(coNum="CO4", course=course, plo=plolist[11]))

colist[0].save()
colist[1].save()
colist[2].save()
colist[3].save()

instructors = []
instructors.append(Instructor_T.objects.get(pk=4501))
instructors.append(Instructor_T.objects.get(pk=4502))
instructors.append(Instructor_T.objects.get(pk=4503))

dept = Department_T.objects.get(pk=5)
program = Program_T.objects.get(pk=5)


def updatedatabase(d, sem, y):

    df = pd.read_excel("ELT503.xlsx", sheet_name="Marks")

    data = df.values.tolist()

    comid = data[0][5:11]
    cofin = data[0][13:17]
    colab = data[0][19]

    midmarks = data[2][5:11]
    finmarks = data[2][13:17]
    labmark = data[2][19]

    data = data[3:][:]

    for i in data:
        i[1] = int(i[1]) + d
        i[3] = int(int(i[3]))

    currentstudents = list(Student_T.objects.all())
    newstudents = []

    sections = []

    for i in data:
        if i[1] not in currentstudents:
            newstudents.append(i[1])

        if i[3] not in sections:
            sections.append(i[3])
    sections.sort()
    # Students
    x = datetime.date(2020, 12, 13)
    for i in newstudents:
        if (i % 10) == 0:
            student = Student_T(studentID=i, program=program, graduateDate=x)
        else:
            student = Student_T(studentID=i, program=program)
        student.save()

    # Sections

    sectionlist = []

    for i in sections:
        faculty = instructors[i - 1]
        section = Section_T(sectionNum=i, course=course,
                            instructor=faculty, sec_semester=sem, year=y)
        section.save()
        sectionlist.append(section)

    # Registration
    reglist = []

    for i in data:
        st = Student_T.objects.get(pk=i[1])
        reg = Registration_T(
            student=st, section=sectionlist[i[3] - 1], reg_semester=sem, year=y)
        reg.save()
        reglist.append(reg)

    # Assessment
    assessmentlist = []
    for i in range(1, len(sectionlist) + 1):
        for j in range(1, len(comid) + 1):

            coid = []

            for k in colist:
                if k.coNum == comid[j - 1]:
                    coid = k
                    break

            assessment = Assessment_T(assessmentName="Mid", questionNum=j, totalMarks=midmarks[j - 1], coID=coid,
                                      sectionID=sectionlist[i - 1], instructorID=instructors[0], weight=30)
            assessment.save()
            assessmentlist.append(assessment)

        for j in range(1, len(cofin) + 1):

            coid = []

            for k in colist:
                if k.coNum == cofin[j - 1]:
                    coid = k
                    break
            assessment = Assessment_T(assessmentName="Final", questionNum=j, totalMarks=finmarks[j - 1], coID=coid,
                                      sectionID=sectionlist[i - 1], instructorID=instructors[0], weight=40)

            assessment.save()
            assessmentlist.append(assessment)

        coid = []

        for k in colist:
            if k.coNum == colab:
                coid = k
                break

        assessment = Assessment_T(assessmentName="Lab", questionNum=1, totalMarks=labmark, coID=coid,
                                  sectionID=sectionlist[i - 1], instructorID=instructors[0], weight=30)
        assessment.save()
        assessmentlist.append(assessment)

    # Evaluation

    evlist = []

    for i in range(0, len(data)):
        marks = data[i][5:11]
        marks.extend(data[i][13:17])
        marks.append(data[i][19])

        num = 11 * (data[i][3] - 1)

        for j in range(0, len(marks)):
            tmark = assessmentlist[num+j].totalMarks
            omark = random.randint(0, int(tmark))
            ev = Evaluation_T(obtainedMarks=omark, assessment=assessmentlist[num+j], reg=reglist[i],
                              instructor=Instructor_T.objects.get(pk=assessmentlist[num+j].instructorID))
            ev.save()
            evlist.append(ev)


updatedatabase(0, "Spring", 2020)
updatedatabase(100, "Summer", 2020)
updatedatabase(200, "Autumn", 2020)
