from django.db import models

# Create your models here.


class Video(models.Model):
    position = models.IntegerField(null=True, blank=True)
    video_url = models.CharField(max_length=500)
    video_primary_id = models.IntegerField()


class Answer(models.Model):
    # ------------ Choice ----------- #
    ACTION = [
        ('switchtoforeground', 'Switch To Foreground'),
        ('switchtobackground', 'Switch To Background'),
        ('mute', 'Mute'),
        ('unmute', 'Unmute')
    ]

    # ------------ Fields ----------- #
    # video = models.IntegerField('Video', default=1)
    video = models.ForeignKey(to=Video, related_name='answer_video', on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField('Action', max_length=20, choices=ACTION, default='switchtoforeground')
    start_time = models.IntegerField('Start Time', default=0)
    end_time = models.IntegerField('End Time', default=0)
    action_time = models.IntegerField('Action Time', default=0)
    position = models.IntegerField('Position', default=0)


class VideoRequest(models.Model):
    name = models.CharField(max_length=256)

    answers = models.ManyToManyField(Answer, blank=True)
    initial_videos = models.ManyToManyField(Video, blank=True, related_name="initial_videos")
    all_videos = models.ManyToManyField(Video, blank=True, related_name="all_videos")

    is_done = models.BooleanField(default=False)
    output_url = models.CharField(max_length=500, null=True, blank=True)
    saved_experience_id = models.IntegerField(null=True, blank=True)

    request_log = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
