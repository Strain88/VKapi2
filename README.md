# VKapi2
This is my simple VK api realisation. Originaly created for simplify audio uploading to VK.

#Usage

    from Vkapi2 import *

    session = Session('vk app token')
    api = Api(session, v=5.52)

    api.audio.get(owner_id=1, count=3)
    
#Feaures
audio.save method takes a direct link to audio file

    api.audio.save(link_to_file="link to mp3 file", artist='artist name', title='title of the song)

