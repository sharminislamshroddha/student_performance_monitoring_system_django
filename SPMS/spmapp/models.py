from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.


class University_T(models.Model):
    universityID = models.CharField(max_length=5, primary_key=True)
    universityName = models.CharField(max_length=50)
    universityAddress = models.CharField(max_length=50)

    def __str__(self):
        return self.universityID


class School_T(models.Model):
    schoolNum = models.AutoField(primary_key=True)
    schoolID = models.CharField(max_length=5)
    schoolName = models.CharField(max_length=50)
    university = models.ForeignKey(University_T, on_delete=models.CASCADE)

    def __str__(self):
        return self.schoolID


class Department_T(models.Model):
    departmentNum = models.AutoField(primary_key=True)
    departmentID = models.CharField(max_length=5)
    departmentName = models.CharField(max_length=50)
    school = models.ForeignKey(School_T, on_delete=models.CASCADE)

    def __str__(self):
        return self.departmentID


class Program_T(models.Model):
    programID = models.AutoField(primary_key=True)
    programName = models.CharField(max_length=70)
    department = models.ForeignKey(
        Department_T, on_delete=models.CASCADE, default='N/A')

    def __str__(self):
        return self.programName


class Account_T(models.Model):
    name = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=6, null=True)
    email = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=15, null=True)
    accountAddress = models.CharField(max_length=30, null=True)
    accountType = models.CharField(max_length=1, null=True)

    class Meta:
        abstract = True


class Student_T(Account_T):
    studentID = models.CharField(max_length=7, primary_key=True)
    enrollmentDate = models.DateField(null=True)
    program = models.ForeignKey(
        Program_T, on_delete=models.CASCADE, default='N/A')
    graduateDate = models.DateField(null=True)

    def __str__(self):
        return self.studentID


class VC_T(Account_T):
    vcID = models.CharField(max_length=4, primary_key=True)
    startDate = models.CharField(max_length=15, default='N/A')
    endDate = models.CharField(max_length=15, default='N/A')


class Dean_T(Account_T):
    deanID = models.CharField(max_length=4, primary_key=True)
    startDate = models.CharField(max_length=15, default='N/A')
    endDate = models.CharField(max_length=15, default='N/A')
    school = models.ForeignKey(School_T, on_delete=models.CASCADE)


class Head_T(Account_T):
    headID = models.CharField(max_length=4, primary_key=True)
    startDate = models.CharField(max_length=15, default='N/A')
    endDate = models.CharField(max_length=15, default='N/A')
    department = models.ForeignKey(Department_T, on_delete=models.CASCADE)


class Instructor_T(Account_T):
    instructorID = models.CharField(max_length=4, primary_key=True)
    startDate = models.DateField(null=True)
    rank = models.CharField(max_length=50, null=True)
    department = models.ForeignKey(Department_T, on_delete=models.CASCADE)

    def __str__(self):
        return self.instructorID


class Course_T(models.Model):
    courseID = models.CharField(max_length=7, primary_key=True)
    courseName = models.CharField(max_length=50, null=True)
    numOfCredits = models.DecimalField(max_digits=2, decimal_places=1)
    program = models.ForeignKey(Program_T, on_delete=models.CASCADE)
    courseType = models.CharField(max_length=15)

    def __str__(self):
        return self.courseID


class PrereqCourse_T(models.Model):
    course = models.ForeignKey(
        Course_T, on_delete=models.CASCADE, related_name='Course')
    preReqCourse = models.ForeignKey(
        Course_T, on_delete=models.CASCADE, related_name='PreRequisite')


class PLO_T(models.Model):
    ploID = models.AutoField(primary_key=True)
    ploNum = models.CharField(max_length=5)
    program = models.ForeignKey(Program_T, on_delete=models.CASCADE)
    plodetails = models.CharField(max_length=50)

    def __str__(self):
        return self.ploNum


class Section_T(models.Model):
    sectionID = models.AutoField(primary_key=True)
    sectionNum = models.IntegerField()
    course = models.ForeignKey(Course_T, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor_T, on_delete=models.CASCADE)
    sec_semester = models.CharField(max_length=15)
    year = models.IntegerField()

    def __str__(self):
        return str(self.sectionNum)


class Registration_T(models.Model):
    regID = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student_T, on_delete=models.CASCADE)
    section = models.ForeignKey(Section_T, on_delete=models.CASCADE)
    reg_semester = models.CharField(max_length=15)
    year = models.IntegerField(default=2020, null=True)

    def __str__(self):
        return str(self.regID)


class CO_T(models.Model):
    coID = models.AutoField(primary_key=True)
    coNum = models.CharField(max_length=4)
    course = models.ForeignKey(
        Course_T, on_delete=models.CASCADE, default='N/A')
    plo = models.ForeignKey(PLO_T, on_delete=models.CASCADE, default='N/A')
    thresold = models.FloatField(default=40)

    def __str__(self):
        return self.coNum


class CO_Course_T(models.Model):
    co = models.ForeignKey(CO_T, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course_T, on_delete=models.CASCADE, default='N/A')
    co_semester = models.CharField(max_length=15)
    co_year = models.IntegerField(default=2020, null=True)

    def __str__(self):
        return self.co


class Assessment_T(models.Model):
    assessmentID = models.AutoField(primary_key=True)
    assessmentName = models.CharField(max_length=30)
    questionNum = models.IntegerField()
    totalMarks = models.FloatField()
    coID = models.ForeignKey(CO_T, on_delete=models.CASCADE)
    sectionID = models.ForeignKey(Section_T, on_delete=models.CASCADE)
    instructorID = models.ForeignKey(Instructor_T, on_delete=models.CASCADE)
    weight = models.IntegerField()

    def __str__(self):
        return self.assessmentName + " "+str(self.questionNum)


class Evaluation_T(models.Model):
    evaluationID = models.AutoField(primary_key=True)
    obtainedMarks = models.FloatField()
    assessment = models.ForeignKey(Assessment_T, on_delete=models.CASCADE)
    reg = models.ForeignKey(Registration_T, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor_T, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.evaluationID)
