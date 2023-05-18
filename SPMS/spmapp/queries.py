from django.db import connection
from spmapp.models import *
import numpy as np

studentlist = Student_T.objects.all()

programlist = Program_T.objects.all()

# Semesters Information


def getAllSemesters():
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT DISTINCT reg_semester
            FROM spmapp_registration_t  
        ''')

        row = cursor.fetchall()
    return row


# A chart showing percentage score in each PLO in a selected course against the average score (from the students in the same course).
def getStudentCourseWisePLO(studentID, courseID):
    with connection.cursor() as cursor:
        cursor.execute(''' 

            SELECT p.ploNum as ploNum,(sum(e.obtainedMarks)/sum(a.totalMarks))*100 as plo_per, drived.avg
            FROM spmapp_registration_t r,
                spmapp_assessment_t a, 
                spmapp_evaluation_t e,
                spmapp_co_t co, 
                spmapp_plo_t p,
                (SELECT p.ploNum as ploNumA,(sum(e.obtainedMarks)/sum(a.totalMarks))*100 as avg
                        FROM spmapp_registration_t r,
                            spmapp_assessment_t a, 
                            spmapp_evaluation_t e,
                            spmapp_co_t co, 
                            spmapp_plo_t p
                        WHERE r.registrationID = e.registrationID 
                            and e.assessment_id = a.assessmentID
                            and a.coID=co.coID 
                            and co.courseID = '{}'      # problem
                            and co.plo_id = p.ploID 
                        GROUP BY p.ploID) derived

            WHERE r.regID = e.regID 
                and e.assessmentID = a.assessmentID
                and a.coID=co.coID 
                and co.ploID = p.ploID 
                and r.studentID = '{}'
                and co.courseID = '{}'
                and p.ploNum = derived.ploNumA
            GROUP BY  r.student_id,p.ploID)

               '''.format(courseID, studentID, courseID))
        row = cursor.fetchall()

    ploNum = []
    avg = []
    plo_percentage = []

    for i in row:
        ploNum.append(i[0])
        plo_percentage.append(i[1])
        avg.append(i[2])

    return ploNum, plo_percentage, avg


# A chart showing percentage score in each PLO against the program average (from the students in the same program).
def getStudentProgramWisePLO(studentID, programID):
    with connection.cursor() as cursor:
        cursor.execute('''
             
            SELECT p.ploNum as ploNum, 100*(sum(e.obtainedMarks)/sum(a.TotalMarks)) as perStd, derived2.avg as avg 
            FROM spmapp_registration_t r,
                spmapp_evaluation_t e,
                spmapp_assessment_t a,
                spmapp_co_t c,
                spmapp_plo_t p,
                (
                SELECT derived.plonum as plonum, avg(per) as avg
                FROM(
                    SELECT p.ploID as PLOID, p.ploNum as ploNum, 100*sum(e.obtainedMarks)/sum(a.TotalMarks) as per
                    FROM spmapp_registration_t r,
                        spmapp_evaluation_t e,
                        spmapp_student_t st,
                        spmapp_program_t p,
                        spmapp_assessment_t a,
                        spmapp_co_t c,
                        spmapp_plo_t p
                    WHERE r.student_id = st.studentID
                        and st.program_id = p.programID
                        and e.registration_id = r.registrationID
                        and a.assessmentID = e.assessment_id
                        and a.co_id = c.coID
                        and c.plo_id = p.ploID
                        and st.program_id = '{}'
                        GROUP BY p.ploID,r.student_id) derived
                GROUP BY derived.PLOID
                ) derived2
            WHERE r.studentID = '{}'
                and p.programID = '{}'
                and e.regID = r.regID
                and a.assessmentID = e.assessmentID
                and a.coID = c.coID
                and c.ploID = p.ploID
                p.ploNum = derived2.plonum
            GROUP BY p.ploNum)
             
            '''.format(programID, studentID, programID))
        row = cursor.fetchall()
    """
        ploNum = []
        perStd = []
        avg = []

        for i in row:
            ploNum.append(i[0])
            perStd.append(i[1])
            avg.append(i[2])
    """
    return row


# A table showing the PLOs achieved and failed to achieve (with percentage score) for a selected student in all the courses taken by that student so far.
def getCourseWiseStudentPLO(studentID, cat):
    with connection.cursor() as cursor:
        cursor.execute(''' 
               SELECT p.ploNum as ploNum,co.course_id,sum(e.obtainedMarks),sum(a.totalMarks), derived.Total
               FROM spmapp_registration_t r,
                   spmapp_assessment_t a, 
                   spmapp_evaluation_t e,
                   spmapp_co_t co, 
                   spmapp_plo_t p,
                   (
                        SELECT p.ploNum as ploNum,sum(a.totalMarks) as Total, r.student_id as StudentID
                        FROM spmapp_registration_t r,
                            spmapp_assessment_t a, 
                            spmapp_evaluation_t e,
                            spmapp_co_t co, 
                            spmapp_plo_t p
                        WHERE r.registrationID = e.registration_id 
                            and e.assessment_id = a.assessmentID
                            and a.co_id=co.coID 
                            and co.plo_id = p.ploID 
                            and r.student_id = '{}'
                        GROUP BY  r.student_id,p.ploID) derived
               WHERE r.student_id = derived.StudentID
                    and e.registration_id = r.registrationID
                    and e.assessment_id = a.assessmentID
                    and a.co_id=co.coID 
                    and co.plo_id = p.ploID
                    and p.ploNum = derived.ploNum

               GROUP BY  p.ploID,co.course_id

               '''.format(studentID))
        row = cursor.fetchall()

    table = []
    courses = []

    for entry in row:
        if entry[1] not in courses:
            courses.append(entry[1])
    courses.sort()
    plo = ["PLO1", "PLO2", "PLO3", "PLO4", "PLO5", "PLO6",
           "PLO7", "PLO8", "PLO9", "PLO10", "PLO11", "PLO12"]

    for i in courses:
        temptable = []
        if cat == 'report':
            temptable = [i]

        for j in plo:
            found = False
            for k in row:
                if j == k[0] and i == k[1]:
                    if cat == 'report':
                        temptable.append(np.round(100 * k[2] / k[3], 2))
                    elif cat == 'chart':
                        temptable.append(np.round(100 * k[2] / k[4], 2))
                    found = True
            if not found:
                if cat == 'report':
                    temptable.append('N/A')
                elif cat == 'chart':
                    temptable.append(0)
        table.append(temptable)
    return plo, courses, table


# ******************* PLO performance trend of selected course/s *************************
# For chosen semester/s, a chart comparing the PLO achieved percentage for each PLO among the instructors who have taken the course.

def getCourseWise_PLO_AmongInstructor(semester, year, course):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            SELECT i.instructorID, c.courseID, s.sec_semester, s.year,(sum(e.obtainedMarks)/sum(a.totalMarks))*100
            FROM spmapp_evaluation_t e,
                spmapp_course_t c, 
                spmapp_instructor_t i,
                spmapp_assessment_t a,
                spmapp_section_t s,
                spmapp_co_t co,
                spmapp_plo_t p
            WHERE e.assessmentID = a.assessmentID
                and c.courseID = s.courseID
                and s.instructorID = i.accountID
                and c.courseID = s.courseID
                and a.coID = co.coID
                and co.coID = p.ploID
                and co.courseID = c.courseID 
                and s.sec_semester = '{}'
                and s.year = '{}'
                and c.courseID = '{}'
            GROUP BY i.instructorID
        '''.format(semester, year, course))
        row = cursor.fetchall()
    return row


