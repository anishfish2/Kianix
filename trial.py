from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

sentences = ['Hmmm, my favorite Twitch streamer? Well, thats a tough one because there are so many talented gamers out there, right? But Id have to say Im quite partial to Pokimane. Shes got that ideal blend of skill and entertainment, and she always keep things light and fun! Just like when in a tight spot in a game, I can always count on her content to lift my spirits - kind of like when Jigglypuff uses her lullaby power! Tee-hee!',
'Well, it simply has to be Jigglypuff! Her lullaby power is so adorably enchanting, it just makes your heart do a little flip. Not forgetting that its especially handy in a tight spot during a game, right', "Who is your favorite twitch streamer"]

model = SentenceTransformer('thenlper/gte-large')
embeddings = model.encode(sentences)

