from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import VideoRequestSerializer
import json
from operations.models import VideoRequest, Video, Answer


@api_view(['POST'])
def record_request(request):
    videos = request.data['videos']
    video_list = []

    for vid in videos:
        saved_vid = Video.objects.filter(video_primary_id=vid['id'])
        if len(saved_vid) > 0:
            saved_vid = saved_vid.first()
        else:
            saved_vid = Video.objects.create(
                video_primary_id=vid['id'],
                video_url=vid['video']
            )
        try:
            position = vid['position']
            saved_vid.position = position
        except:
            saved_vid.position = None
        saved_vid.save()
        if saved_vid.position is not None:
            video_list.append(saved_vid)

    answers = request.data['answers']

    answers_list = []

    for answer in answers:
        ans_video = Video.objects.get(video_primary_id=answer['video'])
        answer_obj = Answer.objects.create(
            video=ans_video,
            action=answer['action'],
            action_time=answer['action_time'],
            position=answer['position']
        )
        answers_list.append(answer_obj)

    vid_request = VideoRequest.objects.create(
        name="API Req",
        saved_experience_id=request.data['saved_experience_id']
    )
    vid_request.answers.add(*answers_list)
    vid_request.initial_videos.add(*video_list)

    return Response(VideoRequestSerializer(vid_request).data)