# For selected PLO/s, within the timeframe of chosen semester/s, a comparison of PLO achievement percentage among courses which have
# the same PLO/s that was/were selected.

def getPloWisePLO(semester, year, plo, course):
    with connection.cursor() as cursor:
        cursor.execute(''' 
        SELECT p.ploNum, s.sec_semester, s.year, c.courseID, (sum(e.obtainedMarks)/sum(a.totalMarks))*100
        FROM spmapp_course_t c,
            spmapp_assessment_t a,
            spmapp_evaluation_t e,    
            spmapp_co_t co,
            spmapp_plo_t p,
            spmapp_section_t s
        WHERE e.assessmentID = a.assessmentID
            and a.coID = co.coID
            and co.courseID = c.courseID
            and co.coID = p.ploID
            and s.courseID = c.courseID
            and s.year = '{}'
            and s.sec_semester = '{}'
            and p.ploNum = '{}'
            and c.courseID = '{}'
                '''.format(year, semester, plo, course))
        row = cursor.fetchall()
    return row


# For chosen semester/s, a chart showing the percentage of students who achieved each of the PLOs and that of those who failed.

# in a selected course/s => a student plo percentage in a specific PLO
def getSemesterWiseStudentPLO(semester, year, course):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            SELECT p.ploNum, s.sec_semester, s.year, c.courseID, r.studentID, (sum(e.obtainedMarks)/sum(a.totalMarks))*100 
            FROM spmapp_course_t c,
                spmapp_assessment_t a,
                spmapp_evaluation_t e,    
                spmapp_co_t co,
                spmapp_plo_t p,
                spmapp_section_t s,
                spmapp_spmapp_registration_t r

            WHERE e.assessmentID = a.assessmentID
                and a.coID = co.coID
                and co.courseID = c.courseID
                and co.coID = p.ploID
                and s.courseID = c.courseID
                and r.regID = e.regID
                and s.sectionID = r.sectionID
                and s.year = '{}'
                and s.sec_semester = '{}'
                and c.courseID = '{}'
            GROUP BY p.ploNum, r.studentID
        '''.format(year, semester, course))
        row = cursor.fetchall()
    return row


# ******************* PLO performance trend of selected program/s *********************
# For chosen semester/s, a chart showing the count of students who attempted each PLO against that of those who achieved.
# in a selected program/s => a student plo percentage in a specific PLO
def getProgramWiseStudentNumber(semester, year, program):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            SELECT plo.ploNum, r.reg_semester, r.year, plo.programID, r.studentID, (sum(e.obtainedMarks)/sum(a.totalMarks))*100 
            FROM spmapp_course_t c,
                spmapp_assessment_t a,
                spmapp_evaluation_t e,    
                spmapp_co_t co,
                spmapp_plo_t plo,
                spmapp_section_t s,
                spmapp_registration_t r,
                spmapp_program_t p

            WHERE e.assessmentID = a.assessmentID
                and a.coID = co.coID
                and co.courseID = c.courseID
                and co.ploID = plo.ploID
                and s.courseID = c.courseID
                and r.regID = e.regID
                and s.sectionID = r.sectionID
                and p.programID = plo.programID
                and s.year = '{}'
                and s.sec_semester = '{}'
                and p.programName = '{}'
            GROUP BY plo.ploNum, r.studentID
                '''.format(year, semester, program))
        row = cursor.fetchall()
    return row


