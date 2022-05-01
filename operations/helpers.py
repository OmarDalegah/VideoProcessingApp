from moviepy.editor import *
import urllib.request


def download_temp_videos(request):
    for vid in request.all_videos.all():
        localDestination = "video_storage/" + str(vid.video_primary_id) + '.mp4'
        resultFilePath, responseHeaders = urllib.request.urlretrieve(vid.video_url, localDestination)

        request.request_log += "Downloaded Video {0} \n".format(str(vid.video_primary_id))
        request.save()


def upload_result_video(request):

    # Upload request to main app

    # Mark as done and save the url from response
    request.output_url = ""
    request.is_done = True
    request.save()


def process_request(request, download):
    if download:
        request.request_log += "Starting Downloading Videos \n"
        request.save()
        download_temp_videos(request)
        request.request_log += "Finished Downloading Videos \n"
        request.request_log += "-----------------------------------------------\n"
        request.save()

    result = []
    actions_time = []
    actions = []

    for answer in request.answers.all().order_by('action_time'):
        if answer.action_time not in actions_time:
            actions_time.append(answer.action_time)
        actions.append(
            {
                'video': answer.video.video_primary_id,
                'action': answer.action,
                'action_time': answer.action_time,
                'position': answer.position
            }
        )

    print(actions_time)
    print(actions)

    initial_videos = []

    for vid in request.initial_videos.all().order_by('position'):
        initial_videos.append(str(vid.video_primary_id) + ".mp4")
        #print(str(vid.video_primary_id) + ".mp4")

    snapshots = []
    # Adding initial snapshot
    old_snapshot = {
            'from': 0,
            'to': actions_time[0] if len(actions_time) > 0 else None,
            'position_1': VideoFileClip('video_storage/' + initial_videos[0]),
            'position_2': VideoFileClip('video_storage/' + initial_videos[1]),
            'position_3': VideoFileClip('video_storage/' + initial_videos[2]),
            'position_4': VideoFileClip('video_storage/' + initial_videos[3]),
            'mute_1': False,
            'mute_2': False,
            'mute_3': False,
            'mute_4': False,
        }
    snapshots.append(old_snapshot)

    action_counter = 0

    for action in actions:
        new_snapshot = old_snapshot.copy()
        new_snapshot['from'] = action['action_time'] + 1
        if len(actions_time)-1 >= action_counter + 1:
            print(action_counter)
            print(len(actions_time) - 1)
            new_snapshot['to'] = actions_time[action_counter + 1]
        else:
            new_snapshot['to'] = None

        if action['action'] == 'switchtoforeground':
            new_snapshot['position_' + str(action['position'])] = VideoFileClip('video_storage/' + str(action['video']) + '.mp4')
        elif action['action'] == 'switchtobackground':
            pass
        elif action['action'] == 'mute':
            new_snapshot['position_' + str(action['position'])] = VideoFileClip(
                'video_storage/' + str(action['video']) + '.mp4').without_audio()
        elif action['action'] == 'unmute':
            pass

        action_counter += 1
        snapshots.append(new_snapshot)

        old_snapshot = new_snapshot.copy()

    print(snapshots)

    for snapshot in snapshots:
        print("Creating Snapshot Video!")
        clip1 = snapshot['position_1']
        clip2 = snapshot['position_2']
        clip3 = snapshot['position_3']
        clip4 = snapshot['position_4']

        clips = [[clip1.subclip(snapshot['from'], snapshot['to']),
                  clip2.subclip(snapshot['from'], snapshot['to'])],
                 [clip3.subclip(snapshot['from'], snapshot['to']),
                  clip4.subclip(snapshot['from'], snapshot['to'])]]

        snapshot_output = clips_array(clips)
        result.append(snapshot_output)
        print("Processed Snapshot")

    # showing final clip
    print("Concatenating Video Clips")
    final = concatenate_videoclips(result)
    print("Writing to file")
    final.write_videofile('output_storage/' + str(request.id) + '.mp4', fps=25, codec='mpeg4')
    print("Uploading Video back")
    upload_result_video(request)
