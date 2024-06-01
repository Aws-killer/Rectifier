import aiohttp
import asyncio
import os
import uuid
import tempfile


class ElevenLab:
    def __init__(self):
        self.api_url = "https://4336zvnmaw.us-east-1.awsapprunner.com"
        self.dir = str(tempfile.mkdtemp())
        self.headers = {"Connection": "keep-alive", "Content-Type": "application/json"}
        self.voices = [
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Aaron [North America, Male, Adult].mp3",
                "category": "generated",
                "name": "Aaron [North America, Male, Adult]",
                "voice_id": "YGD8MPCMMCEtmc5C1e4n",
                "description": "american, young, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Abigail.mp3",
                "category": "generated",
                "name": "Abigail",
                "voice_id": "C3Iez0cLQu2nhWdeIdRL",
                "description": "american, confident, young, female, social_media",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Adam.mp3",
                "category": "premade",
                "name": "Adam",
                "voice_id": "pNInz6obpgDQGcFmaJgB",
                "description": "american, middle aged, male, narration",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Alex.mp3",
                "category": "generated",
                "name": "Alex",
                "voice_id": "LP5FiPNIUj4ZKhZ6uw7g",
                "description": "american, intense, young, male, narrative_story",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Amritanshu.mp3",
                "category": "professional",
                "name": "Amritanshu",
                "voice_id": "1qZOLVpd1TVic43MSkFY",
                "description": "indian, crisp, male, informative_educational",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Amy.mp3",
                "category": "generated",
                "name": "Amy",
                "voice_id": "kDuavY9iblawTM7XXfko",
                "description": "american, crisp, young, female, advertisement",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Andre [North America, Male, Adult].mp3",
                "category": "generated",
                "name": "Andre [North America, Male, Adult]",
                "voice_id": "U7J5NnlayshHr7Z71Wso",
                "description": "american, young, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Andrew.mp3",
                "category": "generated",
                "name": "Andrew",
                "voice_id": "EMI6TU8unLVMVRwAS4D1",
                "description": "american, casual, young, male, social_media",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Antoni.mp3",
                "category": "premade",
                "name": "Antoni",
                "voice_id": "ErXwobaYiN019PkySvjV",
                "description": "american, young, male, narration",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Arjun.mp3",
                "category": "generated",
                "name": "Arjun",
                "voice_id": "43MnyipNiFU4WSf74Xr7",
                "description": "indian, deep, young, male, informative_educational",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Arnold.mp3",
                "category": "premade",
                "name": "Arnold",
                "voice_id": "VR6AewLTigWG4xSOukaG",
                "description": "american, middle aged, male, narration",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Bill.mp3",
                "category": "premade",
                "name": "Bill",
                "voice_id": "pqHfZKP75CvOlQylNhV4",
                "description": "american, middle aged, male, documentary",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Bob [North America, Male, Old].mp3",
                "category": "generated",
                "name": "Bob [North America, Male, Old]",
                "voice_id": "q0WcWS65WZ2a6Z30XyKU",
                "description": "american, old, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Bosco [North America, Male, Adult].mp3",
                "category": "generated",
                "name": "Bosco [North America, Male, Adult]",
                "voice_id": "NSJUUCbctHs2xlXnpUGC",
                "description": "african, young, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Brad  [North America, Male, Adult].mp3",
                "category": "generated",
                "name": "Brad  [North America, Male, Adult]",
                "voice_id": "S456qluv8mEX39UfR9jm",
                "description": "american, middle_aged, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Brandon [North America, Male, Old].mp3",
                "category": "generated",
                "name": "Brandon [North America, Male, Old]",
                "voice_id": "Jb2ZETbcvvfQ0yT8AfQm",
                "description": "american, old, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Brian [North America, Male, Old].mp3",
                "category": "generated",
                "name": "Brian [North America, Male, Old]",
                "voice_id": "ZPAZxV13vwBPd4zQNxt1",
                "description": "american, old, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Bruce [North America, Male, Adult] [Deep].mp3",
                "category": "generated",
                "name": "Bruce [North America, Male, Adult] [Deep]",
                "voice_id": "l8QWgIvZBvDFhRXCNlJb",
                "description": "american, middle_aged, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Callum.mp3",
                "category": "premade",
                "name": "Callum",
                "voice_id": "N2lVS1w4EtoT3dr4eOWO",
                "description": "american, middle aged, male, video games",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Carl.mp3",
                "category": "generated",
                "name": "Carl",
                "voice_id": "cxnObTdeUVB31HmS6G4p",
                "description": "british, deep, old, male, conversational",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Caroline [UK, Female, Adult].mp3",
                "category": "generated",
                "name": "Caroline [UK, Female, Adult]",
                "voice_id": "8HZKfomDkVF1FtMOTNJ6",
                "description": "british, young, female",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Charlie.mp3",
                "category": "premade",
                "name": "Charlie",
                "voice_id": "IKne3meq5aSn9XLyUdCD",
                "description": "australian, middle aged, male, conversational",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Charlotte.mp3",
                "category": "premade",
                "name": "Charlotte",
                "voice_id": "XB0fDUnXU5powFXDhCwa",
                "description": "english-swedish, middle aged, female, video games",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Clyde.mp3",
                "category": "premade",
                "name": "Clyde",
                "voice_id": "2EiwWnXFnvU5JabPnv8n",
                "description": "american, middle aged, male, video games",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Daniel.mp3",
                "category": "premade",
                "name": "Daniel",
                "voice_id": "onwK4e9ZLuTAKqWW03F9",
                "description": "british, middle aged, male, news presenter",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Dave.mp3",
                "category": "premade",
                "name": "Dave",
                "voice_id": "CYw3kZ02Hs0563khs1Fj",
                "description": "british-essex, young, male, video games",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Diva.mp3",
                "category": "generated",
                "name": "Diva",
                "voice_id": "vZSVcdpJoUZLAAyZYfAz",
                "description": "indian, formal, young, female, narrative_story",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Domi.mp3",
                "category": "premade",
                "name": "Domi",
                "voice_id": "AZnzlk1XvdvUeBnXmlld",
                "description": "american, young, female, narration",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Dorothy.mp3",
                "category": "premade",
                "name": "Dorothy",
                "voice_id": "ThT5KcBeYPX3keUQqHPh",
                "description": "british, young, female, children's stories",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Drew.mp3",
                "category": "premade",
                "name": "Drew",
                "voice_id": "29vD33N1CtxCmqQRPOHJ",
                "description": "american, middle aged, male, news",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Erika [UK, Female, Young].mp3",
                "category": "generated",
                "name": "Erika [UK, Female, Young]",
                "voice_id": "jdL71PLBSnnAYbmq8EwJ",
                "description": "indian, young, female",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Ethan.mp3",
                "category": "premade",
                "name": "Ethan",
                "voice_id": "g5CIjZEefAph4nQFvHAz",
                "description": "american, young, male, ASMR",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Ezreal.mp3",
                "category": "generated",
                "name": "Ezreal",
                "voice_id": "2W8QxcEi69qc1wh8xhuk",
                "description": "american, confident, young, male, characters_animation",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Fin.mp3",
                "category": "premade",
                "name": "Fin",
                "voice_id": "D38z5RcWu1voky8WS1ja",
                "description": "irish, old, male, video games",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Freya.mp3",
                "category": "premade",
                "name": "Freya",
                "voice_id": "jsCqWAovK2LkecY7zXl4",
                "description": "american, young, female, video games",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Gabby.mp3",
                "category": "generated",
                "name": "Gabby",
                "voice_id": "ZdnuY2mr2iEYUH8OlDmk",
                "description": "african, husky, young, female, narrative_story",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Gabriella.mp3",
                "category": "generated",
                "name": "Gabriella",
                "voice_id": "GpOuURs45N7gHfIxH2j3",
                "description": "american, sassy, middle_aged, female, characters_animation",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Gerald [UK, Male, Adult].mp3",
                "category": "generated",
                "name": "Gerald [UK, Male, Adult]",
                "voice_id": "rn36nUPcGjSHnlNRtl2X",
                "description": "african, old, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Gillian [North America, Female, Adult].mp3",
                "category": "generated",
                "name": "Gillian [North America, Female, Adult]",
                "voice_id": "WTKq0GrBaTs4d5xqZoA7",
                "description": "american, young, female",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Giovanni.mp3",
                "category": "premade",
                "name": "Giovanni",
                "voice_id": "zcAOhNBS3c14rBihAFp1",
                "description": "english-italian, young, male, audiobook",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Glinda.mp3",
                "category": "premade",
                "name": "Glinda",
                "voice_id": "z9fAnlkpzviPz146aGWa",
                "description": "american, middle aged, female, video games",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Grace.mp3",
                "category": "premade",
                "name": "Grace",
                "voice_id": "oWAxZDx7w5VEj9dCyTzz",
                "description": "american-southern, young, female, audiobook ",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Hank [North America, Male, Old].mp3",
                "category": "generated",
                "name": "Hank [North America, Male, Old]",
                "voice_id": "zpfB1puKk5dflnrZ4HGz",
                "description": "american, old, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Hannah.mp3",
                "category": "generated",
                "name": "Hannah",
                "voice_id": "p328nLsZIvWPC8EWiUCn",
                "description": "american, pleasant, middle_aged, female, narrative_story",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Harry.mp3",
                "category": "premade",
                "name": "Harry",
                "voice_id": "SOYHLrjzK2X1ezoPC6cr",
                "description": "american, young, male, video games",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Iris.mp3",
                "category": "generated",
                "name": "Iris",
                "voice_id": "fml9pRck6vnUvMoFvHKc",
                "description": "american, gentle, young, female, conversational",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/James.mp3",
                "category": "generated",
                "name": "James",
                "voice_id": "Sz46BeRyiz9Nx9xud23c",
                "description": "american, confident, middle_aged, male, characters_animation",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Jax.mp3",
                "category": "generated",
                "name": "Jax",
                "voice_id": "tSdKNFB9FPJtIN25C69n",
                "description": "african, mature, middle_aged, male, conversational",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Jeremy.mp3",
                "category": "premade",
                "name": "Jeremy",
                "voice_id": "bVMeCyTHy58xNoL34h3p",
                "description": "american-irish, young, male, narration",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Jessie.mp3",
                "category": "premade",
                "name": "Jessie",
                "voice_id": "t0jbNlBVZ17f02VDIeMI",
                "description": "american, old, male, video games",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Jim.mp3",
                "category": "generated",
                "name": "Jim",
                "voice_id": "mEBve583FI8xnS7cSwoX",
                "description": "american, pleasant, young, male, entertainment_tv",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Joanne [North America, Female, Adult].mp3",
                "category": "generated",
                "name": "Joanne [North America, Female, Adult]",
                "voice_id": "bT0vAXwKx82DBH9CGTqu",
                "description": "american, young, female",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Johannes [Africa, Male, Old].mp3",
                "category": "generated",
                "name": "Johannes [Africa, Male, Old]",
                "voice_id": "nwKTA4kI2U6cfdm4iDBk",
                "description": "african, old, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Joseph [Africa, Male, Old] [Deep].mp3",
                "category": "generated",
                "name": "Joseph [Africa, Male, Old] [Deep]",
                "voice_id": "mPtNnreciJ73eSPiBAD8",
                "description": "african, old, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Josh.mp3",
                "category": "premade",
                "name": "Josh",
                "voice_id": "TxGEqnHWrfWFTfGW9XjX",
                "description": "american, young, male, narration",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Julia.mp3",
                "category": "generated",
                "name": "Julia",
                "voice_id": "NgMsArH2b26HVAumF6yx",
                "description": "american, upbeat, young, female, narrative_story",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Julius [North America, Male, Adult].mp3",
                "category": "generated",
                "name": "Julius [North America, Male, Adult]",
                "voice_id": "kFDE1ElcvrWbgJWeRoke",
                "description": "american, young, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Kalu [Africa, Male, Adult].mp3",
                "category": "generated",
                "name": "Kalu [Africa, Male, Adult]",
                "voice_id": "OpO4DJa2ejVDSB76Iwt2",
                "description": "african, young, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Keli.mp3",
                "category": "generated",
                "name": "Keli",
                "voice_id": "oDhbxAtuC0OEMIN9duZC",
                "description": "american, excited, young, female, social_media",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Kiel [UK, Male, Adult].mp3",
                "category": "generated",
                "name": "Kiel [UK, Male, Adult]",
                "voice_id": "GDMsifKZMfgKlSSRHZ3p",
                "description": "british, old, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Kimber.mp3",
                "category": "generated",
                "name": "Kimber",
                "voice_id": "zadU88Br2ruxenJGqQxG",
                "description": "american, excited, middle_aged, female, narrative_story",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Lena.mp3",
                "category": "generated",
                "name": "Lena",
                "voice_id": "iighga31Bs4C1CTjor8i",
                "description": "american, cheeky, young, female, social_media",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Liam.mp3",
                "category": "premade",
                "name": "Liam",
                "voice_id": "TX3LPaxmHKxFdv7VOQHJ",
                "description": "american, young, male, narration",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Magnolia.mp3",
                "category": "generated",
                "name": "Magnolia",
                "voice_id": "87vOnVOmLljNG4xII0mT",
                "description": "african, mature, middle_aged, female, informative_educational",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Marcus [North America, Male, Adult] [Deep].mp3",
                "category": "generated",
                "name": "Marcus [North America, Male, Adult] [Deep]",
                "voice_id": "Wd5ZirjKPabjvtTgnQg0",
                "description": "american, middle_aged, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Marques.mp3",
                "category": "generated",
                "name": "Marques",
                "voice_id": "8ooYQvuWViEmIJMaUu2X",
                "description": "african, pleasant, young, male, narrative_story",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Maryanne.mp3",
                "category": "generated",
                "name": "Maryanne",
                "voice_id": "3tpDcwOtqrwlpVOPn6Ut",
                "description": "american, cute, young, female, Storytelling",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Matilda.mp3",
                "category": "premade",
                "name": "Matilda",
                "voice_id": "XrExE9yKIg1WjnnlVkGX",
                "description": "american, young, female, audiobook",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Matthew  [North America, Male, Adult] [Whisper].mp3",
                "category": "generated",
                "name": "Matthew  [North America, Male, Adult] [Whisper]",
                "voice_id": "J5Hc23uOggalhqMTa6nE",
                "description": "american, middle_aged, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Maya.mp3",
                "category": "generated",
                "name": "Maya",
                "voice_id": "546EISeOlrDbgOmIO3uZ",
                "description": "american, meditative, young, female, narrative_story",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Michael.mp3",
                "category": "premade",
                "name": "Michael",
                "voice_id": "flq6f7yk4E4fJM5XTYuZ",
                "description": "american, old, male, audiobook",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Mick [Australia, Male, Adult].mp3",
                "category": "generated",
                "name": "Mick [Australia, Male, Adult]",
                "voice_id": "2Ta4CbBZJ2Nhp7yFxi2Y",
                "description": "australian, middle_aged, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Mike.mp3",
                "category": "generated",
                "name": "Mike",
                "voice_id": "rkvn7xzNBv9lCtEH24Zz",
                "description": "american, calm, young, male, entertainment_tv",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Myra.mp3",
                "category": "generated",
                "name": "Myra",
                "voice_id": "GdrtyESFVdYwpmLnq4UL",
                "description": "american, upbeat, young, female, conversational",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Myriam [North America, Female, Young].mp3",
                "category": "generated",
                "name": "Myriam [North America, Female, Young]",
                "voice_id": "OMrznXTO38QqtBa9XfFu",
                "description": "australian, young, female",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Natasha.mp3",
                "category": "generated",
                "name": "Natasha",
                "voice_id": "xn9QM1b1mWMSQmbALzen",
                "description": "american, sassy, young, female, social_media",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Natasia.mp3",
                "category": "generated",
                "name": "Natasia",
                "voice_id": "9tqVIPhSvVt8FDeAYMO7",
                "description": "african, mature, middle_aged, female, conversational",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Nicole.mp3",
                "category": "premade",
                "name": "Nicole",
                "voice_id": "piTKgcLEGmPE4e6mEKli",
                "description": "american, young, female, audiobook",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Noah.mp3",
                "category": "generated",
                "name": "Noah",
                "voice_id": "R7jBf6zxDQJtm1iq6rW7",
                "description": "american, calm, young, male, informative_educational",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Oliver.mp3",
                "category": "generated",
                "name": "Oliver",
                "voice_id": "OLf8fsuVSS6VyuFoDlHY",
                "description": "american, modulated, young, male, narrative_story",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Oscar [UK, Male, Old].mp3",
                "category": "generated",
                "name": "Oscar [UK, Male, Old]",
                "voice_id": "4lbz9Mt70VF7v82XdjaO",
                "description": "african, old, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Paola.mp3",
                "category": "generated",
                "name": "Paola",
                "voice_id": "sn3BNXKryoY3l9c74BnN",
                "description": "american, gentle, young, female, conversational",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Patricia.mp3",
                "category": "generated",
                "name": "Patricia",
                "voice_id": "FrZ4dJ6V1jMCoSUJO23Y",
                "description": "american, pleasant, young, female, conversational",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Patrick [Africa, Male, Adult].mp3",
                "category": "generated",
                "name": "Patrick [Africa, Male, Adult]",
                "voice_id": "c6bmV2wCVOeFYal1uYSN",
                "description": "african, young, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Paul.mp3",
                "category": "premade",
                "name": "Paul",
                "voice_id": "5Q0t7uMcjvnagumLfvZi",
                "description": "american, middle aged, male, news",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Paula.mp3",
                "category": "generated",
                "name": "Paula",
                "voice_id": "CHax7ep2HJ6YE7rWRFVE",
                "description": "american, gentle, middle_aged, female, narrative_story",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Posie.mp3",
                "category": "generated",
                "name": "Posie",
                "voice_id": "LHrQJob1hKPeddMLspEa",
                "description": "african, casual, young, female, conversational",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Priya.mp3",
                "category": "generated",
                "name": "Priya",
                "voice_id": "00AtUjxZWseGNzCg2hAi",
                "description": "indian, casual, young, male, conversational",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Rachel.mp3",
                "category": "premade",
                "name": "Rachel",
                "voice_id": "21m00Tcm4TlvDq8ikWAM",
                "description": "american, young, female, narration",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Raven.mp3",
                "category": "generated",
                "name": "Raven",
                "voice_id": "ekTxB2LDTaJyy0LPAUbx",
                "description": "american, pleasant, young, female, social_media",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Rayan.mp3",
                "category": "generated",
                "name": "Rayan",
                "voice_id": "yB4kbvttg3WWq5R8HuEX",
                "description": "american, confident, old, female, entertainment_tv",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Rebecca [North America, Female, Young].mp3",
                "category": "generated",
                "name": "Rebecca [North America, Female, Young]",
                "voice_id": "DjPz1qB9cteHqNMbnzaz",
                "description": "american, young, female",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Rose [North America, Female, Young].mp3",
                "category": "generated",
                "name": "Rose [North America, Female, Young]",
                "voice_id": "sYLUtZpVhnGchwd2pYGC",
                "description": "american, young, female",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Sally.mp3",
                "category": "generated",
                "name": "Sally",
                "voice_id": "QtKATu8gXE525Ml2aqnV",
                "description": "american, relaxed, young, female, conversational",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Sam.mp3",
                "category": "premade",
                "name": "Sam",
                "voice_id": "yoZ06aMxZJJ28mfd3POQ",
                "description": "american, young, male, narration",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Sanjay [India, Male, Adult].mp3",
                "category": "generated",
                "name": "Sanjay [India, Male, Adult]",
                "voice_id": "GnF7mpJrZJ5fq9WkxF6w",
                "description": "indian, middle_aged, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Sara.mp3",
                "category": "generated",
                "name": "Sara",
                "voice_id": "wRTEg58D7p7fc9Knory0",
                "description": "american, intense, young, female, characters_animation",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Scarlett.mp3",
                "category": "generated",
                "name": "Scarlett",
                "voice_id": "F2j1uF488FjKPfWDdt6p",
                "description": "american, pleasant, middle_aged, female, conversational",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Sneha [India, Female, Adult].mp3",
                "category": "generated",
                "name": "Sneha [India, Female, Adult]",
                "voice_id": "xUDy0qehRqP0gA1DHlgJ",
                "description": "indian, young, female",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Sunita [India, Female, Young].mp3",
                "category": "generated",
                "name": "Sunita [India, Female, Young]",
                "voice_id": "kQXZXdVadBByBfGwsU5B",
                "description": "indian, young, female",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Thomas.mp3",
                "category": "premade",
                "name": "Thomas",
                "voice_id": "GBv7mTt0atIp3Br8iCZE",
                "description": "american, young, male, meditation",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Timmy.mp3",
                "category": "generated",
                "name": "Timmy",
                "voice_id": "GQ6B5bGEswEmbiAqoFpo",
                "description": "british, casual, young, male, social_media",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/Walter [North America, Male, Adult].mp3",
                "category": "generated",
                "name": "Walter [North America, Male, Adult]",
                "voice_id": "Ad8LXrZKVRNA2vjIglDH",
                "description": "australian, old, male",
            },
            {
                "preview_url": "https://augie-background-music.s3.amazonaws.com/voices/William [North America, Male, Adult].mp3",
                "category": "generated",
                "name": "William [North America, Male, Adult]",
                "voice_id": "f3DHv9UOLFJoO8JHmvhc",
                "description": "american, young, male",
            },
        ]

    async def _make_request(self, method, endpoint, json=None):
        async with aiohttp.ClientSession() as session:
            async with getattr(session, method)(
                f"{self.api_url}/{endpoint}", json=json
            ) as response:
                return await response.json()

    async def say(self, text, speaker="Adam"):

        for i in self.voices:
            name = i["name"].split(" ")[0]
            if name.lower() == speaker.lower():
                voiceId = i["voice_id"]
        data = {"voiceId": voiceId, "text": text}

        response_data = await self._make_request("post", "convert", json=data)
        print(response_data)
        audio_url = response_data["contentUrl"]
        temp = await self.download_file(audio_url)
        return audio_url, temp

    async def download_file(self, url):
        filename = str(uuid.uuid4()) + ".mp3"
        os.makedirs(self.dir, exist_ok=True)
        save_path = os.path.join(self.dir, filename)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(save_path, "wb") as file:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            file.write(chunk)

        return save_path


# Usage
# async def main():
#     tts = ElevenLab()
#     await tts.say("Did you know that you don't have the balls to talk to me")


# Run the main function
# asyncio.run(main())
