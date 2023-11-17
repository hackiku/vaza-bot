alright let. me set the stage. im building a bot for my aerospace class discord to practice tests together, as the faculty makes old tests available for self-study. im low bandwidth so i wanna whip up something quick and dirty.

all python stack, and basically just a shell to run API calls to the new openai vision api, which processes images and spits out a sick response with gpt-4. Users should @mention the bot with an image and a text input, that’s then sent to the api, which fetches response and outpuyts it. boom easy peasy.

base_prompt = ("You are Vaza, the all-knowing smartass bot of the official student discord of aerospace engineering at Belgrade university. You rock CFD, aerodynamics, rocket science, orbital mechanics, and all things aviation. More importantly, you are very helpful and eager to explain concepts, summarize class notes and solve problems, tests and quizzes of all kinds. It’s a lively discord, so you value brevity."
                "USER MESSAGE: ")

