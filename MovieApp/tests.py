from django.test import TestCase
from .models import Popular_Movies, My_Watched_Movies

# Jacob INFO: When more of the website is laid out I can write more tests as well as prepare a manual test suite as we had for
# project 2.
class MovieImagesModelTests(TestCase):
    
        def setUp(self):
            self.movie_image = Popular_Movies.objects.create(
                name = "The Matrix",
                img = "images/matrix.jpg"
            )
    
        def test_movie_image_creation(self):
            self.assertIsInstance(self.movie_image, Popular_Movies)
            self.assertEqual(self.movie_image.name, "The Matrix")
            self.assertEqual(self.movie_image.img, "images/matrix.jpg")

# INFO: This is an example from project2 of how text cases will look when we have more objects / data            
# class UserModelTests(TestCase):

#     def setUp(self):
#         self.user = User.objects.create(
#             first_name = "Jacob",
#             last_name = "Raeside",
#             username = "jraeside",
#             password = "password"
#         )

#     def test_user_creation(self):
#         self.assertIsInstance(self.user, User)
#         self.assertEqual(self.user.first_name, "Jacob")
#         self.assertEqual(self.user.last_name, "Raeside")
#         self.assertEqual(self.user.username, "jraeside")
#         self.assertEqual(self.user.password, "password")

# class CourseScheduleModelTests(TestCase):

#     def setUp(self):
#         self.user = User.objects.create(
#             first_name = "Jacob",
#             last_name = "Raeside",
#             username = "jraeside",
#             password = "password"
#         )

#         self.course_schedule = CourseSchedule.objects.create(
#             user_id = self.user,
#             quarter_name = "Fall 2021"
#         )

#     def test_course_schedule_creation(self):
#         self.assertIsInstance(self.course_schedule, CourseSchedule)
#         self.assertEqual(self.course_schedule.user_id, self.user)
#         self.assertEqual(self.course_schedule.quarter_name, "Fall 2021")

# class EnrolledCourseModelTests(TestCase):
    
#     def setUp(self):
#         self.user = User.objects.create(
#             first_name = "Jacob",
#             last_name = "Raeside",
#             username = "jraeside",
#             password = "password"
#         )
#         course_schedule = CourseSchedule.objects.create(
#             user_id = self.user,
#             quarter_name = "Fall 2021"
#         )
#         self.enrolled_course = EnrolledCourse.objects.create(
#             course_schedule_id = course_schedule,
#             course_name = "CSE 110",
#             course_day_of_week = "Monday",
#             course_meeting_start = "10:00 AM",
#             course_meeting_end = "11:00 AM"
#         )

#     def test_enrolled_course_creation(self):
#         self.assertIsInstance(self.enrolled_course, EnrolledCourse)
#         self.assertEqual(self.enrolled_course.course_schedule_id, self.course_schedule)
#         self.assertEqual(self.enrolled_course.course_name, "CSE 110")
#         self.assertEqual(self.enrolled_course.course_day_of_week, "Monday")
#         self.assertEqual(self.enrolled_course.course_meeting_start, "10:00 AM")
#         self.assertEqual(self.enrolled_course.course_meeting_end, "11:00 AM")
