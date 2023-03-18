from django.db import models
from datetime import date
from django.core.validators import RegexValidator


# Create your models here.

REGEX_PHONE = RegexValidator(r'^(?!0|1|2|3|4|5)[0-9]{10}$', 'Invalid Mobile Number!')

CATEGORIES = (
		("SEO", "SEO"),
		("WEB", "WEB"),
		("OTHERS", "OTHERS"),
	)

class PersonalDetail(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	date_of_birth = models.DateField(blank=True, null=True)
	place_of_birth = models.CharField(max_length=100, null=True, blank=True)
	bg_image = models.ImageField()
	address = models.CharField(max_length=200, null=True, blank=True)
	pincode = models.PositiveIntegerField(blank=True, null=True)

	def __str__(self):
		return f"{self.name}"


	@property
	def calculate_age(self):
		today = date.today()
		dob = self.date_of_birth
		age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
		return age

class ProjectCategory(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	user = models.ForeignKey(PersonalDetail, related_name="user_project_categories", on_delete=models.CASCADE, blank=True, null=True)

	
	class Meta:
		verbose_name = "category"
		verbose_name_plural = "categories"

	def __str__(self):
		return f"{self.name}"


class ProjectDetail(models.Model):
	user = models.ForeignKey(PersonalDetail, related_name="user_details", on_delete=models.CASCADE)
	project_category = models.CharField(max_length=100, choices=CATEGORIES)
	name = models.CharField(max_length=50)
	client_name = models.CharField(max_length=100)
	project_date = models.DateField(blank=True, null=True)
	description = models.TextField(max_length=2000)
	display_image = models.ImageField()
	url = models.URLField(max_length=200)
	is_active = models.BooleanField(default=True)

	class Meta:
		verbose_name = "project"
		verbose_name_plural = "projects"


	def __str__(self):
		return f"{self.name}"

class ProjectDetailImage(models.Model):
	project = models.ForeignKey(ProjectDetail, related_name="project_images", on_delete=models.CASCADE)
	image = models.ImageField()

	class Meta:
		verbose_name = "project image"
		verbose_name_plural = "project images"


	def __str__(self):
		return f"{self.project.name}"




class Client(models.Model):
	name = models.CharField(max_length=50, unique=True)
	email = models.CharField(max_length=50, blank=True, null=True)
	subject = models.CharField(max_length=200, blank=True, null=True)
	message = models.TextField(max_length=2000, blank=True, null=True)
	phone_number = models.CharField(max_length=10, validators=[REGEX_PHONE])


	def __str__(self):
		return f"Client name - {self.name} - {self.email}"