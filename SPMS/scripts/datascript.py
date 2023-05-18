from spmapp.models import *
import django
import pandas as pd


# Add University
university1 = University_T(
    universityID='IUB01', universityName='Independent University, Bangladesh', universityAddress='Bashundhara, Dhaka')
university1.save()

university2 = University_T(
    universityID='BRA02', universityName='Brac University, Bangladesh', universityAddress='Rampura, Dhaka')
university2.save()


# Add School for IUB
school1 = School_T(
    schoolID='SETS', schoolName='School of Engineering, Technology & Sciences', university=university1)
school1.save()

school2 = School_T(
    schoolID='SBE', schoolName='School of Business and Entrepreneurship', university=university1)
school2.save()

school3 = School_T(
    schoolID='SLASS', schoolName='School of Liberal Arts & Social Sciences', university=university1)
school3.save()

# Add School for BRAC
school4 = School_T(
    schoolID='SETS', schoolName='School of Engineering, Technology & Sciences', university=university2)
school4.save()

school5 = School_T(
    schoolID='SBE', schoolName='School of Business and Entrepreneurship', university=university2)
school5.save()

school6 = School_T(
    schoolID='SLASS', schoolName='School of Liberal Arts & Social Sciences', university=university2)
school6.save()

# Add Department for IUB

d1 = Department_T(departmentID='CSE',
                  departmentName='Computer Science & Engineering', school=school1)
d1.save()

d2 = Department_T(departmentID='EEE',
                  departmentName='Electrical and Electronics Engineering', school=school1)
d2.save()

d3 = Department_T(departmentID='ACN',
                  departmentName='Accounting', school=school2)
d3.save()

d4 = Department_T(departmentID='MIS',
                  departmentName='Management Information Systems', school=school2)
d4.save()

d5 = Department_T(departmentID='ENG',
                  departmentName='English', school=school3)
d5.save()

d6 = Department_T(departmentID='GSG',
                  departmentName='Global Studies & Governance', school=school3)
d6.save()

# Add Department for BRAC

d11 = Department_T(departmentID='CSE',
                   departmentName='Computer Science & Engineering', school=school4)
d11.save()

d22 = Department_T(departmentID='EEE',
                   departmentName='Electrical and Electronics Engineering', school=school4)
d22.save()

d33 = Department_T(departmentID='ACN',
                   departmentName='Accounting', school=school5)
d33.save()

d44 = Department_T(departmentID='MIS',
                   departmentName='Management Information Systems', school=school5)
d44.save()

d55 = Department_T(departmentID='ENG',
                   departmentName='English', school=school6)
d55.save()

d66 = Department_T(departmentID='GSG',
                   departmentName='Global Studies & Governance', school=school6)
d66.save()


# Add programs for IUB
p1 = Program_T(programName='B.Sc. in CSE', department=d1)
p1.save()

p2 = Program_T(programName='BBA in Accounting', department=d3)
p2.save()

p3 = Program_T(programName='B.Sc. in EEE', department=d2)
p3.save()

p4 = Program_T(programName='BBA in MIS', department=d4)
p4.save()

p5 = Program_T(programName='BA in ENG', department=d5)
p5.save()

p6 = Program_T(programName='BSS in GSG', department=d6)
p6.save()


# Add programs for BRAC
p11 = Program_T(programName='B.Sc. in CSE', department=d11)
p11.save()

p22 = Program_T(programName='BBA in Accounting', department=d33)
p22.save()

p33 = Program_T(programName='B.Sc. in EEE', department=d22)
p33.save()

p44 = Program_T(programName='BBA in MIS', department=d44)
p44.save()

p55 = Program_T(programName='BA in ENG', department=d55)
p55.save()

p66 = Program_T(programName='BSS in GSG', department=d66)
p66.save()

# Add PLO for all programs
programList = list(Program_T.objects.all())
details = ["Knowledge", "Requirement Analysis", "Requirement Analysis", "Design", "Problem Solving", "Implementation",
           "Experiment and Analysis", "Community Engagement and Engineering", "Teamwork", "Communication",
           "Self-Motivated", "Ethics", "Process Management"]

for p in programList:
    for i in range(1, 13):
        plonum = "PLO" + str(i)
        plo = PLO_T(ploNum=plonum, program=p, plodetails=details[i - 1])
        plo.save()

# Add Instructor Information

"""FOR IUB"""

nlist = ["Mahady Hasan", "Sadita Ahmed", "Md. Abu Sayed", "Romasa Qasim", "Mohammad Motiur Rahman", "Asif Bin Khaled", "Ferdows Zahid", "Bijoy R. Arif", "Raihan Bin Rafique",
         "Faisal M. Uddin", "Subrata Kumar Dey", "Mohammad Noor Nabi", "Farruk Ahmed", "Sabrina Alam", "Sanzar Adnan Alam"]

id = 4101

i = 0
for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", department_id=1)
    f.save()
    id = id + 1
    i = i + 1

nlist = ["Naheem Mahtab", "Md. Saifuddin ", "Susmita",
         "Shahriar", "Kamrul", "Nabila", "Abul", "Nadim", "Farzana"]

id = 4201

i = 0

for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", department_id=3)
    f.save()
    id = id + 1
    i = i + 1


nlist = ["Shahriar", "Feroz", "Kafiul", "Abdur",
         "Mustafa", "Sajib", "Naziba", "Saila", "Khosru"]


id = 4301

i = 0

for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", department_id=2)
    f.save()
    id = id + 1
    i = i + 1

nlist = ["Rezwanul", "Arifur Rahman", "Aminul",
         "Ikramul", "Bushra", "Zakia Binte"]

id = 4401

i = 0
for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", department_id=4)
    f.save()
    id = id + 1
    i = i + 1

nlist = ["Shafiul", "Sara", "Vikarun", "Adilur", "Mazaharul", "Mithila"]

id = 4501

i = 0

for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", department_id=5)
    f.save()
    id = id + 1
    i = i + 1


nlist = ["Marufa", "Imtiaz", "Ahmed", "Amjad", "Mohammad", "Shahidul"]

id = 4601

i = 0

for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", department_id=6)
    f.save()
    id = id + 1
    i = i + 1


# ********************* Faculty (BRAC) ********************
nlist = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"]

id = 5101

i = 0
for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", department_id=7)
    f.save()
    id = id + 1
    i = i + 1

nlist = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10"]

id = 5201

i = 0

for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", department_id=9)
    f.save()
    id = id + 1
    i = i + 1


nlist = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"]


id = 5301

i = 0

for n in nlist:
    f = Instructor_T(instructorID=id, name=n, accountType="I", department_id=8)
    f.save()
    id = id + 1
    i = i + 1

nlist = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10"]

id = 5401

i = 0
for n in nlist:
    f = Instructor_T(instructorID=id, name=n,
                     accountType="I", department_id=10)
    f.save()
    id = id + 1
    i = i + 1

nlist = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10"]

id = 5501

i = 0

for n in nlist:
    f = Instructor_T(instructorID=id, name=n,
                     accountType="I", department_id=11)
    f.save()
    id = id + 1
    i = i + 1


nlist = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"]

id = 5601

i = 0

for n in nlist:
    f = Instructor_T(instructorID=id, name=n,
                     accountType="I", department_id=12)
    f.save()
    id = id + 1
    i = i + 1