# For chosen semester/s, a chart showing the count of students who achieved each PLO, segmented with color-code into the percentage of the
# count that came from the courses that have that PLO. Alternative view with segmentation based on CO instead of course.
# count of student => in the view.py file
def getProgramWiseStudentNumber_course(semester, year, program):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            SELECT plo.ploNum, c.courseID, r.studentID, (sum(e.obtainedMarks)/sum(a.totalMarks))*100 
            FROM spmapp_course_t c,
                spmapp_assessment_t a,
                spmapp_evaluation_t e,    
                spmapp_co_t co,
                spmapp_plo_t plo,
                spmapp_section_t s,
                spmapp_registration_t r,
                spmapp_program_t p

            WHERE e.assessmentID = a.assessmentID
                and a.coID = co.coID
                and co.courseID = c.courseID
                and co.ploID = plo.ploID
                and s.courseID = c.courseID
                and r.regID = e.regID
                and s.sectionID = r.sectionID
                and p.programID = plo.programID
                and s.year = '{}'
                and s.sec_semester = '{}'
                and p.programName = '{}'
            GROUP BY plo.ploNum, c.courseID, r.studentID
                '''.format(year, semester, program))
        row = cursor.fetchall()
    return row


# Upon clicking on any one of the PLOs from the previous chart, a pie chart showing a clearer segmentation should be displayed.
#         =>  extra work for html with the same sql given data set


# ******************** PLO performance trend of selected university/s *******************
# For a selected program, a radar chart showing the PLO achieved count comparison for each PLO within a chosen time frame.

def getUniversityWiseCountStudent_program(semester, year, program, university):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            SELECT plo.ploNum, c.courseID, r.studentID, (sum(e.obtainedMarks)/sum(a.totalMarks))*100, u.universityName
            FROM spmapp_course_t c,
                spmapp_assessment_t a,
                spmapp_evaluation_t e,    
                spmapp_co_t co,
                spmapp_plo_t plo,
                spmapp_section_t s,
                spmapp_registration_t r,
                spmapp_program_t p,
                spmapp_department_t d,
                spmapp_school_t sch,
                spmapp_university_t u,

            WHERE e.assessmentID = a.assessmentID
                and a.coID = co.coID
                and co.courseID = c.courseID
                and co.ploID = plo.ploID
                and s.courseID = c.courseID
                and r.regID = e.regID
                and s.sectionID = r.sectionID
                and p.programID = plo.programID
                and p.departmentID = d.departmentID
                and d.schoolID = sch.schoolID
                and sch.universityID = u.universityID
                and s.year = '{}'
                and s.sec_semester = '{}'
                and p.programName = '{}'
                and u.universityID = '{}'
            GROUP BY plo.ploNum, c.courseID, r.studentID
                '''.format(year, semester, program, university))
        row = cursor.fetchall()
    return row

