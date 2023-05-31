from django.shortcuts import render
from youtube_transcript_api import YouTubeTranscriptApi
import openai
from pytube import extract
def about(request):
    return render(request, 'ytnote/about.html')

def contact(request):
    return render(request, 'ytnote/contact.html')

def index(request):
    try:
        
        link = request.POST['link']
        
        url1 = str(link)
        url=extract.video_id(url1)
        
        srt = YouTubeTranscriptApi.get_transcript(url)
        print(srt)
        prompt1 = "explain context of the youtube video from the given text in less than 15 points and if text is too small then return less points but pint wise ,in case theres no propper information then return that provide link of the video which has more info there's info is too short but dont mention text insted call it link , or length of information is too long the return small amount of data and return small info but answer should be in points and also bold the important text :"
        for i in srt:
            prompt1 += i["text"] + " "
            
        openai.api_key = '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'
        
        prompt = prompt1
        def generate_response(prompt):
            model_engine = "text-davinci-003"
            prompt = (f"{prompt}")
          
            completions = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=1.0,
            )

            message = completions.choices[0].text
            return message.strip()

        
        response = generate_response(prompt)
     
        return render(request, 'ytnote/index.html',{'link': response})
    except KeyError:
        return render(request, 'ytnote/index.html', {'link': ''})
    except Exception as e:
        return render(request, 'ytnote/index.html', {'link': 'Oh no! Error😕. Please try a different video.'})