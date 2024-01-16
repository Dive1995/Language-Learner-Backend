from flask import Flask
from flask_restful import Api, Resource, reqparse
from youtube_transcript_api import YouTubeTranscriptApi
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
api = Api(app)

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("video_id", type=str, help="Video id missing", required=True)
video_put_args.add_argument("lang", type=str, help="Language missing", required=True)


class YotubeVideo(Resource):
    def post(self):
        args = video_put_args.parse_args()
        transcript = None
        print(args["video_id"])

        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(args["video_id"])
            
            try:
                manual_transcript = transcript_list.find_manually_created_transcript([args["lang"]])  
                print("manual ",manual_transcript)
                transcript = manual_transcript

            except Exception as e:
                print(f"Excepption thrown no manual transcripts: {e}")
            
            if transcript is None:
                try:
                    generated_transcript = transcript_list.find_generated_transcript([args["lang"]])
                    print("generated ",generated_transcript)  
                    transcript = generated_transcript
                except Exception as e:
                    print(f"Exception thrown no generated transcripts: {e}")

        except Exception as e:
            print(f"Programmatic exception thrown: {e}")
        
        return {"transcript": None, "is_generated": None} if transcript is None else {"transcript":transcript.fetch(), "is_generated":transcript.is_generated}
        

api.add_resource(YotubeVideo, "/video")
# api.add_resource(YotubeVideo, "/video/<string:video_id>")

if __name__ == "__main__":
    app.run(debug=True)