# For chosen programs, a radar chart comparing the percentage of graduates who have achieved all PLOs of the chosen programs.


# count of student => in the view.py file
def getUniversityWiseGraduateStudent(program, university):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            SELECT plo.ploNum, c.courseID, st.accountID, (sum(e.obtainedMarks)/sum(a.totalMarks))*100, u.universityName
            FROM spmapp_course_t c,
                spmapp_assessment_t a,
                spmapp_evaluation_t e,    
                spmapp_co_t co,
                spmapp_plo_t plo,
                spmapp_section_t s,
                spmapp_registration_t r,
                spmapp_program_t p,
                spmapp_department_t d,
                spmapp_school_t sch,
                spmapp_university_t u,
                spmapp_student_t st

            WHERE e.assessmentID = a.assessmentID
                and a.coID = co.coID
                and co.courseID = c.courseID
                and co.ploID = plo.ploID
                and s.courseID = c.courseID
                and r.regID = e.regID
                and s.sectionID = r.sectionID
                and p.programID = plo.programID
                and p.departmentID = d.departmentID
                and d.schoolID = sch.schoolID
                and sch.universityID = u.universityID
                and st.accountID = r.studentID
                and st.graduateDate IS NOT NULL
                and p.programName = '{}'
                and u.universityID = '{}'
            GROUP BY plo.ploNum, c.courseID, st.accountID
                '''.format(program, university))
        row = cursor.fetchall()
    return row


# For a selection of one/more PLO/s, a comparison of the percentage of students who achieved that/those chosen PLO/s (percentage derived from
# total attempted vs achieved)

def getUniversityWisePLO(plo, university):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            SELECT plo.ploNum, c.courseID, st.accountID, (sum(e.obtainedMarks)/sum(a.totalMarks))*100, u.universityName
            FROM spmapp_course_t c,
                spmapp_assessment_t a,
                spmapp_evaluation_t e,    
                spmapp_co_t co,
                spmapp_plo_t plo,
                spmapp_section_t s,
                spmapp_registration_t r,
                spmapp_program_t p,
                spmapp_department_t d,
                spmapp_school_t sch,
                spmapp_university_t u,
                spmapp_student_t st

            WHERE e.assessmentID = a.assessmentID
                and a.coID = co.coID
                and co.courseID = c.courseID
                and co.ploID = plo.ploID
                and s.courseID = c.courseID
                and r.regID = e.regID
                and s.sectionID = r.sectionID
                and p.programID = plo.programID
                and p.departmentID = d.departmentID
                and d.schoolID = sch.schoolID
                and sch.universityID = u.universityID
                and st.accountID = r.studentID
                and plo.ploNum = '{}'
                and u.universityID = '{}'
            GROUP BY plo.ploNum, c.courseID, st.accountID
                '''.format(plo, university))
        row = cursor.fetchall()
    return row

