from django.db import models
# reverse() 함수는 URL 패턴을 만들어주는 장고 내장 함수
from django.core.urlresolvers import reverse
# ThumbnailImageField 클래스는 사진 원본 및 썸네일 이미지를 저장하는
# (fields.py 파일에서 정의할) 커스텀 필드 - DISQUS와 다르게 직접 코딩 및 정의해야 함
from photo.fields import ThumbnailImageField
from pytz import timezone  # 시간대 처리
from django.utils import timezone


class Album(models.Model):
	name = models.CharField('제품 카테고리', max_length=50)
	description = models.CharField('카테고리 설명', max_length=100, blank=True)

	class Meta:
		ordering = ['name']  # 순서 지정: -name으로 지정하면 최신순 정렬!!!!!!!!!!!!!!!!!

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		# 이 메소드가 정의된 객체의 URL /photo/album/99 형식의 값을 반환
		return reverse('photo:album_detail', args=(self.id,))  # 사진 번호 url


class Photo(models.Model):
	# 자신의 부모(Album)에 대한 외래키
	album = models.ForeignKey(Album)  # Album부모 테이블에서 참조!
	title = models.CharField('제목', max_length=50)
	# ThumbnailImageField는 upload_to 옵션으로 저장 위치를 지정
	# MEDIA_ROOT로 지정된 폴더 하위에 /photo/2018/03/과 같은 폴더를 생성하고,
	# 여기에 업로드된 파일을 자동적으로 저장해줌
	image = ThumbnailImageField(upload_to='photo/%Y/%m')  # media 폴더의 photo안에 Y 년도에 해당하는 폴더 \ m 날짜에 해당하는 폴더에 저장함!
	description = models.TextField('제품 설명', blank=True)  # 여러 줄로 작성할 수 있는 게 TextField
	# settings.TIME_ZONE = 'Asia/Seoul' 으로 설정해도 UTC 시각으로 처리됨
	# DB에 저장되는 시각은 UTC 시각이지만, 아래 속성 처리로 한국 시각으로 변환하여 템플릿에 제공함

  # upload_date = models.DateTimeField('등록 일시', auto_now_add=True)
	upload_date = models.DateTimeField('등록 일시', auto_now_add=True)

	# # ##############아래와 같이 속성 처리를 변경해야 한국 시각으로 처리됨#################
	# @property
	# def created_at_korean_time(self):
	# 	korean_timezone = timezone(settings.TIME_ZONE)
	# 	return self.created_at.astimezone(korean_timezone)


	# class Meta:
	# 	ordering = ['title']
	class Meta:  # 날짜 최신순 정렬
		ordering = ['-upload_date']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		# 이 메소드가 정의된 객체의 URL /photo/photo/99 형식의 값을 반환
		return reverse('photo:photo_detail', args=(self.id,))

	def get_previous_post(self):  # 3.2.5 항에서 템플릿 작성할 때 사용
		return self.get_previous_by_upload_date()

	def get_next_post(self):  # 3.2.5 항에서 템플릿 작성할 때 사용
		return self.get_next_by_upload_date()

	def get_newer_photo(self):  						# ch10_nav
		newer_photo = Photo.objects.filter(
			upload_date__gt = self.upload_date
			, album = self.album
		).order_by('upload_date').first()
		return newer_photo

	def get_older_photo(self):      					# ch10_nav
		older_photo = Photo.objects.filter(
			upload_date__lt = self.upload_date
			, album = self.album
		).order_by('-upload_date').first()
		return older_photo
