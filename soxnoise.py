# # Create background noise profile from mp3
# sox noise.mp3 -n noiseprof noise.prof

# # Remove noise from mp3 using profile
# sox input.mp3 output.mp3 noisered noise.prof 0.26


# system("command")

#  'sox .rawAudio.wav -t null /dev/null trim 0 0.5 noiseprof myprofile'

#  'sox .rawAudio.wav .noisefree.wav noisered myprofile ' + argv[3]

#  'sox .rawAudio.wav .noisefree.wav noisered myprofile 0.26'

#  $SOX "$1"  "$2"   remix -   highpass 100   norm   compand 0.05,0.2 6:-54,-90,-36,-36,-24,-24,0,-12 0 -90 0.1   vad -T 0.6 -p 0.2 -t 5   fade 0.1   reverse   vad -T 0.6 -p 0.2 -t 5   fade 0.1   reverse   norm -0.5

import os

# os.system("sox audio.wav -n trim 0 1.5 noiseprof mynoiseprofile")
# os.system("sox audio.wav noiseremoved.wav noisered mynoiseprofile 0.27")