# ****************** Miscellaneous PLO performance trend *******************
# For selected departments/schools, a chart comparing the percentage count of students who achieved all the PLOs they have attempted within a
# chosen time frame.


def getDepartmentWisePLO(department, semester, year):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            SELECT plo.ploNum, c.courseID, st.accountID, (sum(e.obtainedMarks)/sum(a.totalMarks))*100, d.departmentID, sch.schoolID
            FROM spmapp_course_t c,
                spmapp_assessment_t a,
                spmapp_evaluation_t e,    
                spmapp_co_t co,
                spmapp_plo_t plo,
                spmapp_section_t s,
                spmapp_registration_t r,
                spmapp_program_t p,
                spmapp_department_t d,
                spmapp_student_t st,
                spmapp_school_t sch

            WHERE e.assessmentID = a.assessmentID
                and a.coID = co.coID
                and co.courseID = c.courseID
                and co.ploID = plo.ploID
                and s.courseID = c.courseID
                and r.regID = e.regID
                and s.sectionID = r.sectionID
                and p.programID = plo.programID
                and p.departmentID = d.departmentID
                and st.accountID = r.studentID
                and sch.schoolID = d.schoolID
                and d.departmentID = '{}'
                and s.sec_semester = '{}'
                and s.year = '{}'
            GROUP BY plo.ploNum, c.courseID, st.accountID
                '''.format(department, semester, year))
        row = cursor.fetchall()
    return row

 # For selected departments/schools, a chart comparing the average count of PLOs achieved within a chosen time frame. => prev sql


# For a selected instructor, a chart showing the percentage of students who achieved each PLO in the course/s taught by that instructor within a
# chosen time frame. Upon selecting a specific PLO from that chart, a further comparison of PLO achievement percentage w.r.t. other instructors for that
# chosen PLO should be displayed within the same time frame that was already selected for the source chart.


def getInstructorWisePLO(instructor, semester, year):
    with connection.cursor() as cursor:
        cursor.execute(''' 
            SELECT plo.ploNum, c.courseID, r.studentID, (sum(e.obtainedMarks)/sum(a.totalMarks))*100, i.name
            FROM spmapp_course_t c,
                spmapp_assessment_t a,
                spmapp_evaluation_t e,    
                spmapp_co_t co,
                spmapp_plo_t plo,
                spmapp_section_t s,
                spmapp_registration_t r,
                spmapp_instructor_t i

            WHERE e.assessmentID = a.assessmentID
                and a.coID = co.coID
                and co.courseID = c.courseID
                and co.ploID = plo.ploID
                and s.courseID = c.courseID
                and r.regID = e.regID
                and s.sectionID = r.sectionID
                and s.instructorID = i.instructorID
                and i.name = '{}'
                and s.sec_semester = '{}'
                and s.year = '{}'
            GROUP BY plo.ploNum, c.courseID, st.accountID
                '''.format(instructor, semester, year))
        row = cursor.fetchall()
    return row
